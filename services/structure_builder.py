"""
Structure builder for speed-optimized prompt enhancement.
Predefined structures for different task types.
"""

from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

class StructureBuilder:
    """Backend structure builder for fast, consistent prompt enhancement."""
    
    def __init__(self):
        self.structures = self._initialize_structures()
    
    def _initialize_structures(self) -> Dict[str, Dict[str, Any]]:
        """Initialize predefined structures for different task types."""
        return {
            "ppt": {
                "template": """Professional Presentation: {title}

SLIDE STRUCTURE (10 slides):
{slides}

VISUAL DESIGN:
- Theme: {design_theme}
- Color Scheme: {color_scheme}
- Typography: {typography}
- Icons/Graphics: {graphics}

CLOSING:
{closing}

Total slides: 10""",
                
                "slide_structure": [
                    "Title & Introduction",
                    "Problem Statement", 
                    "Solution Overview",
                    "Key Features/Benefits",
                    "Technical Details",
                    "Implementation Plan",
                    "Case Study/Example",
                    "Results & Metrics",
                    "Timeline & Milestones",
                    "Call to Action & Q&A"
                ],
                
                "default_elements": {
                    "design_theme": "Modern corporate with clean layouts",
                    "color_scheme": "Professional blue palette with accent colors",
                    "typography": "Sans-serif fonts (Headings: 32pt, Body: 18pt)",
                    "graphics": "Minimalist icons and data visualization charts",
                    "closing": "Summary with clear next steps and contact information"
                }
            },
            
            "code": {
                "template": """Technical Specification: {title}

ARCHITECTURE:
{architecture}

CORE COMPONENTS:
{components}

KEY ALGORITHMS:
{algorithms}

TESTING STRATEGY:
{testing}

PERFORMANCE CONSIDERATIONS:
{performance}

Language: {language}
Framework: {framework}""",
                
                "architecture_sections": [
                    "System Architecture Overview",
                    "Data Flow Design",
                    "Component Interaction",
                    "Security Architecture",
                    "Scalability Design"
                ],
                
                "component_structure": [
                    "Main Application Class",
                    "Data Access Layer",
                    "Business Logic Layer",
                    "API/Interface Layer",
                    "Utility/Helper Classes"
                ],
                
                "testing_approaches": [
                    "Unit Tests (pytest/JUnit)",
                    "Integration Tests",
                    "Performance Tests",
                    "Security Tests",
                    "End-to-End Tests"
                ]
            },
            
            "image": {
                "template": """Visual Artwork: {title}

STYLE & MOOD:
{style}

SUBJECT DETAILS:
{subject}

COLOR PALETTE:
{colors}

COMPOSITION:
{composition}

TECHNICAL SPECS:
{specs}

Art Style: {art_style}
Resolution: {resolution}""",
                
                "style_elements": [
                    "Artistic Style & Period",
                    "Mood & Atmosphere",
                    "Lighting Quality",
                    "Texture & Material",
                    "Cultural Context"
                ],
                
                "composition_rules": [
                    "Focal Point Placement",
                    "Rule of Thirds",
                    "Balance & Symmetry",
                    "Depth & Layers",
                    "Framing & Cropping"
                ],
                
                "technical_specs": [
                    "Image Dimensions",
                    "Resolution Quality",
                    "Color Format",
                    "Style Parameters",
                    "Rendering Details"
                ]
            },
            
            "website": {
                "template": """Web Project: {title}

SITE STRUCTURE:
{pages}

KEY FEATURES:
{features}

TECHNOLOGY STACK:
{tech_stack}

DESIGN REQUIREMENTS:
{design}

PERFORMANCE:
{performance}

Pages: {page_count}
Framework: {framework}""",
                
                "page_structure": [
                    "Homepage/Landing",
                    "About/Company",
                    "Services/Products",
                    "Portfolio/Gallery",
                    "Contact/Forms",
                    "Blog/Resources",
                    "User Dashboard",
                    "Admin Panel"
                ],
                
                "feature_categories": [
                    "User Authentication",
                    "Content Management",
                    "Search & Filtering",
                    "Payment Processing",
                    "Social Integration",
                    "Analytics & Tracking"
                ],
                
                "tech_categories": [
                    "Frontend Framework",
                    "Backend Technology",
                    "Database System",
                    "Hosting/Deployment",
                    "Third-party APIs",
                    "Development Tools"
                ]
            },
            
            "general": {
                "template": """Enhanced Prompt: {title}

CONTEXT:
{context}

REQUIREMENTS:
{requirements}

FORMAT:
{format}

SUCCESS CRITERIA:
{success}

CONSTRAINTS:
{constraints}

Expected Output: {output_type}""",
                
                "context_elements": [
                    "Background Information",
                    "Target Audience",
                    "Domain Context",
                    "Use Case Scenario",
                    "Relevant History"
                ],
                
                "requirement_types": [
                    "Primary Objectives",
                    "Key Deliverables",
                    "Quality Standards",
                    "Timeline Requirements",
                    "Resource Constraints"
                ],
                
                "format_options": [
                    "Output Structure",
                    "Length Guidelines",
                    "Style Preferences",
                    "Tone Requirements",
                    "Presentation Format"
                ]
            }
        }
    
    def build_structure(self, task_type: str, content: Dict[str, Any]) -> str:
        """Build structured output using predefined templates and content."""
        if task_type not in self.structures:
            logger.warning(f"Unknown task type: {task_type}, using general")
            task_type = "general"
        
        structure = self.structures[task_type]
        template = structure["template"]
        
        # Fill template with content
        try:
            result = template.format(**content)
            return result
        except KeyError as e:
            logger.error(f"Missing content key: {e}")
            return self._get_fallback_structure(task_type, content)
    
    def _get_fallback_structure(self, task_type: str, content: Dict[str, Any]) -> str:
        """Get fallback structure when template filling fails."""
        if task_type == "ppt":
            return f"Presentation: {content.get('title', 'Untitled')}\n\nContent: {str(content)}"
        elif task_type == "code":
            return f"Code Specification: {content.get('title', 'Untitled')}\n\nContent: {str(content)}"
        elif task_type == "image":
            return f"Image Description: {content.get('title', 'Untitled')}\n\nContent: {str(content)}"
        elif task_type == "website":
            return f"Website Plan: {content.get('title', 'Untitled')}\n\nContent: {str(content)}"
        else:
            return f"Enhanced Prompt: {content.get('title', 'Untitled')}\n\nContent: {str(content)}"
    
    def get_structure_outline(self, task_type: str) -> List[str]:
        """Get the structure outline for a task type."""
        if task_type not in self.structures:
            return []
        
        structure = self.structures[task_type]
        
        if task_type == "ppt":
            return structure["slide_structure"]
        elif task_type == "code":
            return structure["architecture_sections"]
        elif task_type == "image":
            return structure["style_elements"]
        elif task_type == "website":
            return structure["page_structure"]
        else:
            return structure["context_elements"]

# Global structure builder instance
_structure_builder = None

def get_structure_builder() -> StructureBuilder:
    """Get the global structure builder instance."""
    global _structure_builder
    if _structure_builder is None:
        _structure_builder = StructureBuilder()
    return _structure_builder
