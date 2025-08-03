from typing import Any


class PromptConfig:
    """Configuration for AI analysis prompts and limits."""
    
    # Token limits for different analysis types
    PDF_REPORT_TOKEN_LIMIT = 2500
    QUICK_ANALYSIS_TOKEN_LIMIT = 800
    DETAILED_ANALYSIS_TOKEN_LIMIT = 1800
    
    # Response length guidelines (characters)
    PDF_REPORT_MIN_LENGTH = 1500
    PDF_REPORT_TARGET_LENGTH = 3000
    QUICK_ANALYSIS_MIN_LENGTH = 400
    
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
        Create comprehensive prompt for professional PDF report analysis.
        
        Args:
            url: Website URL being analyzed
            metrics: DesignMetrics object containing rule-based analysis results
            
        Returns:
            Formatted prompt optimized for detailed PDF report generation
        """
        
        # Safe metric access with fallbacks
        typo_score = getattr(metrics, 'typography', {}).get('score', 0) if hasattr(metrics, 'typography') else 0
        color_score = getattr(metrics, 'color', {}).get('score', 0) if hasattr(metrics, 'color') else 0
        layout_score = getattr(metrics, 'layout', {}).get('score', 0) if hasattr(metrics, 'layout') else 0
        resp_score = getattr(metrics, 'responsiveness', {}).get('score', 0) if hasattr(metrics, 'responsiveness') else 0
        access_score = getattr(metrics, 'accessibility', {}).get('score', 0) if hasattr(metrics, 'accessibility') else 0
        
        prompt = f"""You are a Senior UI/UX Design Consultant creating a comprehensive design audit report for: {url}

**CRITICAL**: Analyze the provided screenshot image and create a professional report suitable for PDF generation.

**RESPONSE LENGTH REQUIREMENTS**:
- Target response: {PromptConfig.PDF_REPORT_TARGET_LENGTH} characters ({PromptConfig.PDF_REPORT_TOKEN_LIMIT} tokens max)
- Minimum response: {PromptConfig.PDF_REPORT_MIN_LENGTH} characters required
- Be comprehensive but concise - every word must add value

## REPORT STRUCTURE REQUIRED:

### 1. EXECUTIVE SUMMARY
- Overall design quality assessment (Professional/Good/Needs Improvement/Poor)
- Primary visual impression and brand perception
- Key strengths (2-3 main positives)
- Critical improvement areas (2-3 main issues)

### 2. DETAILED CATEGORY ANALYSIS

**TYPOGRAPHY & READABILITY** (Current Score: {typo_score}/100)
- Font choices and brand alignment
- Text hierarchy effectiveness (H1, H2, body)
- Readability and contrast assessment
- Specific improvement recommendations

**COLOR & VISUAL DESIGN** (Current Score: {color_score}/100)
- Color scheme harmony and accessibility
- Brand consistency evaluation
- Visual appeal and professionalism
- Specific color recommendations

**LAYOUT & STRUCTURE** (Current Score: {layout_score}/100)
- Grid alignment and spacing consistency
- Visual hierarchy and information architecture
- White space utilization
- Specific layout improvements

**RESPONSIVENESS & UX** (Current Score: {resp_score}/100)
- Mobile-first design indicators
- Navigation clarity and usability
- Call-to-action effectiveness
- User experience flow assessment

**ACCESSIBILITY & COMPLIANCE** (Current Score: {access_score}/100)
- Visual accessibility compliance
- Contrast and readability for all users
- Inclusive design elements
- Accessibility improvement priorities

### 3. ACTIONABLE RECOMMENDATIONS
Provide specific, prioritized improvement suggestions:

**HIGH PRIORITY** (Fix immediately):
- [Specific actionable item 1]
- [Specific actionable item 2]
- [Specific actionable item 3]

**MEDIUM PRIORITY** (Address soon):
- [Specific actionable item 1]
- [Specific actionable item 2]
- [Specific actionable item 3]

**ENHANCEMENT** (Future improvements):
- [Specific actionable item 1]
- [Specific actionable item 2]

### 4. VISUAL QUALITY SCORE
- Overall Design Rating: X/10
- Professional Readiness: [Ready/Needs Work/Major Revision Required]

**SECTION LENGTH GUIDELINES**:
- Executive Summary: 3-4 sentences per point (150-200 characters)
- Each Category Analysis: 2-3 detailed observations (200-300 characters)
- Recommendations: Specific actionable items (100-150 characters each)
- Total sections must cover all required categories above

**FORMATTING REQUIREMENTS**:
- Use markdown headers (##, ###) for sections
- Use bullet points for lists
- Be specific and actionable in all recommendations
- Include visual details you observe in the screenshot
- Write in professional consulting tone
- MUST reach minimum {PromptConfig.PDF_REPORT_MIN_LENGTH} characters total

**IMPORTANT**: Base all analysis on actual visual observation of the screenshot. Reference specific colors, spacing, text, and design elements you can see.

Provide a complete, professional analysis suitable for client presentation."""

        return prompt
    
    @staticmethod
    def create_vision_analysis_prompt(url: str, metrics: Any) -> str:
        """
        Create optimized prompt for Llama 3.2-Vision analysis with screenshot.
        
        Args:
            url: Website URL being analyzed
            metrics: DesignMetrics object containing rule-based analysis results
            
        Returns:
            Formatted prompt string for vision analysis
        """
        
        # Safe metric access with fallbacks
        typo_score = getattr(metrics, 'typography', {}).get('score', 0) if hasattr(metrics, 'typography') else 0
        color_score = getattr(metrics, 'color', {}).get('score', 0) if hasattr(metrics, 'color') else 0
        layout_score = getattr(metrics, 'layout', {}).get('score', 0) if hasattr(metrics, 'layout') else 0
        resp_score = getattr(metrics, 'responsiveness', {}).get('score', 0) if hasattr(metrics, 'responsiveness') else 0
        access_score = getattr(metrics, 'accessibility', {}).get('score', 0) if hasattr(metrics, 'accessibility') else 0
        
        prompt = f"""You are an expert UI/UX designer with advanced vision capabilities. You are analyzing a SCREENSHOT of this website: {url}

CRITICAL: You MUST look at and analyze the provided screenshot image. Your analysis should be based entirely on what you can SEE in the screenshot.

**RESPONSE LENGTH**: Target {PromptConfig.get_min_length('quick')}-{PromptConfig.DETAILED_ANALYSIS_TOKEN_LIMIT} characters, maximum {PromptConfig.get_token_limit('detailed')} tokens.

VISUAL ANALYSIS REQUIREMENTS (based on what you SEE in the screenshot):

**1. SCREENSHOT VERIFICATION**:
- Confirm you can see the website screenshot
- Describe what you see in the first few lines (header, main content, colors)

**2. VISUAL LAYOUT ANALYSIS (1-10 scale)**:
- Overall visual hierarchy visible in the screenshot
- Grid alignment, spacing consistency, and balance you observe
- Content organization and readability flow you can see

**3. TYPOGRAPHY & READABILITY (from what's visible)**:
- Font choices, sizing, and hierarchy you can observe in the screenshot
- Text contrast and legibility of all text elements you see
- Reading flow and content structure visible in the image

**4. COLOR & VISUAL DESIGN (based on screenshot)**:
- Color scheme harmony and accessibility visible in the image
- Contrast ratios and visual emphasis you can see
- Brand consistency and aesthetic appeal from the screenshot

**5. UI/UX ELEMENTS (what you observe in the screenshot)**:
- Navigation clarity and button design visible
- Interactive element visibility and accessibility you can see
- Mobile-responsive design indicators visible
- Call-to-action effectiveness from what's shown

**6. TECHNICAL OBSERVATIONS (from the screenshot)**:
- Layout consistency and professional polish visible
- Visual bugs, alignment issues, or inconsistencies you can see
- Accessibility compliance indicators visible in the image

**AUTOMATED METRICS FOR REFERENCE**:
Typography: {typo_score}/100 | Color: {color_score}/100 | Layout: {layout_score}/100
Responsiveness: {resp_score}/100 | Accessibility: {access_score}/100

**DELIVERABLE**: 
1. START by confirming you can see the screenshot and briefly describe what's visible
2. Provide specific, actionable feedback based entirely on visual observation
3. Give a final visual quality score (1-10) based on what you see
4. Focus ONLY on what you can actually SEE and READ in the screenshot

**IMPORTANT**: Your analysis must demonstrate you're actually looking at the screenshot. Mention specific visual elements, colors, text, and layout details you observe.

Response limit: 600 words."""

        return prompt
    
    @staticmethod
    def create_detailed_vision_prompt(url: str, metrics: Any, rules_content: str = "") -> str:
        """
        Create a more detailed prompt with custom design rules context.
        
        Args:
            url: Website URL being analyzed
            metrics: DesignMetrics object containing rule-based analysis results
            rules_content: Custom design rules content from rules.md
            
        Returns:
            Formatted detailed prompt string for vision analysis
        """
        
        rules_excerpt = rules_content[:800] if rules_content else "No custom rules loaded"
        
        # Safe metric access with fallbacks
        typo_score = getattr(metrics, 'typography', {}).get('score', 0) if hasattr(metrics, 'typography') else 0
        color_score = getattr(metrics, 'color', {}).get('score', 0) if hasattr(metrics, 'color') else 0
        layout_score = getattr(metrics, 'layout', {}).get('score', 0) if hasattr(metrics, 'layout') else 0
        resp_score = getattr(metrics, 'responsiveness', {}).get('score', 0) if hasattr(metrics, 'responsiveness') else 0
        access_score = getattr(metrics, 'accessibility', {}).get('score', 0) if hasattr(metrics, 'accessibility') else 0
        
        prompt = f"""You are a senior UI/UX designer with advanced computer vision capabilities analyzing this website screenshot: {url}

🎯 MISSION: Provide expert design analysis based EXCLUSIVELY on visual observation of the screenshot.

📸 SCREENSHOT ANALYSIS PROTOCOL:

**STEP 1: VISUAL CONFIRMATION**
- Explicitly confirm you can see the website screenshot
- Describe the immediate visual impression (layout structure, dominant colors, content type)

**STEP 2: DESIGN EVALUATION (Rate each 1-10)**

🎨 **VISUAL HIERARCHY & LAYOUT**
- Information architecture clarity from visual structure
- Grid system adherence and spacing consistency
- Content flow and visual balance observed
- White space utilization and breathing room

✍️ **TYPOGRAPHY & READABILITY** 
- Font selection appropriateness for brand/purpose
- Text size hierarchy effectiveness (H1, H2, body text)
- Reading flow and text contrast ratios
- Content density and paragraph structure

🌈 **COLOR & VISUAL DESIGN**
- Color scheme harmony and brand consistency
- Accessibility of color choices (contrast, readability)
- Visual emphasis and call-to-action prominence
- Overall aesthetic appeal and professionalism

🖱️ **UI/UX ELEMENTS**
- Navigation clarity and intuitive structure
- Button design and interactive element visibility
- Mobile responsiveness indicators (if applicable)
- User experience flow and ease of use

**STEP 3: TECHNICAL ASSESSMENT**
- Visual consistency across interface elements
- Potential accessibility issues visible
- Professional polish and attention to detail
- Any visual bugs or alignment problems

**DESIGN RULES CONTEXT**:
{rules_excerpt}

**AUTOMATED ANALYSIS REFERENCE**:
• Typography Score: {typo_score}/100
• Color Score: {color_score}/100  
• Layout Score: {layout_score}/100
• Responsiveness: {resp_score}/100
• Accessibility: {access_score}/100

**FINAL DELIVERABLE**:
1. Screenshot confirmation with visual description
2. Specific design observations and ratings
3. Top 3 strengths and 3 improvement areas
4. Overall visual quality score (1-10)
5. Actionable recommendations

**CRITICAL**: Base analysis ONLY on visual elements you can actually observe in the screenshot. Mention specific colors, text, spacing, and layout details you see.

Target: 500-700 words with precise visual observations."""

        return prompt
    
    @staticmethod
    def create_quick_vision_prompt(url: str) -> str:
        """
        Create a quick prompt for basic vision analysis without detailed metrics.
        
        Args:
            url: Website URL being analyzed
            
        Returns:
            Formatted quick prompt string for basic vision analysis
        """
        
        config = PromptConfig.get_token_limit("quick")
        min_length = PromptConfig.get_min_length("quick")
        
        prompt = f"""Analyze this website screenshot for: {url}

You are a UX expert. Look at the screenshot and provide:

**RESPONSE LIMITS**: {min_length}-{config*4} characters, maximum {config} tokens.

1. **Visual Confirmation**: Confirm you can see the screenshot and describe what's visible
2. **Quick Assessment**: Rate the design quality (1-10) based on:
   - Layout and visual hierarchy
   - Color scheme and typography
   - Overall user experience
3. **Key Observations**: 2-3 specific visual elements you notice
4. **Improvement Suggestion**: 1 main recommendation

Keep it concise but demonstrate you're actually seeing the screenshot by mentioning specific visual details."""

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
