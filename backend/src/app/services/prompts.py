from typing import Any


class PromptConfig:
    """Configuration for AI analysis prompts and limits."""
    
    # Token limits for different analysis types (optimized for better analysis)
    PDF_REPORT_TOKEN_LIMIT = 1500  # Increased for comprehensive analysis
    QUICK_ANALYSIS_TOKEN_LIMIT = 600  # Increased for better quick analysis
    DETAILED_ANALYSIS_TOKEN_LIMIT = 1200  # Increased for focused analysis
    
    # Response length guidelines (characters) - optimized for completeness
    PDF_REPORT_MIN_LENGTH = 1200   # Increased for more comprehensive reports
    PDF_REPORT_TARGET_LENGTH = 2500  # Increased for detailed analysis
    QUICK_ANALYSIS_MIN_LENGTH = 500  # Increased for better quick responses
    
    # Response structure requirements
    PDF_SECTIONS_REQUIRED = [
        "EXECUTIVE SUMMARY",
        "TYPOGRAPHY & READABILITY", 
        "COLOR & VISUAL DESIGN",
        "LAYOUT & STRUCTURE",
        "RESPONSIVENESS & UX",
        "ACCESSIBILITY & COMPLIANCE",
        "ACTIONABLE RECOMMENDATIONS"
    ]
    
    @classmethod
    def get_token_limit(cls, analysis_type: str = "pdf_report") -> int:
        """Get token limit for specific analysis type."""
        limits = {
            "pdf_report": cls.PDF_REPORT_TOKEN_LIMIT,
            "quick": cls.QUICK_ANALYSIS_TOKEN_LIMIT,
            "detailed": cls.DETAILED_ANALYSIS_TOKEN_LIMIT
        }
        return limits.get(analysis_type, cls.PDF_REPORT_TOKEN_LIMIT)
    
    @classmethod
    def get_min_length(cls, analysis_type: str = "pdf_report") -> int:
        """Get minimum expected response length."""
        lengths = {
            "pdf_report": cls.PDF_REPORT_MIN_LENGTH,
            "quick": cls.QUICK_ANALYSIS_MIN_LENGTH
        }
        return lengths.get(analysis_type, cls.PDF_REPORT_MIN_LENGTH)


class VisionAnalysisPrompts:
    """Collection of prompts for AI vision analysis."""
    
    @staticmethod
    def get_analysis_config(analysis_type: str = "pdf_report") -> dict:
        """Get configuration for specific analysis type."""
        return {
            "token_limit": PromptConfig.get_token_limit(analysis_type),
            "min_length": PromptConfig.get_min_length(analysis_type),
            "target_length": getattr(PromptConfig, f"{analysis_type.upper()}_TARGET_LENGTH", 
                                   PromptConfig.PDF_REPORT_TARGET_LENGTH)
        }
    
    @staticmethod
    def create_pdf_report_prompt(url: str, metrics: Any) -> str:
        """
        Create optimized prompt for fast, concise PDF report analysis.
        
        Args:
            url: Website URL being analyzed
            metrics: DesignMetrics object containing rule-based analysis results
            
        Returns:
            Formatted prompt optimized for 160-220 word responses (faster processing)
        """
        
        # Safe metric access with fallbacks
        typo_score = getattr(metrics, 'typography', {}).get('score', 0) if hasattr(metrics, 'typography') else 0
        color_score = getattr(metrics, 'color', {}).get('score', 0) if hasattr(metrics, 'color') else 0
        layout_score = getattr(metrics, 'layout', {}).get('score', 0) if hasattr(metrics, 'layout') else 0
        resp_score = getattr(metrics, 'responsiveness', {}).get('score', 0) if hasattr(metrics, 'responsiveness') else 0
        access_score = getattr(metrics, 'accessibility', {}).get('score', 0) if hasattr(metrics, 'accessibility') else 0
        
        prompt = f"""**IMPORTANT: You are analyzing a website screenshot. Please look at the image provided and base your analysis on what you can actually see.**

**Website Analysis for: {url}**

You are a Senior UI/UX Design Consultant analyzing this website screenshot. Please provide a comprehensive professional design report.

**ANALYSIS REQUIREMENTS:**
- Look at the provided screenshot image and describe what you see
- Analyze the visual design, layout, typography, colors, and user experience
- Target response: {PromptConfig.PDF_REPORT_TARGET_LENGTH} characters
- Be specific about visual elements you observe in the screenshot

**CURRENT DESIGN METRICS (for reference):**
- Typography Score: {typo_score}/100
- Color Design Score: {color_score}/100  
- Layout Score: {layout_score}/100
- Responsiveness Score: {resp_score}/100
- Accessibility Score: {access_score}/100

**ANALYSIS STRUCTURE:**

## EXECUTIVE SUMMARY
Provide an overall assessment of the website's design quality based on what you see in the screenshot. Include 2-3 key observations about visual appeal and usability.

## DESIGN CATEGORY ANALYSIS

### Typography & Readability ({typo_score}/100)
Analyze the fonts, text hierarchy, and readability you observe in the screenshot.

### Color Design ({color_score}/100)  
Evaluate the color scheme, harmony, and visual appeal you can see.

### Layout & Structure ({layout_score}/100)
Assess the layout organization, spacing, and visual structure visible in the image.

### Responsiveness & UX ({resp_score}/100)
Comment on the user interface design and apparent mobile-friendliness.

### Accessibility ({access_score}/100)
Evaluate accessibility indicators visible in the design.

## PRIORITY RECOMMENDATIONS
Provide 3-4 specific, actionable recommendations based on your visual analysis.

## FINAL ASSESSMENT
- Overall Design Rating: X/10
- Professional Readiness: [Ready for Production / Needs Minor Improvements / Requires Significant Work]
- Key Strengths: List 2-3 main strengths
- Main Areas for Improvement: List 2-3 priority areas

**CRITICAL: Base your entire analysis on visual elements you can actually see in the screenshot. Mention specific colors, text, layouts, and design elements that are visible.**"""

        return prompt
    
    @staticmethod
    def create_vision_analysis_prompt(url: str, metrics: Any) -> str:
        """
        Create optimized prompt for fast Llama 3.2-Vision analysis with screenshot.
        
        Args:
            url: Website URL being analyzed
            metrics: DesignMetrics object containing rule-based analysis results
            
        Returns:
            Formatted prompt string for concise vision analysis
        """
        
        # Safe metric access with fallbacks
        typo_score = getattr(metrics, 'typography', {}).get('score', 0) if hasattr(metrics, 'typography') else 0
        color_score = getattr(metrics, 'color', {}).get('score', 0) if hasattr(metrics, 'color') else 0
        layout_score = getattr(metrics, 'layout', {}).get('score', 0) if hasattr(metrics, 'layout') else 0
        resp_score = getattr(metrics, 'responsiveness', {}).get('score', 0) if hasattr(metrics, 'responsiveness') else 0
        access_score = getattr(metrics, 'accessibility', {}).get('score', 0) if hasattr(metrics, 'accessibility') else 0
        
        prompt = f"""Expert UI/UX designer analyzing screenshot of: {url}

**CRITICAL**: Analyze the screenshot and provide concise professional insights.

**RESPONSE TARGET**: {PromptConfig.get_min_length('quick')}-{PromptConfig.DETAILED_ANALYSIS_TOKEN_LIMIT} characters, max {PromptConfig.get_token_limit('detailed')} tokens.

**FAST ANALYSIS STRUCTURE**:

1. **Screenshot Confirmation**: Describe what you see (layout, colors, main elements)

2. **Quick Design Assessment (1-10 scale)**:
   - Visual hierarchy and layout quality
   - Typography readability and choices
   - Color harmony and professional appeal
   - Mobile responsiveness indicators
   - Overall user experience

3. **Key Observations**: 3 specific visual strengths or issues you notice

4. **Priority Recommendation**: 1 main improvement suggestion

**Reference Scores**: Typography: {typo_score} | Color: {color_score} | Layout: {layout_score} | Mobile: {resp_score} | A11y: {access_score}

**REQUIREMENT**: Base analysis entirely on visual elements you observe in the screenshot. Mention specific colors, spacing, text, and design details you see.

Deliver focused, actionable insights in under 400 words."""

        return prompt
    
    @staticmethod
    def create_detailed_vision_prompt(url: str, metrics: Any, rules_content: str = "") -> str:
        """
        Create optimized detailed prompt for faster response times.
        
        Args:
            url: Website URL being analyzed
            metrics: DesignMetrics object containing rule-based analysis results
            rules_content: Custom design rules content from rules.md
            
        Returns:
            Formatted detailed prompt string for concise vision analysis
        """
        
        rules_excerpt = rules_content[:400] if rules_content else "No custom rules loaded"
        
        # Safe metric access with fallbacks
        typo_score = getattr(metrics, 'typography', {}).get('score', 0) if hasattr(metrics, 'typography') else 0
        color_score = getattr(metrics, 'color', {}).get('score', 0) if hasattr(metrics, 'color') else 0
        layout_score = getattr(metrics, 'layout', {}).get('score', 0) if hasattr(metrics, 'layout') else 0
        resp_score = getattr(metrics, 'responsiveness', {}).get('score', 0) if hasattr(metrics, 'responsiveness') else 0
        access_score = getattr(metrics, 'accessibility', {}).get('score', 0) if hasattr(metrics, 'accessibility') else 0
        
        prompt = f"""Senior UI/UX designer analyzing screenshot: {url}

🎯 **MISSION**: Provide expert design analysis based on visual observation.

📸 **ANALYSIS PROTOCOL**:

**STEP 1: Visual Confirmation**
Confirm you see the screenshot and describe immediate visual impression.

**STEP 2: Design Assessment (Rate each 1-10)**

🎨 **Layout & Hierarchy**: Structure, spacing, visual balance
✍️ **Typography**: Font choices, text hierarchy, readability
🌈 **Color Design**: Scheme harmony, contrast, accessibility
🖱️ **UI/UX Elements**: Navigation, buttons, user experience

**STEP 3: Key Insights**
- Top 2 strengths
- Top 2 improvement areas
- Overall visual quality score (1-10)

**DESIGN RULES**: {rules_excerpt}

**CURRENT SCORES**: Typography: {typo_score} | Color: {color_score} | Layout: {layout_score} | Mobile: {resp_score} | A11y: {access_score}

**CRITICAL**: Base analysis ONLY on visual elements you observe. Mention specific colors, text, spacing, and layout details you see.

Target: 300-500 words with precise visual observations."""

        return prompt
    
    @staticmethod
    def create_quick_vision_prompt(url: str) -> str:
        """
        Create ultra-fast prompt for basic vision analysis without detailed metrics.
        
        Args:
            url: Website URL being analyzed
            
        Returns:
            Formatted quick prompt string for rapid analysis
        """
        
        config = PromptConfig.get_token_limit("quick")
        min_length = PromptConfig.get_min_length("quick")
        
        prompt = f"""Quick design analysis for: {url}

**UX Expert rapid assessment. Target: {min_length}-{config*3} characters, max {config} tokens.**

1. **Visual Confirmation**: Describe what you see in the screenshot
2. **Quick Rating (1-10)**: 
   - Layout quality and visual hierarchy
   - Typography and readability
   - Color scheme and aesthetics
   - Overall user experience
3. **Key Observation**: 1-2 specific visual elements you notice
4. **Main Suggestion**: 1 priority improvement

**REQUIREMENT**: Demonstrate you see the screenshot by mentioning specific visual details (colors, text, layout elements).

Keep concise but impactful - under 200 words."""

        return prompt


class PromptTemplates:
    """Template strings for common prompt patterns."""
    
    VISION_VERIFICATION = """
CRITICAL: You MUST look at and analyze the provided screenshot image. 
Your analysis should be based entirely on what you can SEE in the screenshot.
Confirm you can see the screenshot and describe what's visible.
"""
    
    ANALYSIS_REQUIREMENTS = """
**IMPORTANT**: Your analysis must demonstrate you're actually looking at the screenshot. 
Mention specific visual elements, colors, text, and layout details you observe.
"""
    
    SCORING_INSTRUCTION = """
Provide specific, actionable feedback based entirely on visual observation.
Give a final visual quality score (1-10) based on what you see.
Focus ONLY on what you can actually SEE and READ in the screenshot.
"""


# Export the main classes for easy importing
__all__ = ['VisionAnalysisPrompts', 'PromptTemplates', 'PromptConfig']
