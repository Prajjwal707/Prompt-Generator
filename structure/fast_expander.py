"""
Fast expander for short prompts in PromptGenius.
Provides template-based expansion for inputs < 6 words to skip LLM generation.
"""

import logging
from typing import Dict, Optional
import re

logger = logging.getLogger(__name__)

class FastExpander:
    """Fast template-based expansion for short prompts."""
    
    def __init__(self):
        self.expansion_templates = self._initialize_expansion_templates()
    
    def _initialize_expansion_templates(self) -> Dict[str, str]:
        """Initialize predefined expansion templates for common short inputs."""
        return {
            # Image generation templates
            "dog in pool": "Generate a detailed photorealistic image prompt of a dog swimming in a pool, including lighting, water reflections, environment details, and camera perspective.",
            "cat on sofa": "Create a detailed photorealistic image prompt of a cat resting on a sofa, with cozy lighting, soft textures, domestic atmosphere, and artistic composition.",
            "sunset beach": "Generate a stunning landscape image prompt of a sunset at the beach, featuring golden hour lighting, ocean waves, sand textures, and atmospheric effects.",
            "mountain landscape": "Create a breathtaking mountain landscape image prompt with dramatic peaks, natural lighting, environmental details, and panoramic composition.",
            
            # Web design templates
            "login page ui": "Design a modern responsive login page UI with email/password fields, validation, error handling, and accessibility support.",
            "portfolio website": "Create a professional portfolio website with project gallery, about section, contact form, and modern responsive design.",
            "ecommerce site": "Design a complete e-commerce website with product catalog, shopping cart, checkout process, and user account management.",
            "blog platform": "Build a modern blog platform with article management, commenting system, user profiles, and responsive design.",
            
            # Code development templates
            "python hello world": "Develop a complete Python 'Hello World' application with proper structure, error handling, documentation, and best practices.",
            "rest api": "Create a comprehensive REST API with endpoints, authentication, validation, error handling, and API documentation.",
            "web scraper": "Build a robust web scraper with data extraction, error handling, rate limiting, and data storage capabilities.",
            "data analysis": "Develop a complete data analysis pipeline with data loading, cleaning, visualization, and statistical analysis.",
            
            # Presentation templates
            "business proposal": "Create a compelling business proposal presentation with problem statement, solution, benefits, timeline, and call to action.",
            "product launch": "Design a product launch presentation with market analysis, product features, competitive advantages, and marketing strategy.",
            "training material": "Develop comprehensive training presentation with learning objectives, content modules, examples, and assessment sections.",
            "company overview": "Create a professional company overview presentation with history, mission, services, team, and future vision.",
            
            # General templates
            "project plan": "Create a detailed project plan with objectives, timeline, resources, milestones, and risk management.",
            "marketing strategy": "Develop a comprehensive marketing strategy with target audience, channels, budget, and performance metrics.",
            "research report": "Structure a research report with introduction, methodology, findings, analysis, and conclusions.",
            "user manual": "Create a user manual with installation guide, features overview, step-by-step instructions, and troubleshooting."
        }
    
    def expand_short_prompt(self, user_input: str, task_type: str = "general") -> Optional[str]:
        """
        Expand short prompt using predefined templates.
        
        Args:
            user_input: Original user input
            task_type: Task type (website, image, ppt, code, general)
            
        Returns:
            Expanded prompt or None if no template matches
        """
        # Normalize input for matching
        normalized_input = user_input.lower().strip()
        
        # Direct template match
        if normalized_input in self.expansion_templates:
            expanded = self.expansion_templates[normalized_input]
            logger.info(f"Fast expanded '{user_input}' using direct template match")
            return expanded
        
        # Pattern-based matching for common structures
        pattern_matches = self._match_patterns(normalized_input, task_type)
        if pattern_matches:
            logger.info(f"Fast expanded '{user_input}' using pattern matching")
            return pattern_matches
        
        # Generic expansion based on task type
        generic_expansion = self._get_generic_expansion(user_input, task_type)
        if generic_expansion:
            logger.info(f"Fast expanded '{user_input}' using generic template")
            return generic_expansion
        
        return None
    
    def _match_patterns(self, normalized_input: str, task_type: str) -> Optional[str]:
        """Match input patterns to generate appropriate expansions."""
        
        # Image generation patterns
        if task_type == "image":
            if re.match(r'^\w+\s+(in|on|at|with)\s+\w+', normalized_input):
                # Pattern: "subject in location" or "subject on surface"
                return f"Generate a detailed photorealistic image prompt of {normalized_input}, including professional lighting, composition, environmental details, and artistic quality."
            
            if re.match(r'^\w+\s+\w+$', normalized_input):
                # Pattern: two-word description
                return f"Create a detailed image prompt featuring {normalized_input}, with artistic style, proper composition, appealing colors, and professional quality."
        
        # Web design patterns
        elif task_type == "website":
            if "page" in normalized_input or "ui" in normalized_input:
                return f"Design a modern responsive {normalized_input} with user-friendly interface, accessibility features, and best practices."
            
            if "website" in normalized_input or "site" in normalized_input:
                return f"Create a complete {normalized_input} with responsive design, modern UI/UX, essential features, and performance optimization."
        
        # Code patterns
        elif task_type == "code":
            if re.match(r'^\w+\s+\w+$', normalized_input):
                # Pattern: two-word code request
                return f"Develop comprehensive {normalized_input} code with proper architecture, error handling, documentation, and best practices."
        
        # Presentation patterns
        elif task_type == "ppt":
            if re.match(r'^\w+\s+\w+$', normalized_input):
                # Pattern: two-word presentation topic
                return f"Create a professional presentation about {normalized_input} with engaging slides, clear structure, visual elements, and compelling content."
        
        return None
    
    def _get_generic_expansion(self, user_input: str, task_type: str) -> str:
        """Get generic expansion based on task type when no specific pattern matches."""
        
        generic_templates = {
            "image": f"Generate a detailed image prompt of {user_input}, including artistic style, composition, lighting, and professional quality.",
            "website": f"Create a modern website for {user_input} with responsive design, user-friendly interface, and essential features.",
            "code": f"Develop code for {user_input} with proper architecture, error handling, documentation, and best practices.",
            "ppt": f"Create a presentation about {user_input} with professional design, clear content structure, and engaging visual elements.",
            "general": f"Provide detailed information about {user_input}, including comprehensive context, specific requirements, and clear guidelines."
        }
        
        return generic_templates.get(task_type, generic_templates["general"])
    
    def should_use_fast_expansion(self, user_input: str) -> bool:
        """
        Determine if fast expansion should be used based on input length.
        
        Args:
            user_input: User input to check
            
        Returns:
            True if input is short enough for fast expansion
        """
        word_count = len(user_input.split())
        return word_count < 6
    
    def get_supported_patterns(self) -> Dict[str, list]:
        """Get information about supported patterns for debugging."""
        return {
            "direct_templates": list(self.expansion_templates.keys()),
            "pattern_types": [
                "subject in location (image)",
                "subject on surface (image)", 
                "two-word descriptions (image)",
                "page/ui designs (website)",
                "website requests (website)",
                "two-word code requests (code)",
                "two-word presentations (ppt)"
            ],
            "task_types": ["image", "website", "code", "ppt", "general"]
        }

# Global fast expander instance
_fast_expander = None

def get_fast_expander() -> FastExpander:
    """Get the global fast expander instance."""
    global _fast_expander
    if _fast_expander is None:
        _fast_expander = FastExpander()
    return _fast_expander
