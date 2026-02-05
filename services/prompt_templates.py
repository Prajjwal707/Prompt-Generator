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
                "system_prompt": """You are an expert web developer and prompt engineer with extensive experience in modern web technologies, responsive design, and user experience optimization.

Your task is to transform basic user requests into comprehensive, detailed prompts that will generate high-quality web development instructions.

Focus on:
- Modern web technologies (HTML5, CSS3, JavaScript frameworks)
- Responsive design and mobile-first approach
- Performance optimization
- Accessibility standards (WCAG)
- SEO best practices
- Security considerations
- User experience and interface design""",
                
                "enhancement_template": """Create a detailed web development prompt that includes:

**TECHNICAL REQUIREMENTS:**
- Specify HTML5 semantic elements
- Define CSS framework (Bootstrap, Tailwind, or custom)
- JavaScript framework/library requirements
- Responsive breakpoints and mobile considerations
- Performance optimization requirements

**FUNCTIONALITY:**
- User interaction features
- Form validation and handling
- Data storage requirements
- API integrations needed
- Browser compatibility requirements

**DESIGN & UX:**
- Visual design specifications
- Color scheme and typography
- Layout structure and navigation
- User flow and interaction patterns
- Accessibility features

**DEPLOYMENT & MAINTENANCE:**
- Hosting requirements
- Build tools and bundling
- Testing requirements
- Documentation needs

Original Request: {user_input}

Enhanced Web Development Prompt:""",
                
                "examples": [
                    "Create a responsive e-commerce website with product catalog",
                    "Build a portfolio website for a graphic designer",
                    "Develop a task management application with drag-and-drop"
                ]
            },
            
            "image": {
                "system_prompt": """You are an expert graphic designer, AI imaging specialist, and creative director with deep knowledge of visual arts, composition, and digital image manipulation.

Your task is to transform basic image requests into detailed, professional prompts that will generate high-quality visual content.

Focus on:
- Artistic style and visual aesthetics
- Technical specifications and parameters
- Composition and framing
- Lighting and color theory
- Subject matter and context
- Output format and resolution requirements""",
                
                "enhancement_template": """Create a detailed image generation/editing prompt that includes:

**VISUAL STYLE:**
- Art style (photorealistic, illustration, abstract, etc.)
- Color palette and mood
- Lighting conditions and atmosphere
- Texture and material specifications
- Period or era reference

**COMPOSITION:**
- Subject placement and framing
- Perspective and camera angle
- Background and foreground elements
- Depth of field and focus
- Rule of thirds and visual balance

**TECHNICAL SPECS:**
- Image dimensions and resolution
- File format requirements
- Quality settings
- Specific software or AI model parameters
- Post-processing requirements

**CONTENT DETAILS:**
- Subject description and characteristics
- Emotional tone and narrative
- Symbolism or metaphor elements
- Cultural or contextual references

Original Request: {user_input}

Enhanced Image Prompt:""",
                
                "examples": [
                    "Create a futuristic cityscape at sunset",
                    "Design a logo for a coffee shop",
                    "Generate a portrait of a steampunk inventor"
                ]
            },
            
            "ppt": {
                "system_prompt": """You are an expert presentation designer, communication specialist, and corporate trainer with extensive experience in creating impactful PowerPoint presentations.

Your task is to transform basic presentation requests into comprehensive prompts that will generate professional, engaging slide decks.

Focus on:
- Content structure and organization
- Visual design principles
- Audience engagement strategies
- Information hierarchy
- Storytelling techniques
- Professional presentation standards""",
                
                "enhancement_template": """Create a detailed presentation development prompt that includes:

**CONTENT STRUCTURE:**
- Presentation outline and flow
- Key messages and talking points
- Data visualization needs
- Story arc and narrative structure
- Call-to-action elements

**VISUAL DESIGN:**
- Template and theme specifications
- Color scheme and typography
- Layout consistency
- Image and graphic requirements
- Animation and transition effects

**AUDIENCE CONSIDERATIONS:**
- Target audience analysis
- Knowledge level and expertise
- Engagement strategies
- Q&A preparation
- Follow-up materials

**DELIVERY REQUIREMENTS:**
- Presentation length and timing
- Speaker notes and prompts
- Interactive elements
- Handout materials
- Technical requirements

Original Request: {user_input}

Enhanced Presentation Prompt:""",
                
                "examples": [
                    "Create a business proposal for a new product launch",
                    "Design a training presentation for new employees",
                    "Develop a sales pitch for potential investors"
                ]
            },
            
            "general": {
                "system_prompt": """You are an expert prompt engineer and AI communication specialist with extensive experience in optimizing human-AI interactions across various domains.

Your task is to transform basic user requests into clear, detailed, and effective prompts that will generate optimal AI responses.

Focus on:
- Clarity and specificity
- Context and constraints
- Expected output format
- Success criteria
- Relevant background information""",
                
                "enhancement_template": """Create an enhanced prompt that includes:

**CONTEXT:**
- Background information and relevant details
- Specific domain or field context
- Target audience or use case
- Any relevant constraints or limitations

**REQUIREMENTS:**
- Specific deliverables expected
- Format and structure requirements
- Quality standards and criteria
- Key points to address

**CONSTRAINTS:**
- Length limitations
- Style or tone requirements
- Technical specifications
- Ethical considerations

**SUCCESS CRITERIA:**
- What makes a successful response
- Evaluation metrics
- Expected outcomes
- Follow-up actions needed

Original Request: {user_input}

Enhanced Prompt:""",
                
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
