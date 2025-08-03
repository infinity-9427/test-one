
import asyncio
import base64
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from urllib.parse import urljoin, urlparse

import httpx
from bs4 import BeautifulSoup
from colorthief import ColorThief
from PIL import Image

from ..core.settings import settings
from .prompts import VisionAnalysisPrompts


class DesignMetrics:
    
    def __init__(self):
        self.typography = {
            "base_font_size": 16,
            "line_height_ratio": 1.4,
            "contrast_violations": [],
            "font_fallbacks": [],
            "heading_hierarchy": [],
            "paragraph_lengths": [],
            "score": 70  # Default moderate score
        }
        
        self.color = {
            "primary_palette": [],
            "harmony_violations": [],
            "saturation_violations": [],
            "contrast_violations": [],
            "color_count": 0,
            "score": 70  # Default moderate score
        }
        
        self.layout = {
            "whitespace_ratio": 0.3,  # Reasonable default
            "grid_violations": [],
            "section_padding": [],
            "visual_balance": {"x": 0, "y": 0, "balanced": False},
            "score": 70  # Default moderate score
        }
        
        self.responsiveness = {
            "viewport_meta": False,
            "breakpoint_violations": [],
            "touch_target_violations": [],
            "image_scaling_issues": [],
            "score": 70  # Default moderate score
        }
        
        self.accessibility = {
            "missing_alt_text": [],
            "aria_violations": [],
            "semantic_html_issues": [],
            "focus_order_issues": [],
            "score": 70  # Default moderate score
        }
        
        self.performance = {
            "page_weight": 0,
            "image_optimization": [],
            "meta_tags": [],
            "score": 70  # Default moderate score
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
        """Analyze responsiveness indicators."""
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
            
            # Check for responsive images
            img_tags = self.soup.find_all('img')
            for img in img_tags:
                srcset = self._get_attribute_safely(img, 'srcset')
                style = self._get_attribute_safely(img, 'style')
                
                if not (srcset or 'width:100%' in style):
                    metrics["image_scaling_issues"].append({
                        "src": self._get_attribute_safely(img, 'src'),
                        "alt": self._get_attribute_safely(img, 'alt')
                    })
                    metrics["score"] -= 20
                    
        except Exception as e:
            print(f"Responsiveness analysis error: {e}")
        
        return metrics
    
    def _analyze_accessibility(self) -> Dict[str, Any]:
        """Analyze accessibility indicators."""
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
                
            # Check for missing alt text
            img_tags = self.soup.find_all('img')
            for img in img_tags:
                alt_text = self._get_attribute_safely(img, 'alt')
                if not alt_text:
                    src = self._get_attribute_safely(img, 'src', 'unknown')
                    metrics["missing_alt_text"].append(src)
                    metrics["score"] -= 10
            
            # Check for semantic HTML
            required_semantic = ['header', 'main', 'footer']
            for tag in required_semantic:
                if not self.soup.find(tag):
                    metrics["semantic_html_issues"].append(f"Missing {tag} tag")
                    metrics["score"] -= 20
            
            # Check for ARIA labels on buttons
            buttons = self.soup.find_all(['button', 'a'])
            for button in buttons:
                aria_label = self._get_attribute_safely(button, 'aria-label')
                button_text = self._get_text_safely(button)
                
                if not (aria_label or button_text):
                    metrics["aria_violations"].append("Button without label")
                    metrics["score"] -= 15
                    
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
            
            # Run all analyses with individual error handling
            try:
                metrics.typography = self._analyze_typography(html_content)
            except Exception as e:
                print(f"Typography analysis failed: {e}, using defaults")
                metrics.typography = {"score": 50, "error": str(e)}
            
            try:
                metrics.color = self._analyze_colors(screenshot_path)
            except Exception as e:
                print(f"Color analysis failed: {e}, using defaults")
                metrics.color = {"score": 50, "error": str(e)}
            
            try:
                metrics.layout = self._analyze_layout_whitespace(screenshot_path)
            except Exception as e:
                print(f"Layout analysis failed: {e}, using defaults")
                metrics.layout = {"score": 50, "error": str(e)}
            
            try:
                metrics.responsiveness = self._analyze_responsiveness()
            except Exception as e:
                print(f"Responsiveness analysis failed: {e}, using defaults")
                metrics.responsiveness = {"score": 50, "error": str(e)}
            
            try:
                metrics.accessibility = self._analyze_accessibility()
            except Exception as e:
                print(f"Accessibility analysis failed: {e}, using defaults")
                metrics.accessibility = {"score": 50, "error": str(e)}
            
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
        """Check if Ollama is available."""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.base_url}/api/tags")
                return response.status_code == 200
        except Exception:
            return False
    
    def _encode_image_base64(self, image_path: str) -> str:
        """Encode image to base64 for vision models with validation."""
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
                
            print(f"Successfully encoded image: {len(encoded)} characters, {file_size} bytes")
            return encoded
            
        except Exception as e:
            print(f"Image encoding error for {image_path}: {e}")
            raise Exception(f"Failed to prepare screenshot for vision analysis: {str(e)}")
    
    async def generate_vision_analysis(self, prompt: str, image_path: str, max_tokens: int = 1000) -> str:
        """Generate analysis using Ollama vision model with image - CORE FEATURE."""
        try:
            print(f"Starting vision analysis with image: {image_path}")
            
            # Encode image to base64 with validation
            image_base64 = self._encode_image_base64(image_path)
            
            # Prepare payload for vision model
            payload = {
                "model": self.model,
                "prompt": prompt,
                "images": [image_base64],
                "stream": False,
                "options": {
                    "temperature": 0.3,
                    "num_predict": max_tokens,
                    "top_p": 0.9,
                    "repeat_penalty": 1.1
                }
            }
            
            print(f"Sending vision request to {self.base_url}/api/generate with model {self.model}")
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json=payload
                )
                
                # Check response status
                if response.status_code != 200:
                    raise Exception(f"Ollama API returned status {response.status_code}: {response.text}")
                
                result = response.json()
                
                # Validate response structure
                if "response" not in result:
                    raise Exception(f"Invalid response from Ollama: {result}")
                
                analysis_content = result.get("response", "").strip()
                
                # Verify the LLM actually processed the image and gave meaningful analysis
                if not analysis_content:
                    raise Exception("Vision model returned empty response - may not be processing the screenshot")
                
                if len(analysis_content) < 100:
                    raise Exception("Vision model returned insufficient analysis - may not be seeing the screenshot properly")
                
                # Check if response contains vision-specific observations
                vision_indicators = [
                    "see", "visible", "visual", "screenshot", "image", "display", 
                    "color", "layout", "text", "button", "navigation", "design"
                ]
                
                if not any(indicator in analysis_content.lower() for indicator in vision_indicators):
                    raise Exception("Vision analysis doesn't contain visual observations - LLM may not be processing the screenshot")
                
                print(f"Vision analysis successful: {len(analysis_content)} characters of analysis")
                return analysis_content
                
        except Exception as e:
            print(f"Vision analysis failed for {image_path}: {str(e)}")
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
            analysis_start = datetime.now()
            
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
            
            # Apply weights from rules (from rules.md context)
            weights = {
                "typography": 0.25,
                "color": 0.20,
                "layout": 0.25,
                "responsiveness": 0.15,
                "accessibility": 0.15
            }
            
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
                # Check Ollama availability
                if not await self.ollama_client.check_health():
                    raise Exception("AI vision analysis service is currently unavailable")
                
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
                
                # VISION ANALYSIS ONLY - LLM must see the screenshot
                print(f"Starting vision analysis for {url} with screenshot: {desktop_screenshot_path}")
                prompt = self.prompt_service.create_vision_analysis_prompt(url, metrics)
                llm_analysis = await self.ollama_client.generate_vision_analysis(
                    prompt, desktop_screenshot_path
                )
                
                # Verify we got meaningful analysis content
                if not llm_analysis or len(llm_analysis.strip()) < 50:
                    raise Exception("Vision analysis returned insufficient content - AI may not be seeing the screenshot properly")
                    
            except Exception as e:
                llm_error = str(e)
                print(f"LLM vision analysis failed: {e}")
                # No fallbacks - vision analysis is our core feature and must work
            
            # Step 4: Compile final results - ONLY if vision analysis succeeded
            if llm_error:
                # Vision analysis failed - this is our core feature, so fail the entire analysis
                raise Exception(f"Vision analysis is required but failed: {llm_error}")
            
            analysis_result = {
                "analysis_id": f"analysis_{int(analysis_start.timestamp())}",
                "url": url,
                "analyzed_at": analysis_start.isoformat(),
                "analysis_duration": (datetime.now() - analysis_start).total_seconds(),
                "status": "completed",
                
                # Scores
                "overall_score": round(weighted_score, 1),
                "rule_based_score": round(weighted_score, 1),
                "scores_breakdown": {
                    "typography": round(metrics.typography["score"], 1),
                    "color": round(metrics.color["score"], 1),
                    "layout": round(metrics.layout["score"], 1),
                    "responsiveness": round(metrics.responsiveness["score"], 1),
                    "accessibility": round(metrics.accessibility["score"], 1)
                },
                
                # Detailed metrics
                "rule_based_metrics": {
                    "typography": metrics.typography,
                    "color": metrics.color,
                    "layout": metrics.layout,
                    "responsiveness": metrics.responsiveness,
                    "accessibility": metrics.accessibility
                },
                
                # LLM analysis - confirmed to contain vision analysis
                "llm_analysis": {
                    "content": llm_analysis,
                    "error": None,
                    "model_used": self.ollama_client.model,
                    "vision_analysis": True  # Flag to confirm this used vision
                },
                
                # Screenshots
                "screenshots": screenshot_data,
                
                # Metadata
                "weights_applied": weights,
                "rules_version": "v1.0"
            }
            
            return analysis_result
            
        except Exception as e:
            # Proper error handling - no fallback responses
            print(f"Analysis failed for {url}: {str(e)}")
            raise Exception(f"We're experiencing technical issues with our analysis service. Please try again later.")


# Global service instance
ai_analysis_service = AIAnalysisService()
