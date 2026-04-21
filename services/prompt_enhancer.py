"""
Optimized prompt enhancer service for PromptGenius.
Fast enhancement with task-specific token limits and caching.
"""

import json
import logging
import time
import hashlib
from typing import Dict, Any, Optional
import re

from utils.model_loader import get_model_loader
from structure.structure_builder import get_structure_builder
from utils.cache import get_prompt_cache
from structure.fast_expander import get_fast_expander

logger = logging.getLogger(__name__)

class PromptEnhancer:
    """Optimized service for enhancing user prompts."""
    
    def __init__(self):
        self.model_loader = get_model_loader()
        self.structure_builder = get_structure_builder()
        self.cache = get_prompt_cache()
        self.fast_expander = get_fast_expander()
        
        # Task-specific token limits
        self.token_limits = {
            "general": 120,
            "image": 80,
            "code": 180,
            "ppt": 200,
            "website": 180
        }
        
        logger.info("PromptEnhancer initialized")
    
    
    def _expand_short_prompt(self, prompt: str) -> str:
        """Expand very short prompts (<5 words) for better context."""
        words = prompt.strip().split()
        if len(words) < 5:
            expansion_prompts = {
                "general": "Create a detailed and comprehensive response about: {prompt}",
                "image": "Generate a detailed visual description for: {prompt}",
                "code": "Develop a complete technical solution for: {prompt}",
                "ppt": "Create a professional presentation about: {prompt}",
                "website": "Design a complete website project for: {prompt}"
            }
            return expansion_prompts.get("general", "Create a detailed response about: {prompt}").format(prompt=prompt)
        return prompt
    
    def _build_enhancement_prompt(self, user_prompt: str, task_type: str) -> str:
        """Build the enhancement prompt for the LLM."""
        return f"""
You are an expert AI system.

IMPORTANT:
- You MUST return valid JSON
- NO explanation
- NO extra text
- ONLY JSON

Task: {task_type}

Input: {user_prompt}

Output format strictly:

{{
  "title": "...",
  "pages": "...",
  "features": "...",
  "tech_stack": "...",
  "design": "...",
  "performance": "..."
}}
"""
    
    def _smart_fallback(self, text: str, task_type: str):
        text = text.strip()

        if task_type == "website":
            return {
                "title": text.split("\n")[0][:80],
                "pages": text,
                "features": text,
                "tech_stack": "React, Node.js, MongoDB",
                "design": text,
                "performance": "Optimized for speed and responsiveness",
                "page_count": "5-8",
                "framework": "React/Next.js"
            }

        elif task_type == "image":
            return {
                "title": text.split("\n")[0][:80],
                "style": text,
                "subject": text,
                "colors": text,
                "composition": text,
                "specs": "High quality, detailed rendering"
            }

        elif task_type == "code":
            return {
                "title": text.split("\n")[0][:80],
                "architecture": text,
                "components": text,
                "algorithms": text,
                "testing": "Unit + integration tests",
                "performance": "Optimized logic"
            }

        elif task_type == "ppt":
            return {
                "title": text.split("\n")[0][:80],
                "slides": text,
                "design_theme": "Modern",
                "color_scheme": "Professional",
                "typography": "Clean sans-serif",
                "graphics": "Minimal",
                "closing": "Summary"
            }

        else:
            return {
                "title": text.split("\n")[0][:80],
                "context": text,
                "requirements": text,
                "format": "Structured",
                "success": "Clear output",
                "constraints": "None"
            }
        
    def _extract_title(self, text: str) -> str:
        """Extract title from response text."""
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if line and len(line) < 100:
                # Remove common prefixes
                line = re.sub(r'^(Title:|Prompt:|Enhanced:)', '', line).strip()
                if line and not line.lower().startswith(('here is', 'the enhanced', 'below is')):
                    return line
        return "Enhanced Prompt"
    
        
    def _extract_list_content(self, text: str, section_name: str) -> str:
        """Extract list content from response."""
        lines = text.split('\n')
        list_items = []
        
        for line in lines:
            if re.match(r'^\d+\.', line) or line.startswith('-') or line.startswith('*'):
                list_items.append(line.strip())
        
        return '\n'.join(list_items[:10]) if list_items else ""
    
    def _generate_default_slides(self, response: str) -> str:
        """Generate default slide structure based on response."""
        default_slides = [
            "1. Title & Introduction",
            "2. Problem Statement",
            "3. Solution Overview", 
            "4. Key Features/Benefits",
            "5. Implementation Details",
            "6. Examples/Case Studies",
            "7. Results & Outcomes",
            "8. Timeline & Milestones",
            "9. Resources & Requirements",
            "10. Next Steps & Q&A"
        ]
        return '\n'.join(default_slides)
    
    def enhance_prompt(self, user_input: str, task_type: str = "general") -> Dict[str, Any]:
        """
        Enhance a user prompt using optimized LLM generation.
        
        Args:
            user_input: Original user prompt
            task_type: Type of task (website, image, ppt, general)
            
        Returns:
            Dictionary containing enhanced prompt and metadata
        """
        start_time = time.time()
        
        try:
            # Check cache first
            cached_result = self.cache.get(user_input, task_type)
            if cached_result:
                logger.info(f"Cache hit for prompt: {user_input[:50]}...")
                return {
                    "success": True,
                    "enhanced_prompt": cached_result,
                    "task_type": task_type,
                    "processing_time": 0.001,
                    "cached": True
                }
            
            # Try fast expansion for short prompts
            if self.fast_expander.should_use_fast_expansion(user_input):
                fast_result = self.fast_expander.expand_short_prompt(user_input, task_type)
                if fast_result:
                    # Cache the fast result
                    self.cache.set(user_input, task_type, fast_result)
                    logger.info(f"Fast expanded '{user_input}' in {time.time() - start_time:.3f}s")
                    return {
                        "success": True,
                        "enhanced_prompt": fast_result,
                        "task_type": task_type,
                        "processing_time": 0.001,
                        "cached": False,
                        "fast_path": True
                    }
            
            # Expand short prompts if needed
            expanded_prompt = self._expand_short_prompt(user_input)
            
            # Build enhancement prompt
            enhancement_prompt = self._build_enhancement_prompt(expanded_prompt, task_type)
            
            # Get task-specific token limit with dynamic optimization
            base_tokens = self.token_limits.get(task_type, 120)
            max_tokens = min(len(user_input.split()) * 5, base_tokens * 2, 400)
            
            # Generate enhanced content
            enhanced_content = self.model_loader.generate_response(
                enhancement_prompt, 
                max_tokens=max_tokens
            )
            
            print("RAW MODEL OUTPUT:\n", enhanced_content)
            
            # Parse JSON response
            try:
                structured_content = json.loads(enhanced_content)
            except:
                # Smart fallback (not dumb fallback)
                structured_content = self._smart_fallback(enhanced_content, task_type)
            
            # Build final structured prompt
            final_prompt = self.structure_builder.build_structure(task_type, structured_content)
            
            # Cache the result
            self.cache.set(user_input, task_type, final_prompt)
            
            processing_time = time.time() - start_time
            
            logger.info(f"Enhanced {task_type} prompt in {processing_time:.2f}s")
            
            return {
                "success": True,
                "enhanced_prompt": final_prompt,
                "task_type": task_type,
                "processing_time": processing_time,
                "cached": False,
                "tokens_used": len(enhanced_content.split())
            }
            
        except Exception as e:
            processing_time = time.time() - start_time
            logger.error(f"Prompt enhancement failed: {e}")
            
            return {
                "success": False,
                "error": str(e),
                "task_type": task_type,
                "processing_time": processing_time,
                "cached": False
            }

# Global enhancer instance
_prompt_enhancer = None

def get_prompt_enhancer() -> PromptEnhancer:
    """Get the global prompt enhancer instance."""
    global _prompt_enhancer
    if _prompt_enhancer is None:
        _prompt_enhancer = PromptEnhancer()
    return _prompt_enhancer
