"""
Caching utilities for PromptGenius backend.
"""

import hashlib
import json
import time
from typing import Dict, Any, Optional
from threading import Lock

class PromptCache:
    """In-memory cache for enhanced prompts."""
    
    def __init__(self, max_size: int = 1000, ttl_seconds: int = 3600):
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.lock = Lock()
    
    def _generate_key(self, prompt: str, task_type: str) -> str:
        """Generate cache key from prompt and task type."""
        content = f"{prompt}:{task_type}"
        return hashlib.sha256(content.encode()).hexdigest()
    
    def get(self, prompt: str, task_type: str) -> Optional[str]:
        """Get cached enhanced prompt."""
        key = self._generate_key(prompt, task_type)
        
        with self.lock:
            if key in self.cache:
                entry = self.cache[key]
                
                # Check TTL
                if time.time() - entry["timestamp"] < self.ttl_seconds:
                    return entry["enhanced_prompt"]
                else:
                    # Expired, remove it
                    del self.cache[key]
        
        return None
    
    def set(self, prompt: str, task_type: str, enhanced_prompt: str) -> None:
        """Cache enhanced prompt."""
        key = self._generate_key(prompt, task_type)
        
        with self.lock:
            # Remove oldest entries if cache is full
            if len(self.cache) >= self.max_size:
                oldest_key = min(self.cache.keys(), 
                               key=lambda k: self.cache[k]["timestamp"])
                del self.cache[oldest_key]
            
            # Add new entry
            self.cache[key] = {
                "enhanced_prompt": enhanced_prompt,
                "timestamp": time.time()
            }
    
    def clear(self) -> None:
        """Clear all cache entries."""
        with self.lock:
            self.cache.clear()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        with self.lock:
            current_time = time.time()
            active_entries = sum(1 for entry in self.cache.values() 
                              if current_time - entry["timestamp"] < self.ttl_seconds)
            
            return {
                "total_entries": len(self.cache),
                "active_entries": active_entries,
                "max_size": self.max_size,
                "ttl_seconds": self.ttl_seconds
            }

# Global cache instance
_prompt_cache = PromptCache()

def get_prompt_cache() -> PromptCache:
    """Get the global prompt cache instance."""
    return _prompt_cache
