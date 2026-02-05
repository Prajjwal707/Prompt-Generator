"""
Enhanced model loader for PromptGenius.
Features lazy loading, GPU/CPU auto-detection, and configurable parameters.
"""

import os
import logging
from pathlib import Path
from typing import Optional, Dict, Any
import threading
import time

from llama_cpp import Llama
from config.model_config import get_config

logger = logging.getLogger(__name__)

class ModelLoader:
    """Enhanced model loader with lazy loading and error handling."""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        """Singleton pattern for model loader."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize the model loader."""
        if hasattr(self, '_initialized'):
            return
        
        self.config = get_config()
        self.llm: Optional[Llama] = None
        self._loaded = False
        self._load_lock = threading.Lock()
        self._initialization_time = 0
        
        logger.info("ModelLoader initialized")
        self._initialized = True
    
    def _detect_gpu(self) -> int:
        """Detect GPU and determine optimal number of GPU layers."""
        try:
            import torch
            if torch.cuda.is_available():
                gpu_count = torch.cuda.device_count()
                gpu_memory = torch.cuda.get_device_properties(0).total_memory
                
                logger.info(f"Detected {gpu_count} GPU(s) with {gpu_memory // 1024**3}GB memory")
                
                # Determine GPU layers based on available memory
                if gpu_memory >= 8 * 1024**3:  # 8GB+
                    return min(35, gpu_count * 35)  # Use more layers for more memory
                elif gpu_memory >= 4 * 1024**3:  # 4GB+
                    return 20
                else:
                    return 10
            else:
                logger.info("No GPU detected, using CPU only")
                return 0
        except ImportError:
            logger.warning("PyTorch not available, assuming CPU only")
            return 0
        except Exception as e:
            logger.warning(f"GPU detection failed: {e}, using CPU only")
            return 0
    
    def _load_model(self) -> bool:
        """Load the LLaMA model with error handling."""
        with self._load_lock:
            if self._loaded:
                return True
            
            try:
                start_time = time.time()
                
                # Check if model file exists
                if not self.config.model_exists():
                    logger.error(f"Model file not found: {self.config.get_model_path()}")
                    logger.info("Please download the model file or set correct MODEL_DIR environment variable")
                    return False
                
                # Auto-detect GPU layers if not specified
                gpu_layers = self.config.N_GPU_LAYERS
                if gpu_layers == 0:  # Auto-detect
                    gpu_layers = self._detect_gpu()
                
                logger.info(f"Loading model: {self.config.get_model_path()}")
                logger.info(f"Configuration: ctx={self.config.N_CTX}, threads={self.config.N_THREADS}, gpu_layers={gpu_layers}")
                
                # Load the model
                self.llm = Llama(
                    model_path=str(self.config.get_model_path()),
                    n_ctx=self.config.N_CTX,
                    n_threads=self.config.N_THREADS,
                    n_gpu_layers=gpu_layers,
                    verbose=self.config.VERBOSE
                )
                
                self._loaded = True
                self._initialization_time = time.time() - start_time
                
                logger.info(f"Model loaded successfully in {self._initialization_time:.2f}s")
                return True
                
            except Exception as e:
                logger.error(f"Failed to load model: {e}")
                self.llm = None
                self._loaded = False
                return False
    
    def is_loaded(self) -> bool:
        """Check if model is loaded."""
        return self._loaded and self.llm is not None
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the loaded model."""
        if not self.is_loaded():
            return {"loaded": False, "error": "Model not loaded"}
        
        return {
            "loaded": True,
            "model_path": str(self.config.get_model_path()),
            "context_size": self.config.N_CTX,
            "threads": self.config.N_THREADS,
            "gpu_layers": self.config.N_GPU_LAYERS,
            "initialization_time": self._initialization_time,
            "n_ctx": getattr(self.llm, 'n_ctx', self.config.N_CTX),
            "n_embd": getattr(self.llm, 'n_embd', 'unknown')
        }
    
    def generate_prompt(self, user_input: str, task_type: str = "general") -> str:
        """Generate enhanced prompt using the loaded model."""
        if not self.is_loaded():
            if not self._load_model():
                raise RuntimeError("Failed to load model")
        
        try:
            # Get task-specific configuration
            system_prompt = self.config.get_system_prompt(task_type)
            task_template = self.config.get_task_template(task_type)
            inference_params = self.config.get_inference_params(task_type)
            
            # Build the prompt
            prompt_parts = [
                system_prompt,
                "",
                task_template["prefix"],
                user_input,
                task_template["suffix"],
                "",
                "Enhanced prompt:"
            ]
            
            full_prompt = "\n".join(prompt_parts)
            
            logger.debug(f"Generating prompt for task type: {task_type}")
            logger.debug(f"Prompt length: {len(full_prompt)} characters")
            
            # Generate response
            output = self.llm(
                full_prompt,
                **inference_params
            )
            
            enhanced_prompt = output['choices'][0]['text'].strip()
            
            # Clean up the output
            enhanced_prompt = self._clean_output(enhanced_prompt)
            
            logger.info(f"Generated enhanced prompt ({len(enhanced_prompt)} chars) for {task_type}")
            return enhanced_prompt
            
        except Exception as e:
            logger.error(f"Error generating prompt: {e}")
            raise RuntimeError(f"Prompt generation failed: {e}")
    
    def _clean_output(self, output: str) -> str:
        """Clean and format the model output."""
        if not output:
            return ""
        
        # Remove common artifacts
        lines = output.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith(('Enhanced prompt:', 'Prompt:', 'Output:')):
                cleaned_lines.append(line)
        
        # Join lines and clean up
        result = '\n'.join(cleaned_lines)
        
        # Remove excessive whitespace
        while '\n\n\n' in result:
            result = result.replace('\n\n\n', '\n\n')
        
        return result.strip()
    
    def unload_model(self) -> None:
        """Unload the model from memory."""
        if self.llm is not None:
            try:
                # Clear the model reference
                self.llm = None
                self._loaded = False
                logger.info("Model unloaded from memory")
            except Exception as e:
                logger.warning(f"Error unloading model: {e}")
    
    def reload_model(self) -> bool:
        """Reload the model."""
        self.unload_model()
        return self._load_model()

# Global model loader instance
_model_loader = None

def get_model_loader() -> ModelLoader:
    """Get the global model loader instance."""
    global _model_loader
    if _model_loader is None:
        _model_loader = ModelLoader()
    return _model_loader

def generate_prompt(user_input: str, task_type: str = "general") -> str:
    """Convenience function to generate a prompt."""
    loader = get_model_loader()
    return loader.generate_prompt(user_input, task_type)
