"""
Prompt templates for PromptGenius.
Modular prompt engineering system with task-specific templates.
"""

from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

class PromptTemplates:
    """Centralized prompt template management."""
    
    def __init__(self):
        self.templates = self._initialize_templates()
        self.enhancement_rules = self._initialize_enhancement_rules()
    
    def _initialize_templates(self) -> Dict[str, Dict[str, str]]:
        """Initialize task-specific prompt templates."""
        return {
            "website": {
                "system_prompt": """Expert web developer. Generate concise, structured content.""",
                
                "enhancement_template": """Expand this web request into structured content:

User: {user_input}

Generate:
1. Pages needed
2. Key features per page
3. Tech stack recommendations
4. Design requirements

Return structured content only.""",
                
                "examples": [
                    "Create a responsive e-commerce website with product catalog",
                    "Build a portfolio website for a graphic designer",
                    "Develop a task management application with drag-and-drop"
                ]
            },
            
            "image": {
                "system_prompt": """Expert designer. Generate concise visual descriptions.""",
                
                "enhancement_template": """Expand this image request into structured visual content:

User: {user_input}

Generate:
1. Art style and mood
2. Subject details
3. Color palette
4. Composition guidelines
5. Technical specs

Return structured visual content only.""",
                
                "examples": [
                    "Create a futuristic cityscape at sunset",
                    "Design a logo for a coffee shop",
                    "Generate a portrait of a steampunk inventor"
                ]
            },
            
            "code": {
                "system_prompt": """Expert software engineer. Generate concise technical specifications.""",
                
                "enhancement_template": """Expand this code request into structured technical content:

User: {user_input}

Generate:
1. Language and framework
2. Architecture overview
3. Core functions/classes
4. Key algorithms
5. Testing approach

Return structured technical content only.""",
                
                "examples": [
                    "Create a REST API for user management",
                    "Build a data processing pipeline",
                    "Develop a machine learning model trainer"
                ]
            },
            
            "ppt": {
                "system_prompt": """Expert presentation designer. Generate concise slide content.""",
                
                "enhancement_template": """Expand this presentation request into structured slide content:

User: {user_input}

Generate:
1. Compelling title
2. 10-slide outline
3. Key content per slide
4. Visual design theme
5. Color scheme
6. Closing structure

Return structured presentation content only.""",
                
                "examples": [
                    "Create a business proposal for a new product launch",
                    "Design a training presentation for new employees",
                    "Develop a sales pitch for potential investors"
                ]
            },
            
            "general": {
                "system_prompt": """Expert prompt engineer. Generate concise, structured content.""",
                
                "enhancement_template": """Enhance the following prompt to make it clear, specific, and optimized for AI generation.

User Prompt:
{user_input}

Enhancement Goals:

• Clarify intent
• Add missing details
• Specify output format
• Improve precision
• Keep it concise but structured

Return only the enhanced prompt.""",
                
                "examples": [
                    "Explain quantum computing in simple terms",
                    "Write a professional email to a client",
                    "Create a project plan for a marketing campaign"
                ]
            }
        }
    
    def _initialize_enhancement_rules(self) -> Dict[str, List[str]]:
        """Initialize prompt enhancement rules."""
        return {
            "clarity": [
                "Add specific details and context",
                "Remove ambiguous language",
                "Define technical terms",
                "Specify desired output format"
            ],
            "completeness": [
                "Include relevant background information",
                "Specify constraints and limitations",
                "Define success criteria",
                "Add examples or references"
            ],
            "structure": [
                "Organize information logically",
                "Use clear headings and sections",
                "Provide step-by-step instructions when needed",
                "Ensure proper flow and coherence"
            ],
            "engagement": [
                "Use active voice",
                "Include engaging language",
                "Add relevant examples",
                "Consider audience perspective"
            ]
        }
    
    def get_template(self, task_type: str) -> Dict[str, str]:
        """Get template for a specific task type."""
        return self.templates.get(task_type, self.templates["general"])
    
    def get_system_prompt(self, task_type: str) -> str:
        """Get system prompt for a specific task type."""
        template = self.get_template(task_type)
        return template["system_prompt"]
    
    def get_enhancement_template(self, task_type: str) -> str:
        """Get enhancement template for a specific task type."""
        template = self.get_template(task_type)
        return template["enhancement_template"]
    
    def get_examples(self, task_type: str) -> List[str]:
        """Get example prompts for a specific task type."""
        template = self.get_template(task_type)
        return template["examples"]
    
    def list_task_types(self) -> List[str]:
        """Get list of available task types."""
        return list(self.templates.keys())
    
    def validate_task_type(self, task_type: str) -> bool:
        """Validate if task type is supported."""
        return task_type in self.templates
    
    def apply_template(self, user_input: str, task_type: str) -> str:
        """Apply template to user input."""
        if not self.validate_task_type(task_type):
            logger.warning(f"Unknown task type: {task_type}, using general")
            task_type = "general"
        
        template = self.get_enhancement_template(task_type)
        enhanced_prompt = template.format(user_input=user_input)
        
        return enhanced_prompt
    
    def get_enhancement_rules(self) -> Dict[str, List[str]]:
        """Get enhancement rules for different aspects."""
        return self.enhancement_rules
    
    def add_custom_template(self, task_type: str, template: Dict[str, str]) -> None:
        """Add a custom template for a new task type."""
        required_keys = ["system_prompt", "enhancement_template", "examples"]
        
        if not all(key in template for key in required_keys):
            raise ValueError(f"Template must contain all required keys: {required_keys}")
        
        self.templates[task_type] = template
        logger.info(f"Added custom template for task type: {task_type}")

# Global template instance
_prompt_templates = None

def get_prompt_templates() -> PromptTemplates:
    """Get the global prompt templates instance."""
    global _prompt_templates
    if _prompt_templates is None:
        _prompt_templates = PromptTemplates()
    return _prompt_templates
