
import asyncio
import base64
import json
import re
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from urllib.parse import urljoin, urlparse

import httpx
from bs4 import BeautifulSoup
from colorthief import ColorThief
from PIL import Image

from ..core.settings import settings
from .prompts import VisionAnalysisPrompts, PromptConfig
from .weights_config import weights_config
from ..utils.timezone import get_colombia_time, format_colombia_time_short


class DesignMetrics:
    
    def __init__(self):
        self.typography = {
            "base_font_size": 16,
            "line_height_ratio": 1.4,
            "contrast_violations": [],
            "font_fallbacks": [],
            "heading_hierarchy": [],
            "paragraph_lengths": [],
            "score": 100  # Start perfect, subtract for issues found
        }
        
        self.color = {
            "primary_palette": [],
            "harmony_violations": [],
            "saturation_violations": [],
            "contrast_violations": [],
            "color_count": 0,
            "score": 100  # Start perfect, subtract for issues found
        }
        
        self.layout = {
            "whitespace_ratio": 0.3,  # Reasonable default
            "grid_violations": [],
            "section_padding": [],
            "visual_balance": {"x": 0, "y": 0, "balanced": False},
            "score": 100  # Start perfect, subtract for issues found
        }
        
        self.responsiveness = {
            "viewport_meta": False,
            "breakpoint_violations": [],
            "touch_target_violations": [],
            "image_scaling_issues": [],
            "score": 100  # Start perfect, subtract for issues found
        }
        
        self.accessibility = {
            "missing_alt_text": [],
            "aria_violations": [],
            "semantic_html_issues": [],
            "focus_order_issues": [],
            "score": 100  # Start perfect, subtract for issues found
        }
        
        self.performance = {
            "page_weight": 0,
            "image_optimization": [],
            "meta_tags": [],
            "score": 100  # Start perfect, subtract for issues found
        }


class RuleBasedAnalyzer:
    
    def __init__(self):
        self.soup: Optional[BeautifulSoup] = None
        self.css_rules = []
        self.image_path = None
    
    def _normalize_url(self, url: str) -> str:
        """Normalize URL to handle various formats and ensure it's accessible."""
        try:
            # Add protocol if missing
            if not url.startswith(('http://', 'https://')):
                url = f'https://{url}'
            
            # Parse and validate URL
            parsed = urlparse(url)
            
            # Ensure we have a valid domain
            if not parsed.netloc:
                raise Exception(f"Invalid URL format: {url}")
            
            # Reconstruct URL to ensure proper format
            normalized = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
            if parsed.query:
                normalized += f"?{parsed.query}"
            if parsed.fragment:
                normalized += f"#{parsed.fragment}"
                
            return normalized
            
        except Exception as e:
            raise Exception(f"URL normalization failed for '{url}': {str(e)}")

    async def analyze_html_content(self, url: str) -> Tuple[BeautifulSoup, str]:
        """Fetch and parse HTML content with robust handling for all websites."""
        try:
            # Normalize URL first
            normalized_url = self._normalize_url(url)
            print(f"Analyzing normalized URL: {normalized_url}")
            
            # Configure client to handle redirects, user agents, and various web scenarios
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }
            
            async with httpx.AsyncClient(
                timeout=30.0,
                follow_redirects=True,  # Handle redirects automatically
                max_redirects=10,       # Allow reasonable redirect chains
                headers=headers,
                verify=False           # Handle SSL certificate issues for some sites
            ) as client:
                response = await client.get(normalized_url)
                response.raise_for_status()
                html_content = response.text
                
                # Log the final URL after redirects for debugging
                final_url = str(response.url)
                if final_url != normalized_url:
                    print(f"URL redirected from {normalized_url} to {final_url}")
                
            self.soup = BeautifulSoup(html_content, 'html.parser')
            return self.soup, html_content
            
        except httpx.HTTPStatusError as e:
            raise Exception(f"HTTP error {e.response.status_code} for {url}: {e.response.text[:200]}...")
        except httpx.RequestError as e:
            raise Exception(f"Network error accessing {url}: {str(e)}")
        except Exception as e:
            raise Exception(f"Failed to fetch HTML content from {url}: {str(e)}")
    
    def _extract_css_rules(self, html_content: str) -> List[str]:
        """Extract CSS rules from HTML content."""
        css_rules = []
        
        try:
            if not self.soup:
                return css_rules
                
            # Extract inline styles
            style_tags = self.soup.find_all('style')
            for style in style_tags:
                text_content = self._get_text_safely(style)
                if text_content:
                    css_rules.append(text_content)
            
            # Extract linked stylesheets (basic parsing)
            link_tags = self.soup.find_all('link', {'rel': 'stylesheet'})
            for link in link_tags:
                href = self._get_attribute_safely(link, 'href')
                if href:
                    css_rules.append(f"/* External CSS: {href} */")
            
        except Exception as e:
            print(f"CSS extraction error: {e}")
        
        return css_rules
    
    def _analyze_typography(self, html_content: str) -> Dict[str, Any]:
        """Analyze typography and readability metrics."""
        metrics = {
            "base_font_size": 16,  # Default assumption
            "line_height_ratio": 1.4,  # Default assumption
            "contrast_violations": [],
            "font_fallbacks": [],
            "heading_hierarchy": [],
            "paragraph_lengths": [],
            "score": 100
        }
        
        try:
            if not self.soup:
                return metrics
                
            # Analyze heading hierarchy
            headings = []
            for level in range(1, 7):
                heading_tags = self.soup.find_all(f'h{level}')
                for tag in heading_tags:
                    text_content = self._get_text_safely(tag)
                    if text_content:
                        headings.append({
                            "level": level,
                            "text": text_content[:50],
                            "position": len(headings)
                        })
            
            metrics["heading_hierarchy"] = headings
            
            # Check for proper hierarchy (h1 -> h2 -> h3)
            if headings:
                levels = [h["level"] for h in headings]
                for i in range(len(levels) - 1):
                    if levels[i + 1] > levels[i] + 1:
                        metrics["score"] -= 10
            
            # Analyze paragraph lengths
            paragraphs = self.soup.find_all('p')
            for p in paragraphs:
                text = self._get_text_safely(p)
                if text:
                    char_count = len(text)
                    metrics["paragraph_lengths"].append(char_count)
                    
                    # Penalty for overly long paragraphs (>75 chars per line avg)
                    if char_count > 400:  # Assuming ~75 chars per line * 5 lines
                        metrics["score"] -= 5
            
            # Check for font fallbacks in CSS (basic check)
            css_content = ' '.join(self._extract_css_rules(html_content))
            font_family_matches = re.findall(r'font-family:\s*([^;]+)', css_content, re.IGNORECASE)
            
            for match in font_family_matches:
                fonts = [f.strip().strip('"\'') for f in match.split(',')]
                metrics["font_fallbacks"].append(fonts)
                if len(fonts) < 2:
                    metrics["score"] -= 15
            
            # Ensure score stays within valid range
            metrics["score"] = max(0, min(100, metrics["score"]))
                    
        except Exception as e:
            print(f"Typography analysis error: {e}")
        
        return metrics
    
    def _analyze_colors(self, image_path: str) -> Dict[str, Any]:
        """Analyze color palette and harmony."""
        metrics = {
            "primary_palette": [],
            "harmony_violations": [],
            "saturation_violations": [],
            "contrast_violations": [],
            "color_count": 0,
            "score": 100
        }
        
        try:
            if not Path(image_path).exists():
                return metrics
                
            # Extract dominant colors using ColorThief
            color_thief = ColorThief(image_path)
            palette = color_thief.get_palette(color_count=6, quality=1)
            
            metrics["primary_palette"] = [
                {"rgb": color, "hex": f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"}
                for color in palette
            ]
            metrics["color_count"] = len(palette)
            
            # Check for too many distinct colors
            if len(palette) > 5:
                metrics["score"] -= (len(palette) - 5) * 10
            
            # Analyze saturation (basic check)
            for color in palette:
                r, g, b = color
                max_val = max(r, g, b)
                min_val = min(r, g, b)
                saturation = (max_val - min_val) / max_val if max_val > 0 else 0
                
                if saturation > 0.85:
                    metrics["saturation_violations"].append(color)
                    metrics["score"] -= 15
            
            # Ensure score stays within valid range
            metrics["score"] = max(0, min(100, metrics["score"]))
                    
        except Exception as e:
            print(f"Color analysis error: {e}")
        
        return metrics
    
    def _analyze_layout_whitespace(self, image_path: str) -> Dict[str, Any]:
        """Analyze layout and whitespace using image processing."""
        metrics = {
            "whitespace_ratio": 0,
            "grid_violations": [],
            "section_padding": [],
            "visual_balance": {"x": 0, "y": 0, "balanced": False},
            "score": 100
        }
        
        try:
            if not Path(image_path).exists():
                return metrics
                
            # Load and analyze screenshot
            img = Image.open(image_path)
            width, height = img.size
            
            # Convert to grayscale for analysis
            gray_img = img.convert('L')
            pixels = list(gray_img.getdata())
            
            # Estimate whitespace (simplified - looking for light pixels)
            light_pixels = sum(1 for pixel in pixels if pixel > 240)
            whitespace_ratio = light_pixels / len(pixels)
            
            metrics["whitespace_ratio"] = whitespace_ratio
            
            # Apply scoring based on whitespace ratio
            if whitespace_ratio < 0.3:
                metrics["score"] -= 30
            elif whitespace_ratio > 0.5:
                metrics["score"] -= 15
            
            # Ensure score stays within valid range
            metrics["score"] = max(0, min(100, metrics["score"]))
                
        except Exception as e:
            print(f"Layout analysis error: {e}")
        
        return metrics
    
    def _get_attribute_safely(self, element, attribute: str, default: str = "") -> str:
        """Safely get attribute from BeautifulSoup element."""
        try:
            if hasattr(element, 'get') and callable(getattr(element, 'get')):
                return element.get(attribute, default)
            return default
        except Exception:
            return default
    
    def _get_text_safely(self, element, default: str = "") -> str:
        """Safely get text from BeautifulSoup element."""
        try:
            if hasattr(element, 'get_text') and callable(getattr(element, 'get_text')):
                return element.get_text().strip()
            return default
        except Exception:
            return default
    
    def _analyze_responsiveness(self) -> Dict[str, Any]:
        """Analyze responsiveness indicators with modern web standards."""
        metrics = {
            "viewport_meta": False,
            "breakpoint_violations": [],
            "touch_target_violations": [],
            "image_scaling_issues": [],
            "score": 100
        }
        
        try:
            if not self.soup:
                return metrics
                
            # Check for viewport meta tag
            viewport_meta = self.soup.find('meta', {'name': 'viewport'})
            metrics["viewport_meta"] = viewport_meta is not None
            
            if not viewport_meta:
                metrics["score"] -= 25
            
            # Modern approach to image analysis - focus on critical issues only
            img_tags = self.soup.find_all('img')
            critical_issues = 0
            
            for img in img_tags:
                src = self._get_attribute_safely(img, 'src')
                
                # Skip non-critical images
                if (not src or 
                    src.startswith('data:') or 
                    any(keyword in src.lower() for keyword in ['icon', 'logo', 'sprite', '.svg']) or
                    src.startswith('//')):
                    continue
                
                # Check for responsive attributes
                srcset = self._get_attribute_safely(img, 'srcset')
                style = self._get_attribute_safely(img, 'style') or ''
                classes = self._get_attribute_safely(img, 'class') or ''
                
                # Modern responsive indicators
                has_responsive = any([
                    srcset,
                    'width:100%' in style,
                    'max-width:100%' in style,
                    'width: 100%' in style,
                    'responsive' in classes.lower(),
                    'img-responsive' in classes.lower(),
                    'img-fluid' in classes.lower()
                ])
                
                if not has_responsive:
                    metrics["image_scaling_issues"].append({
                        "src": src[:100] + '...' if len(src) > 100 else src,
                        "alt": self._get_attribute_safely(img, 'alt')
                    })
                    critical_issues += 1
            
            # Much more reasonable penalty system
            if critical_issues > 0:
                # Only penalize if there are many critical issues
                if critical_issues > 5:
                    penalty = min(15, critical_issues)  # Max 15 points penalty
                    metrics["score"] -= penalty
            
            # Ensure score doesn't go below 0
            metrics["score"] = max(0, metrics["score"])
                    
        except Exception as e:
            print(f"Responsiveness analysis error: {e}")
        
        return metrics
    
    def _analyze_accessibility(self) -> Dict[str, Any]:
        """Analyze accessibility indicators with modern web standards."""
        metrics = {
            "missing_alt_text": [],
            "aria_violations": [],
            "semantic_html_issues": [],
            "focus_order_issues": [],
            "score": 100
        }
        
        try:
            if not self.soup:
                return metrics
                
            # Check for missing alt text on content images only
            img_tags = self.soup.find_all('img')
            missing_alt = 0
            
            for img in img_tags:
                src = self._get_attribute_safely(img, 'src')
                alt_text = self._get_attribute_safely(img, 'alt')
                
                # Skip decorative images and icons (be more generous)
                if (not src or 
                    src.startswith('data:') or 
                    any(keyword in src.lower() for keyword in ['icon', 'logo', 'sprite', '.svg', 'button', 'arrow', 'chevron']) or
                    src.startswith('//')):
                    continue
                
                # Check if it's likely a decorative image by size or CSS
                parent = img.parent if img.parent else None
                if parent:
                    parent_class = parent.get('class') or []
                    if any(keyword in str(parent_class).lower() for keyword in ['icon', 'decoration', 'background']):
                        continue
                
                if not alt_text:
                    metrics["missing_alt_text"].append(src[:50] + '...' if len(src) > 50 else src)
                    missing_alt += 1
            
            # Much more reasonable penalty for missing alt text
            if missing_alt > 3:  # Only penalize if many content images are missing alt
                penalty = min(missing_alt * 2, 15)  # 2 points per missing alt, max 15
                metrics["score"] -= penalty
            
            # Check for semantic HTML (be more lenient)
            semantic_penalty = 0
            
            # Main is most important
            if not self.soup.find('main'):
                metrics["semantic_html_issues"].append("Missing main tag")
                semantic_penalty += 10
            
            # Header and footer are nice to have but not critical
            if not self.soup.find('header'):
                metrics["semantic_html_issues"].append("Missing header tag")
                semantic_penalty += 5
                
            if not self.soup.find('footer'):
                metrics["semantic_html_issues"].append("Missing footer tag")
                semantic_penalty += 5
            
            # Navigation is good for accessibility
            if not self.soup.find('nav'):
                metrics["semantic_html_issues"].append("Missing nav tag")
                semantic_penalty += 3
            
            # Apply penalty instead of negative addition
            metrics["score"] -= semantic_penalty
            
            # Check for ARIA labels on buttons (be very selective)
            aria_violations = 0
            buttons = self.soup.find_all('button')  # Only actual buttons
            
            for button in buttons:
                aria_label = self._get_attribute_safely(button, 'aria-label')
                button_text = self._get_text_safely(button).strip()
                
                # Only flag if it's a critical button with no text or label
                if not (aria_label or button_text) and len(button_text) == 0:
                    metrics["aria_violations"].append("Button without label")
                    aria_violations += 1
            
            # Very small penalty for ARIA violations
            if aria_violations > 2:
                penalty = min(aria_violations * 3, 10)  # 3 points per violation, max 10
                metrics["score"] -= penalty
            
            # Ensure score doesn't go below 0
            metrics["score"] = max(0, metrics["score"])
                    
        except Exception as e:
            print(f"Accessibility analysis error: {e}")
        
        return metrics
    
    async def analyze(self, url: str, screenshot_path: str) -> DesignMetrics:
        """Perform comprehensive rule-based analysis with robust error handling."""
        try:
            # Fetch and parse HTML
            soup, html_content = await self.analyze_html_content(url)
            self.image_path = screenshot_path
            
            # Create metrics container
            metrics = DesignMetrics()
            
            # Run all analyses with strict error handling - no fallbacks
            failed_analyses = []
            
            try:
                metrics.typography = self._analyze_typography(html_content)
            except Exception as e:
                print(f"Typography analysis failed: {e}")
                failed_analyses.append(f"Typography: {str(e)}")
            
            try:
                metrics.color = self._analyze_colors(screenshot_path)
            except Exception as e:
                print(f"Color analysis failed: {e}")
                failed_analyses.append(f"Color: {str(e)}")
            
            try:
                metrics.layout = self._analyze_layout_whitespace(screenshot_path)
            except Exception as e:
                print(f"Layout analysis failed: {e}")
                failed_analyses.append(f"Layout: {str(e)}")
            
            try:
                metrics.responsiveness = self._analyze_responsiveness()
            except Exception as e:
                print(f"Responsiveness analysis failed: {e}")
                failed_analyses.append(f"Responsiveness: {str(e)}")
            
            try:
                metrics.accessibility = self._analyze_accessibility()
            except Exception as e:
                print(f"Accessibility analysis failed: {e}")
                failed_analyses.append(f"Accessibility: {str(e)}")
            
            # If multiple core analyses failed, fail the entire analysis
            if len(failed_analyses) >= 3:
                raise Exception(f"Critical analysis failure - multiple components failed: {'; '.join(failed_analyses)}")
            
            # If some analyses failed, log but continue (partial results are still valuable)
            if failed_analyses:
                print(f"Partial analysis - some components failed: {'; '.join(failed_analyses)}")
            
            return metrics
            
        except Exception as e:
            # If we can't even fetch the HTML, this is a critical failure
            raise Exception(f"Critical analysis failure for {url}: {str(e)}")


class OllamaClient:
    """Client for Ollama LLM integration - Vision Analysis Only."""
    
    def __init__(self):
        self.base_url = settings.ollama_base_url
        self.model = settings.ollama_model
        self.timeout = settings.ollama_timeout
    
    async def check_health(self) -> bool:
        """Check if Ollama is available and the model is loaded."""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                # Check if Ollama is running
                response = await client.get(f"{self.base_url}/api/tags")
                if response.status_code != 200:
                    print(f"Ollama API not responding: {response.status_code}")
                    return False
                
                # Check if our model is available
                models = response.json()
                model_names = [model['name'] for model in models.get('models', [])]
                
                if self.model not in model_names:
                    print(f"Model {self.model} not found. Available models: {model_names}")
                    print(f"You may need to pull the model: docker exec website_scorer_ollama ollama pull {self.model}")
                    return False
                
                print(f"Ollama health check passed. Model {self.model} is available.")
                return True
                
        except Exception as e:
            print(f"Ollama health check failed: {e}")
            return False
    
    def _encode_image_base64(self, image_path: str) -> str:
        """Encode image to base64 for vision models with validation and optimization."""
        try:
            # Verify file exists and is readable
            if not Path(image_path).exists():
                raise Exception(f"Screenshot file not found: {image_path}")
            
            # Check file size (should be reasonable for a screenshot)
            file_size = Path(image_path).stat().st_size
            if file_size == 0:
                raise Exception("Screenshot file is empty")
            if file_size > 10 * 1024 * 1024:  # 10MB limit
                raise Exception("Screenshot file too large for vision analysis")
            
            # OPTIMIZATION: Resize image if too large to reduce processing time
            if file_size > 2 * 1024 * 1024:  # 2MB threshold
                print(f"Large image detected ({file_size} bytes), resizing for faster processing")
                # Open, resize, and compress the image
                with Image.open(image_path) as img:
                    # Resize to max 1920x1080 while maintaining aspect ratio
                    img.thumbnail((1920, 1080), Image.Resampling.LANCZOS)
                    
                    # Save to temporary compressed version
                    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
                        img.save(temp_file.name, 'JPEG', quality=85, optimize=True)
                        image_path = temp_file.name
                
            # Read and validate image
            with open(image_path, "rb") as image_file:
                image_data = image_file.read()
                
            # Verify it's a valid image by checking headers
            if not (image_data.startswith(b'\x89PNG') or 
                   image_data.startswith(b'\xff\xd8\xff') or
                   image_data.startswith(b'RIFF')):
                raise Exception("File is not a valid image format")
            
            # Encode to base64
            encoded = base64.b64encode(image_data).decode('utf-8')
            
            # Verify encoding worked
            if not encoded or len(encoded) < 100:
                raise Exception("Image encoding failed or produced invalid result")
                
            print(f"Successfully encoded image: {len(encoded)} characters, {len(image_data)} bytes")
            return encoded
            
        except Exception as e:
            print(f"Image encoding error for {image_path}: {e}")
            raise Exception(f"Failed to prepare screenshot for vision analysis: {str(e)}")
    
    async def generate_vision_analysis(self, prompt: str, image_path: str, analysis_type: str = "pdf_report") -> str:
        """Generate analysis using Ollama vision model with image - OPTIMIZED FOR COMPREHENSIVE ANALYSIS."""
        vision_start = datetime.now()
        
        # Get configuration for this analysis type
        config = PromptConfig.get_token_limit(analysis_type)
        min_length = PromptConfig.get_min_length(analysis_type)
        
        try:
            print(f"Starting vision analysis with image: {image_path} (type: {analysis_type}, max_tokens: {config})")
            
            # Encode image to base64 with validation and optimization
            encoding_start = datetime.now()
            image_base64 = self._encode_image_base64(image_path)
            encoding_time = (datetime.now() - encoding_start).total_seconds()
            print(f"Image encoding completed in {encoding_time:.2f}s")
            
            # Prepare payload for vision model - OPTIMIZED FOR FAST, CONCISE RESPONSES
            payload = {
                "model": self.model,
                "prompt": prompt,
                "images": [image_base64],
                "stream": False,
                "options": {
                    "temperature": 0.2,   # Slightly higher for more natural shorter responses
                    "num_predict": config,  # Use configured token limit (now much lower)
                    "top_p": 0.9,         # Higher for more diverse but focused responses
                    "repeat_penalty": 1.15, # Higher penalty to avoid repetition in short responses
                    "num_ctx": 2048,      # Smaller context window for faster processing
                    "num_gpu": 1,         # Force GPU usage
                    "num_thread": 6,      # Fewer threads for better GPU utilization
                    "use_mmap": True,     # Memory mapping for speed
                    "use_mlock": True     # Lock model in memory
                }
            }
            
            print(f"Sending vision request to {self.base_url}/api/generate with model {self.model}")
            
            # Track API call time separately
            api_start = datetime.now()
            async with httpx.AsyncClient(timeout=httpx.Timeout(connect=30.0, read=180.0, write=30.0, pool=30.0)) as client:
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json=payload
                )
                
                # Check response status
                if response.status_code != 200:
                    raise Exception(f"Ollama API returned status {response.status_code}: {response.text}")
                
                result = response.json()
            
            api_time = (datetime.now() - api_start).total_seconds()
            print(f"Ollama API call completed in {api_time:.2f}s")
                
            # Validate response structure
            if "response" not in result:
                raise Exception(f"Invalid response from Ollama: {result}")
            
            analysis_content = result.get("response", "").strip()
            
            # Verify the LLM actually processed the image and gave meaningful analysis
            if not analysis_content:
                raise Exception("Vision model returned empty response - may not be processing the screenshot")
            
            if len(analysis_content) < min_length:  # Use configured minimum length
                raise Exception(f"Vision model returned insufficient analysis ({len(analysis_content)} chars, expected {min_length}+) - may not be seeing the screenshot properly")
            
            # Check if response contains vision-specific observations
            vision_indicators = [
                "see", "visible", "visual", "screenshot", "image", "display", 
                "color", "layout", "text", "button", "navigation", "design"
            ]
            
            if not any(indicator in analysis_content.lower() for indicator in vision_indicators):
                raise Exception("Vision analysis doesn't contain visual observations - LLM may not be processing the screenshot")
            
            total_time = (datetime.now() - vision_start).total_seconds()
            print(f"Vision analysis successful: {len(analysis_content)} characters in {total_time:.2f}s (encoding: {encoding_time:.2f}s, API: {api_time:.2f}s)")
            return analysis_content
                
        except Exception as e:
            total_time = (datetime.now() - vision_start).total_seconds()
            print(f"Vision analysis failed for {image_path} after {total_time:.2f}s: {str(e)}")
            raise Exception(f"AI vision analysis failed: {str(e)}")


class AIAnalysisService:
    """Main AI analysis service coordinating rule-based and LLM analysis."""
    
    def __init__(self):
        self.rule_analyzer = RuleBasedAnalyzer()
        self.ollama_client = OllamaClient()
        self.rules_content = self._load_rules()
        self.prompt_service = VisionAnalysisPrompts()
    
    def _load_rules(self) -> str:
        """Load custom rules from rules.md file."""
        try:
            rules_path = Path(__file__).parent.parent.parent.parent / "rules.md"
            if rules_path.exists():
                return rules_path.read_text(encoding='utf-8')
            return ""
        except Exception as e:
            print(f"Failed to load rules: {e}")
            return ""
    
    async def analyze_website_design(
        self, 
        url: str, 
        screenshot_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Perform comprehensive website design analysis.
        
        Args:
            url: Website URL to analyze
            screenshot_data: Screenshot data from ScreenshotService
            
        Returns:
            Complete analysis results with scores and recommendations
        """
        try:
            analysis_start = get_colombia_time()
            
            # Get screenshot path (prefer desktop)
            screenshot_path = ""
            if screenshot_data.get("desktop"):
                screenshot_path = screenshot_data["desktop"]["local_path"]
            elif screenshot_data.get("mobile"):
                screenshot_path = screenshot_data["mobile"]["local_path"]
            else:
                raise Exception("No valid screenshot data provided")
            
            # Step 1: Rule-based analysis
            print(f"Starting rule-based analysis for {url}")
            metrics = await self.rule_analyzer.analyze(url, screenshot_path)
            
            # Step 2: Calculate overall rule-based score
            rule_scores = [
                metrics.typography["score"],
                metrics.color["score"], 
                metrics.layout["score"],
                metrics.responsiveness["score"],
                metrics.accessibility["score"]
            ]
            
            # Apply weights from configuration
            weights = weights_config.get_weights()
            
            weighted_score = (
                metrics.typography["score"] * weights["typography"] +
                metrics.color["score"] * weights["color"] +
                metrics.layout["score"] * weights["layout"] +
                metrics.responsiveness["score"] * weights["responsiveness"] +
                metrics.accessibility["score"] * weights["accessibility"]
            )
            
            # Step 3: LLM Vision Analysis - CORE FEATURE (must see screenshots)
            llm_analysis = ""
            llm_error = None
            
            try:
                # REQUIRE desktop screenshot for vision analysis - this is our main feature
                desktop_screenshot_path = screenshot_data.get("desktop", {}).get("local_path")
                
                if not desktop_screenshot_path or not Path(desktop_screenshot_path).exists():
                    raise Exception("Screenshot required for AI vision analysis but not available")
                
                # Verify the screenshot file is valid and readable
                try:
                    with open(desktop_screenshot_path, 'rb') as f:
                        # Read first few bytes to verify it's a valid image
                        header = f.read(10)
                        if not (header.startswith(b'\x89PNG') or header.startswith(b'\xff\xd8\xff')):
                            raise Exception("Invalid or corrupted screenshot file")
                except Exception as img_err:
                    raise Exception(f"Screenshot file is not readable or corrupted: {str(img_err)}")
                
                # First check if Ollama and model are available
                if not await self.ollama_client.check_health():
                    raise Exception("AI vision analysis service is currently unavailable. Please ensure Ollama is running and the model is loaded.")
                
                # COMPREHENSIVE VISION ANALYSIS FOR PDF REPORTS
                print(f"Starting professional design analysis for {url} with screenshot: {desktop_screenshot_path}")
                prompt = self.prompt_service.create_pdf_report_prompt(url, metrics)
                llm_analysis = await self.ollama_client.generate_vision_analysis(
                    prompt, desktop_screenshot_path, analysis_type="pdf_report"
                )
                
                # Verify we got meaningful analysis content
                min_expected_length = PromptConfig.get_min_length("pdf_report")
                if not llm_analysis or len(llm_analysis.strip()) < min_expected_length:
                    raise Exception(f"Vision analysis returned insufficient content ({len(llm_analysis.strip()) if llm_analysis else 0} chars, expected {min_expected_length}+) - AI may not be seeing the screenshot properly")
                    
            except Exception as e:
                llm_error = str(e)
                print(f"LLM vision analysis failed: {e}")
                # No fallbacks - vision analysis is our core feature and must work
            
            # Step 4: Compile final results - ONLY if vision analysis succeeded
            if llm_error:
                # Vision analysis failed - this is our core feature, so fail the entire analysis
                raise Exception(f"Vision analysis is required but failed: {llm_error}")
            
            # Get score category for overall assessment
            score_category = weights_config.get_score_category(weighted_score)
            
            analysis_result = {
                "analysis_id": f"analysis_{int(analysis_start.timestamp())}",
                "url": url,
                "analyzed_at": format_colombia_time_short(analysis_start),
                "analysis_duration": (get_colombia_time() - analysis_start).total_seconds(),
                "status": "completed",
                
                # Main Scores for Report Header
                "overall_score": round(weighted_score, 1),
                "score_category": score_category,
                "score_grade": self._get_score_grade(weighted_score),
                "scores_breakdown": {
                    "typography": round(metrics.typography["score"], 1),
                    "color": round(metrics.color["score"], 1),
                    "layout": round(metrics.layout["score"], 1),
                    "responsiveness": round(metrics.responsiveness["score"], 1),
                    "accessibility": round(metrics.accessibility["score"], 1)
                },
                
                # Report Summary for Executive Overview
                "report_summary": {
                    "website_title": screenshot_data.get("desktop", {}).get("page_metrics", {}).get("title", "Unknown"),
                    "evaluation_date": analysis_start.strftime("%B %d, %Y"),
                    "evaluation_time": analysis_start.strftime("%I:%M %p"),
                    "total_issues_found": self._count_total_issues(metrics),
                    "critical_issues": self._get_critical_issues(metrics),
                    "strengths": self._get_strengths(metrics),
                    "improvement_areas": self._get_improvement_areas(metrics)
                },
                
                # Detailed Analysis for Each Category
                "detailed_analysis": {
                    "typography": {
                        "score": round(metrics.typography["score"], 1),
                        "grade": self._get_score_grade(metrics.typography["score"]),
                        "summary": self._get_typography_summary(metrics.typography),
                        "issues": self._get_typography_issues(metrics.typography),
                        "recommendations": self._get_typography_recommendations(metrics.typography)
                    },
                    "color": {
                        "score": round(metrics.color["score"], 1),
                        "grade": self._get_score_grade(metrics.color["score"]),
                        "summary": self._get_color_summary(metrics.color),
                        "issues": self._get_color_issues(metrics.color),
                        "recommendations": self._get_color_recommendations(metrics.color)
                    },
                    "layout": {
                        "score": round(metrics.layout["score"], 1),
                        "grade": self._get_score_grade(metrics.layout["score"]),
                        "summary": self._get_layout_summary(metrics.layout),
                        "issues": self._get_layout_issues(metrics.layout),
                        "recommendations": self._get_layout_recommendations(metrics.layout)
                    },
                    "responsiveness": {
                        "score": round(metrics.responsiveness["score"], 1),
                        "grade": self._get_score_grade(metrics.responsiveness["score"]),
                        "summary": self._get_responsiveness_summary(metrics.responsiveness),
                        "issues": self._get_responsiveness_issues(metrics.responsiveness),
                        "recommendations": self._get_responsiveness_recommendations(metrics.responsiveness)
                    },
                    "accessibility": {
                        "score": round(metrics.accessibility["score"], 1),
                        "grade": self._get_score_grade(metrics.accessibility["score"]),
                        "summary": self._get_accessibility_summary(metrics.accessibility),
                        "issues": self._get_accessibility_issues(metrics.accessibility),
                        "recommendations": self._get_accessibility_recommendations(metrics.accessibility)
                    }
                },
                
                # Raw Metrics for Technical Details
                "rule_based_metrics": {
                    "typography": metrics.typography,
                    "color": metrics.color,
                    "layout": metrics.layout,
                    "responsiveness": metrics.responsiveness,
                    "accessibility": metrics.accessibility
                },
                
                # AI Vision Analysis
                "llm_analysis": {
                    "content": llm_analysis,
                    "error": None,
                    "model_used": self.ollama_client.model,
                    "vision_analysis": True
                },
                
                # Screenshots for Report
                "screenshots": screenshot_data,
                
                # Configuration & Metadata
                "weights_applied": weights,
                "rules_version": weights_config.get_version(),
                "thresholds": weights_config.get_thresholds()
            }
            
            return analysis_result
            
        except Exception as e:
            # Proper error handling - no fallback responses
            print(f"Analysis failed for {url}: {str(e)}")
            raise Exception(f"We're experiencing technical issues with our analysis service. Please try again later.")

    def _get_score_grade(self, score: float) -> str:
        """Convert numeric score to letter grade."""
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "F"
    
    def _count_total_issues(self, metrics) -> int:
        """Count total issues across all categories."""
        total = 0
        total += len(metrics.typography.get("contrast_violations", []))
        total += len(metrics.color.get("harmony_violations", []))
        total += len(metrics.layout.get("grid_violations", []))
        total += len(metrics.responsiveness.get("touch_target_violations", []))
        total += len(metrics.accessibility.get("missing_alt_text", []))
        total += len(metrics.accessibility.get("aria_violations", []))
        return total
    
    def _get_critical_issues(self, metrics) -> list:
        """Get list of critical issues that need immediate attention."""
        issues = []
        
        # Accessibility issues are critical
        if len(metrics.accessibility.get("missing_alt_text", [])) > 5:
            issues.append("Multiple images missing alt text")
        if len(metrics.accessibility.get("aria_violations", [])) > 0:
            issues.append("ARIA accessibility violations detected")
        
        # Responsiveness issues
        if len(metrics.responsiveness.get("image_scaling_issues", [])) > 10:
            issues.append("Significant mobile responsiveness problems")
        
        # Low scores
        if metrics.accessibility["score"] < 30:
            issues.append("Poor accessibility compliance")
        if metrics.responsiveness["score"] < 30:
            issues.append("Poor mobile experience")
        
        return issues
    
    def _get_strengths(self, metrics) -> list:
        """Identify design strengths."""
        strengths = []
        
        if metrics.typography["score"] >= 80:
            strengths.append("Excellent typography and readability")
        if metrics.color["score"] >= 80:
            strengths.append("Good color scheme and harmony")
        if metrics.layout["score"] >= 80:
            strengths.append("Well-structured layout and spacing")
        if metrics.accessibility["score"] >= 80:
            strengths.append("Good accessibility compliance")
        if metrics.responsiveness["score"] >= 80:
            strengths.append("Mobile-friendly design")
        
        return strengths if strengths else ["Basic functionality is working"]
    
    def _get_improvement_areas(self, metrics) -> list:
        """Identify areas needing improvement."""
        areas = []
        
        if metrics.typography["score"] < 70:
            areas.append("Typography and text readability")
        if metrics.color["score"] < 70:
            areas.append("Color scheme and visual harmony")
        if metrics.layout["score"] < 70:
            areas.append("Layout structure and spacing")
        if metrics.accessibility["score"] < 70:
            areas.append("Accessibility compliance")
        if metrics.responsiveness["score"] < 70:
            areas.append("Mobile responsiveness")
        
        return areas
    
    # Typography helper methods
    def _get_typography_summary(self, typography_metrics: dict) -> str:
        """Generate typography analysis summary."""
        score = typography_metrics["score"]
        if score >= 90:
            return "Excellent typography with clear hierarchy and readability"
        elif score >= 70:
            return "Good typography with minor areas for improvement"
        else:
            return "Typography needs significant improvement for better readability"
    
    def _get_typography_issues(self, typography_metrics: dict) -> list:
        """Get typography issues."""
        issues = []
        if len(typography_metrics.get("contrast_violations", [])) > 0:
            issues.append(f"{len(typography_metrics['contrast_violations'])} text contrast violations")
        if typography_metrics.get("base_font_size", 16) < 14:
            issues.append("Font size too small for readability")
        return issues
    
    def _get_typography_recommendations(self, typography_metrics: dict) -> list:
        """Get typography recommendations."""
        recs = []
        if len(typography_metrics.get("contrast_violations", [])) > 0:
            recs.append("Improve text contrast ratios for better readability")
        if typography_metrics.get("base_font_size", 16) < 16:
            recs.append("Increase base font size to at least 16px")
        if not recs:
            recs.append("Typography is well-implemented")
        return recs
    
    # Color helper methods
    def _get_color_summary(self, color_metrics: dict) -> str:
        """Generate color analysis summary."""
        score = color_metrics["score"]
        if score >= 90:
            return "Excellent color scheme with great harmony and accessibility"
        elif score >= 70:
            return "Good color usage with room for minor improvements"
        else:
            return "Color scheme needs improvement for better visual appeal"
    
    def _get_color_issues(self, color_metrics: dict) -> list:
        """Get color issues."""
        issues = []
        if color_metrics.get("color_count", 0) > 8:
            issues.append("Too many colors used, may appear cluttered")
        if len(color_metrics.get("contrast_violations", [])) > 0:
            issues.append("Color contrast issues detected")
        return issues
    
    def _get_color_recommendations(self, color_metrics: dict) -> list:
        """Get color recommendations."""
        recs = []
        if color_metrics.get("color_count", 0) > 6:
            recs.append("Reduce color palette to 5-6 main colors for better cohesion")
        if len(color_metrics.get("contrast_violations", [])) > 0:
            recs.append("Improve color contrast for accessibility compliance")
        if not recs:
            recs.append("Color scheme is well-balanced")
        return recs
    
    # Layout helper methods
    def _get_layout_summary(self, layout_metrics: dict) -> str:
        """Generate layout analysis summary."""
        score = layout_metrics["score"]
        if score >= 90:
            return "Excellent layout with proper spacing and visual hierarchy"
        elif score >= 70:
            return "Good layout structure with some areas for refinement"
        else:
            return "Layout needs significant improvement for better user experience"
    
    def _get_layout_issues(self, layout_metrics: dict) -> list:
        """Get layout issues."""
        issues = []
        if layout_metrics.get("whitespace_ratio", 0) < 0.3:
            issues.append("Insufficient whitespace, layout appears cramped")
        if not layout_metrics.get("visual_balance", {}).get("balanced", True):
            issues.append("Visual elements appear unbalanced")
        return issues
    
    def _get_layout_recommendations(self, layout_metrics: dict) -> list:
        """Get layout recommendations."""
        recs = []
        if layout_metrics.get("whitespace_ratio", 0) < 0.3:
            recs.append("Add more whitespace to improve visual breathing room")
        if len(layout_metrics.get("grid_violations", [])) > 0:
            recs.append("Improve grid alignment for more professional appearance")
        if not recs:
            recs.append("Layout structure is well-organized")
        return recs
    
    # Responsiveness helper methods
    def _get_responsiveness_summary(self, resp_metrics: dict) -> str:
        """Generate responsiveness analysis summary."""
        score = resp_metrics["score"]
        if score >= 90:
            return "Excellent mobile responsiveness and cross-device compatibility"
        elif score >= 70:
            return "Good responsive design with minor mobile optimizations needed"
        else:
            return "Poor mobile experience requiring significant responsive improvements"
    
    def _get_responsiveness_issues(self, resp_metrics: dict) -> list:
        """Get responsiveness issues."""
        issues = []
        if not resp_metrics.get("viewport_meta", False):
            issues.append("Missing viewport meta tag")
        scaling_issues = len(resp_metrics.get("image_scaling_issues", []))
        if scaling_issues > 5:
            issues.append(f"{scaling_issues} images with scaling problems")
        return issues
    
    def _get_responsiveness_recommendations(self, resp_metrics: dict) -> list:
        """Get responsiveness recommendations."""
        recs = []
        if not resp_metrics.get("viewport_meta", False):
            recs.append("Add proper viewport meta tag for mobile compatibility")
        if len(resp_metrics.get("image_scaling_issues", [])) > 0:
            recs.append("Optimize images for responsive scaling")
        if len(resp_metrics.get("touch_target_violations", [])) > 0:
            recs.append("Increase touch target sizes for better mobile usability")
        if not recs:
            recs.append("Responsive design is well-implemented")
        return recs
    
    # Accessibility helper methods
    def _get_accessibility_summary(self, a11y_metrics: dict) -> str:
        """Generate accessibility analysis summary."""
        score = a11y_metrics["score"]
        if score >= 90:
            return "Excellent accessibility compliance with inclusive design"
        elif score >= 70:
            return "Good accessibility with some areas for improvement"
        else:
            return "Poor accessibility requiring immediate attention for compliance"
    
    def _get_accessibility_issues(self, a11y_metrics: dict) -> list:
        """Get accessibility issues."""
        issues = []
        missing_alt = len(a11y_metrics.get("missing_alt_text", []))
        if missing_alt > 0:
            issues.append(f"{missing_alt} images missing alt text")
        aria_violations = len(a11y_metrics.get("aria_violations", []))
        if aria_violations > 0:
            issues.append(f"{aria_violations} ARIA violations")
        return issues
    
    def _get_accessibility_recommendations(self, a11y_metrics: dict) -> list:
        """Get accessibility recommendations."""
        recs = []
        if len(a11y_metrics.get("missing_alt_text", [])) > 0:
            recs.append("Add descriptive alt text to all images")
        if len(a11y_metrics.get("aria_violations", [])) > 0:
            recs.append("Fix ARIA violations for screen reader compatibility")
        if len(a11y_metrics.get("semantic_html_issues", [])) > 0:
            recs.append("Improve semantic HTML structure")
        if not recs:
            recs.append("Accessibility implementation is compliant")
        return recs


# Global service instance
ai_analysis_service = AIAnalysisService()
