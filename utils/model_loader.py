"""
Optimized model loader for PromptGenius.
Uses llama-cpp-python with singleton pattern for efficiency.
"""

import logging
import os
from typing import Optional, Dict, Any
import threading
from pathlib import Path

try:
    from llama_cpp import Llama
except ImportError:
    Llama = None
    logging.warning("llama-cpp-python not installed. Model loading will fail.")

logger = logging.getLogger(__name__)

class ModelLoader:
    """Singleton model loader for optimized CPU inference."""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if hasattr(self, '_initialized'):
            return
        
        self._initialized = True
        self._model = None
        self._model_loaded = False
        self._load_lock = threading.Lock()
        
        # Model configuration
        self.model_path = os.getenv('MODEL_PATH', 'models/llama-2-7b-chat.Q4_K_M.gguf')
        self.config = {
            'n_ctx': 1024,
            'max_tokens': 200,
            'temperature': 0.5,
            'top_p': 0.8,
            'threads': os.cpu_count(),
            'stop': ['</s>', '[INST]', '[/INST]', 'User:', 'Assistant:', '\n\n']
        }
        
        logger.info("ModelLoader initialized")
    
    def _load_model(self) -> bool:
        """Load the model if not already loaded."""
        if self._model_loaded:
            return True
        
        with self._load_lock:
            if self._model_loaded:
                return True
            
            try:
                if Llama is None:
                    raise ImportError("llama-cpp-python not installed")
                
                model_file = Path(self.model_path)
                if not model_file.exists():
                    raise FileNotFoundError(f"Model file not found: {self.model_path}")
                
                logger.info(f"Loading model from {self.model_path}")
                
                self._model = Llama(
                    model_path=str(model_file),
                    n_ctx=self.config['n_ctx'],
                    n_threads=self.config['threads'],
                    verbose=False
                )
                
                self._model_loaded = True
                logger.info("Model loaded successfully")
                return True
                
            except Exception as e:
                logger.error(f"Failed to load model: {e}")
                return False
    
    def generate_response(self, prompt: str, max_tokens: Optional[int] = None) -> str:
        """Generate response from the model."""
        if not self._load_model():
            raise RuntimeError("Failed to load model")
        
        try:
            # Use task-specific token limits if provided
            tokens = max_tokens or self.config['max_tokens']
            
            response = self._model(
                prompt,
                max_tokens=tokens,
                temperature=self.config['temperature'],
                top_p=self.config['top_p'],
                stop=self.config['stop'],
                echo=False
            )
            
            # Extract the generated text
            if isinstance(response, dict) and 'choices' in response:
                text = response['choices'][0]['text'].strip()
            elif isinstance(response, list) and len(response) > 0:
                text = response[0]['text'].strip()
            else:
                text = str(response).strip()
            
            return text
            
        except Exception as e:
            logger.error(f"Generation failed: {e}")
            raise
    
    def get_config(self) -> Dict[str, Any]:
        """Get current model configuration."""
        return self.config.copy()
    
    def is_loaded(self) -> bool:
        """Check if model is loaded."""
        return self._model_loaded
    
    def unload_model(self):
        """Unload the model to free memory."""
        with self._load_lock:
            if self._model_loaded:
                self._model = None
                self._model_loaded = False
                logger.info("Model unloaded")

# Global instance
_model_loader = None

def get_model_loader() -> ModelLoader:
    """Get the global model loader instance."""
    global _model_loader
    if _model_loader is None:
        _model_loader = ModelLoader()
    return _model_loader
