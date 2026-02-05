"""
Prompt enhancement service for PromptGenius.
Combines templates with AI model to generate enhanced prompts.
"""

import logging
from typing import Dict, Any, Optional
import time
import re

from utils.model_loader import get_model_loader
from services.prompt_templates import get_prompt_templates
from config.model_config import get_config

logger = logging.getLogger(__name__)

class PromptEnhancer:
    """Service for enhancing user prompts using templates and AI."""
    
    def __init__(self):
        self.model_loader = get_model_loader()
        self.templates = get_prompt_templates()
        self.config = get_config()
        
        # Enhancement statistics
        self.stats = {
            "total_enhancements": 0,
            "task_type_counts": {},
            "average_enhancement_time": 0.0,
            "error_count": 0
        }
    
    def enhance_prompt(self, user_input: str, task_type: str = "general") -> Dict[str, Any]:
        """
        Enhance a user prompt using templates and AI model.
        
        Args:
            user_input: Original user prompt
            task_type: Type of task (website, image, ppt, general)
            
        Returns:
            Dictionary containing enhanced prompt and metadata
        """
        start_time = time.time()
        
        try:
            # Validate inputs
            if not user_input or not user_input.strip():
                raise ValueError("User input cannot be empty")
            
            if not self.templates.validate_task_type(task_type):
                logger.warning(f"Unknown task type: {task_type}, using general")
                task_type = "general"
            
            # Pre-process user input
            cleaned_input = self._preprocess_input(user_input)
            
            # Apply template
            template_prompt = self.templates.apply_template(cleaned_input, task_type)
            
            # Generate enhanced prompt using AI model
            enhanced_prompt = self.model_loader.generate_prompt(template_prompt, task_type)
            
            # Post-process the output
            final_prompt = self._postprocess_output(enhanced_prompt)
            
            # Calculate enhancement time
            enhancement_time = time.time() - start_time
            
            # Update statistics
            self._update_stats(task_type, enhancement_time, success=True)
            
            # Prepare response
            response = {
                "success": True,
                "original_prompt": user_input,
                "enhanced_prompt": final_prompt,
                "task_type": task_type,
                "enhancement_time": round(enhancement_time, 2),
                "prompt_length": len(final_prompt),
                "template_used": task_type,
                "model_info": self.model_loader.get_model_info()
            }
            
            logger.info(f"Enhanced prompt for {task_type} in {enhancement_time:.2f}s")
            return response
            
        except Exception as e:
            enhancement_time = time.time() - start_time
            self._update_stats(task_type, enhancement_time, success=False)
            
            logger.error(f"Prompt enhancement failed: {e}")
            
            return {
                "success": False,
                "error": str(e),
                "original_prompt": user_input,
                "task_type": task_type,
                "enhancement_time": round(enhancement_time, 2)
            }
    
    def _preprocess_input(self, user_input: str) -> str:
        """Pre-process user input before enhancement."""
        if not user_input:
            return ""
        
        # Clean up the input
        cleaned = user_input.strip()
        
        # Remove excessive whitespace
        cleaned = re.sub(r'\s+', ' ', cleaned)
        
        # Ensure proper capitalization (first letter)
        if cleaned and not cleaned[0].isupper():
            cleaned = cleaned[0].upper() + cleaned[1:]
        
        # Ensure proper punctuation at the end
        if cleaned and cleaned[-1] not in '.!?':
            cleaned += '.'
        
        return cleaned
    
    def _postprocess_output(self, enhanced_prompt: str) -> str:
        """Post-process the AI-generated enhanced prompt."""
        if not enhanced_prompt:
            return ""
        
        # Remove common AI artifacts
        lines = enhanced_prompt.split('\n')
        cleaned_lines = []
        
        skip_patterns = [
            r'^Enhanced Prompt:',
            r'^Enhanced Web Development Prompt:',
            r'^Enhanced Image Prompt:',
            r'^Enhanced Presentation Prompt:',
            r'^Here is the enhanced prompt:',
            r'^.*prompt.*:$',
            r'^Original Request:',
            r'^.*enhanced.*prompt.*$'
        ]
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Skip lines that match artifact patterns
            skip_line = False
            for pattern in skip_patterns:
                if re.match(pattern, line, re.IGNORECASE):
                    skip_line = True
                    break
            
            if not skip_line:
                cleaned_lines.append(line)
        
        # Join lines and clean up
        result = '\n'.join(cleaned_lines)
        
        # Remove excessive whitespace
        while '\n\n\n' in result:
            result = result.replace('\n\n\n', '\n\n')
        
        # Remove excessive spaces
        result = re.sub(r' +', ' ', result)
        
        return result.strip()
    
    def _update_stats(self, task_type: str, enhancement_time: float, success: bool) -> None:
        """Update enhancement statistics."""
        self.stats["total_enhancements"] += 1
        
        if task_type not in self.stats["task_type_counts"]:
            self.stats["task_type_counts"][task_type] = 0
        self.stats["task_type_counts"][task_type] += 1
        
        # Update average enhancement time
        total_time = self.stats["average_enhancement_time"] * (self.stats["total_enhancements"] - 1)
        self.stats["average_enhancement_time"] = (total_time + enhancement_time) / self.stats["total_enhancements"]
        
        if not success:
            self.stats["error_count"] += 1
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get enhancement statistics."""
        stats = self.stats.copy()
        
        # Add derived statistics
        if stats["total_enhancements"] > 0:
            stats["success_rate"] = ((stats["total_enhancements"] - stats["error_count"]) / 
                                    stats["total_enhancements"]) * 100
        else:
            stats["success_rate"] = 0.0
        
        # Add model information
        stats["model_loaded"] = self.model_loader.is_loaded()
        stats["available_task_types"] = self.templates.list_task_types()
        
        return stats
    
    def validate_prompt(self, prompt: str) -> Dict[str, Any]:
        """Validate a prompt for quality and completeness."""
        if not prompt:
            return {"valid": False, "errors": ["Prompt cannot be empty"]}
        
        errors = []
        warnings = []
        
        # Length checks
        if len(prompt) < 10:
            errors.append("Prompt is too short (minimum 10 characters)")
        elif len(prompt) > 2000:
            warnings.append("Prompt is very long, consider being more concise")
        
        # Content checks
        if prompt.isupper():
            warnings.append("Avoid using all caps")
        
        # Check for basic structure
        if not any(char in prompt for char in '.!?'):
            warnings.append("Consider ending with proper punctuation")
        
        # Check for ambiguous terms
        ambiguous_terms = ["thing", "stuff", "something", "anything", "etc"]
        for term in ambiguous_terms:
            if term.lower() in prompt.lower():
                warnings.append(f"Ambiguous term '{term}' detected - be more specific")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "length": len(prompt),
            "word_count": len(prompt.split())
        }
    
    def batch_enhance(self, prompts: list, task_type: str = "general") -> list:
        """Enhance multiple prompts in batch."""
        results = []
        
        for i, prompt in enumerate(prompts):
            try:
                result = self.enhance_prompt(prompt, task_type)
                result["batch_index"] = i
                results.append(result)
            except Exception as e:
                results.append({
                    "success": False,
                    "error": str(e),
                    "batch_index": i,
                    "original_prompt": prompt
                })
        
        return results
    
    def get_enhancement_suggestions(self, prompt: str) -> list:
        """Get suggestions for improving a prompt."""
        suggestions = []
        
        validation = self.validate_prompt(prompt)
        
        # Add suggestions based on validation
        for error in validation["errors"]:
            suggestions.append(f"Fix: {error}")
        
        for warning in validation["warnings"]:
            suggestions.append(f"Consider: {warning}")
        
        # Add general enhancement suggestions
        if len(prompt.split()) < 10:
            suggestions.append("Add more context and details")
        
        if not any(word in prompt.lower() for word in ["because", "since", "due to"]):
            suggestions.append("Explain the reasoning or context")
        
        if not any(word in prompt.lower() for word in ["format", "structure", "output"]):
            suggestions.append("Specify desired output format")
        
        return suggestions

# Global enhancer instance
_prompt_enhancer = None

def get_prompt_enhancer() -> PromptEnhancer:
    """Get the global prompt enhancer instance."""
    global _prompt_enhancer
    if _prompt_enhancer is None:
        _prompt_enhancer = PromptEnhancer()
    return _prompt_enhancer
