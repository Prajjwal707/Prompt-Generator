"""
Model configuration for PromptGenius.
Centralized configuration for model loading and inference parameters.
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class ModelConfig:
    """Configuration class for LLaMA model loading and inference."""
    
    def __init__(self):
        # Model paths
        self.MODEL_DIR = Path(os.getenv("MODEL_DIR", "models"))
        self.MODEL_NAME = os.getenv("MODEL_NAME", "llama-2-7b-chat.Q4_K_M.gguf")
        self.MODEL_PATH = self.MODEL_DIR / self.MODEL_NAME
        
        # Model loading parameters
        self.N_CTX = int(os.getenv("N_CTX", "2048"))  # Context window size
        self.N_THREADS = int(os.getenv("N_THREADS", "4"))  # Number of CPU threads
        self.N_GPU_LAYERS = int(os.getenv("N_GPU_LAYERS", "0"))  # GPU layers (0 = CPU only)
        self.VERBOSE = bool(os.getenv("VERBOSE", "False"))  # Verbose logging
        
        # Inference parameters
        self.TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
        self.TOP_P = float(os.getenv("TOP_P", "0.9"))
        self.MAX_TOKENS = int(os.getenv("MAX_TOKENS", "300"))
        self.REPEAT_PENALTY = float(os.getenv("REPEAT_PENALTY", "1.1"))
        self.STOP_SEQUENCES = ["User:", "Human:", "\n\n", "###"]
        
        # System prompts for different task types
        self.SYSTEM_PROMPTS = {
            "website": """You are an expert web developer and prompt engineer. 
Create detailed, technical prompts for website development tasks.
Include specific technologies, frameworks, and best practices.
Focus on modern web development standards and user experience.""",
            
            "image": """You are an expert graphic designer and AI imaging specialist.
Create detailed prompts for image editing and generation tasks.
Include artistic styles, technical specifications, and composition details.
Focus on visual impact and technical precision.""",
            
            "ppt": """You are an expert presentation designer and communication specialist.
Create detailed prompts for PowerPoint presentation creation.
Include structure, design principles, and content organization.
Focus on clarity, engagement, and professional delivery.""",
            
            "general": """You are an expert prompt engineer and AI communication specialist.
Create clear, detailed, and effective prompts for any task.
Include context, constraints, and desired output format.
Focus on precision and achieving optimal results."""
        }
        
        # Task-specific templates
        self.TASK_TEMPLATES = {
            "website": {
                "prefix": "Create a comprehensive web development prompt for:",
                "suffix": "Include specific technologies, responsive design requirements, and performance considerations."
            },
            "image": {
                "prefix": "Create a detailed image editing/generation prompt for:",
                "suffix": "Include artistic style, composition, lighting, and technical specifications."
            },
            "ppt": {
                "prefix": "Create a professional presentation development prompt for:",
                "suffix": "Include slide structure, visual design, content flow, and audience engagement strategies."
            },
            "general": {
                "prefix": "Create an enhanced, detailed prompt for:",
                "suffix": "Include context, constraints, success criteria, and expected output format."
            }
        }
    
    def get_model_path(self) -> Path:
        """Get the full model path."""
        return self.MODEL_PATH
    
    def model_exists(self) -> bool:
        """Check if model file exists."""
        return self.MODEL_PATH.exists()
    
    def get_inference_params(self, task_type: str = "general") -> Dict[str, Any]:
        """Get inference parameters for a specific task type."""
        base_params = {
            "temperature": self.TEMPERATURE,
            "top_p": self.TOP_P,
            "max_tokens": self.MAX_TOKENS,
            "repeat_penalty": self.REPEAT_PENALTY,
            "stop": self.STOP_SEQUENCES
        }
        
        # Adjust parameters based on task type
        if task_type == "website":
            base_params["temperature"] = 0.6  # More deterministic for technical tasks
            base_params["max_tokens"] = 400
        elif task_type == "image":
            base_params["temperature"] = 0.8  # More creative for visual tasks
            base_params["max_tokens"] = 350
        elif task_type == "ppt":
            base_params["temperature"] = 0.7
            base_params["max_tokens"] = 450
        
        return base_params
    
    def get_system_prompt(self, task_type: str) -> str:
        """Get system prompt for a specific task type."""
        return self.SYSTEM_PROMPTS.get(task_type, self.SYSTEM_PROMPTS["general"])
    
    def get_task_template(self, task_type: str) -> Dict[str, str]:
        """Get task template for a specific task type."""
        return self.TASK_TEMPLATES.get(task_type, self.TASK_TEMPLATES["general"])
    
    def validate_config(self) -> bool:
        """Validate configuration parameters."""
        try:
            # Validate numeric parameters
            if self.N_CTX <= 0:
                logger.error("N_CTX must be positive")
                return False
            if self.N_THREADS <= 0:
                logger.error("N_THREADS must be positive")
                return False
            if self.N_GPU_LAYERS < 0:
                logger.error("N_GPU_LAYERS must be non-negative")
                return False
            
            # Validate inference parameters
            if not 0.0 <= self.TEMPERATURE <= 2.0:
                logger.error("TEMPERATURE must be between 0.0 and 2.0")
                return False
            if not 0.0 <= self.TOP_P <= 1.0:
                logger.error("TOP_P must be between 0.0 and 1.0")
                return False
            if self.MAX_TOKENS <= 0:
                logger.error("MAX_TOKENS must be positive")
                return False
            if self.REPEAT_PENALTY <= 0:
                logger.error("REPEAT_PENALTY must be positive")
                return False
            
            logger.info("Configuration validation passed")
            return True
            
        except Exception as e:
            logger.error(f"Configuration validation failed: {e}")
            return False
    
    def print_config(self) -> None:
        """Print current configuration."""
        print("=== Model Configuration ===")
        print(f"Model Path: {self.MODEL_PATH}")
        print(f"Context Window: {self.N_CTX}")
        print(f"CPU Threads: {self.N_THREADS}")
        print(f"GPU Layers: {self.N_GPU_LAYERS}")
        print(f"Temperature: {self.TEMPERATURE}")
        print(f"Top P: {self.TOP_P}")
        print(f"Max Tokens: {self.MAX_TOKENS}")
        print(f"Repeat Penalty: {self.REPEAT_PENALTY}")
        print("==========================")

# Global configuration instance
model_config = ModelConfig()

def get_config() -> ModelConfig:
    """Get the global model configuration."""
    return model_config
