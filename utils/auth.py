"""
Authentication utilities for PromptGenius API.
Implements API key authentication and rate limiting.
"""

import os
import hashlib
import secrets
import time
import logging
from typing import Dict, Optional, List
from functools import wraps
from flask import request, jsonify, g

logger = logging.getLogger(__name__)

class APIKeyManager:
    """Manages API keys for authentication."""
    
    def __init__(self):
        self.api_keys = self._load_api_keys()
        self.usage_tracking = {}
    
    def _load_api_keys(self) -> Dict[str, Dict]:
        """Load API keys from environment or file."""
        api_keys = {}
        
        # Load from environment variables
        env_keys = os.getenv('API_KEYS', '').split(',')
        for key in env_keys:
            key = key.strip()
            if key and len(key) == 32:  # Basic validation
                api_keys[key] = {
                    'created_at': time.time(),
                    'name': 'Environment Key',
                    'rate_limit': 100,  # requests per hour
                    'active': True
                }
        
        # Load from file if exists
        api_keys_file = 'config/api_keys.json'
        if os.path.exists(api_keys_file):
            try:
                import json
                with open(api_keys_file, 'r') as f:
                    file_keys = json.load(f)
                api_keys.update(file_keys)
                logger.info(f"Loaded {len(file_keys)} API keys from file")
            except Exception as e:
                logger.error(f"Error loading API keys file: {e}")
        
        logger.info(f"Loaded {len(api_keys)} API keys total")
        return api_keys
    
    def validate_api_key(self, api_key: str) -> Optional[Dict]:
        """Validate an API key."""
        if not api_key:
            return None
        
        key_info = self.api_keys.get(api_key)
        if not key_info:
            return None
        
        if not key_info.get('active', True):
            return None
        
        return key_info
    
    def check_rate_limit(self, api_key: str) -> bool:
        """Check if API key has exceeded rate limit."""
        key_info = self.api_keys.get(api_key)
        if not key_info:
            return False
        
        rate_limit = key_info.get('rate_limit', 100)
        current_time = time.time()
        hour_ago = current_time - 3600  # 1 hour ago
        
        # Clean old usage records
        if api_key not in self.usage_tracking:
            self.usage_tracking[api_key] = []
        
        self.usage_tracking[api_key] = [
            timestamp for timestamp in self.usage_tracking[api_key]
            if timestamp > hour_ago
        ]
        
        # Check rate limit
        if len(self.usage_tracking[api_key]) >= rate_limit:
            return False
        
        # Record this usage
        self.usage_tracking[api_key].append(current_time)
        return True
    
    def generate_api_key(self, name: str = "Generated Key") -> str:
        """Generate a new API key."""
        api_key = secrets.token_hex(16)  # 32 characters
        
        self.api_keys[api_key] = {
            'created_at': time.time(),
            'name': name,
            'rate_limit': 100,
            'active': True
        }
        
        self._save_api_keys()
        logger.info(f"Generated new API key: {api_key[:8]}... for {name}")
        return api_key
    
    def revoke_api_key(self, api_key: str) -> bool:
        """Revoke an API key."""
        if api_key in self.api_keys:
            self.api_keys[api_key]['active'] = False
            self._save_api_keys()
            logger.info(f"Revoked API key: {api_key[:8]}...")
            return True
        return False
    
    def _save_api_keys(self) -> None:
        """Save API keys to file."""
        try:
            os.makedirs('config', exist_ok=True)
            import json
            with open('config/api_keys.json', 'w') as f:
                json.dump(self.api_keys, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving API keys: {e}")
    
    def get_key_stats(self, api_key: str) -> Dict:
        """Get usage statistics for an API key."""
        key_info = self.api_keys.get(api_key)
        if not key_info:
            return {}
        
        current_time = time.time()
        hour_ago = current_time - 3600
        
        usage_count = len(self.usage_tracking.get(api_key, []))
        recent_usage = len([
            timestamp for timestamp in self.usage_tracking.get(api_key, [])
            if timestamp > hour_ago
        ])
        
        return {
            'name': key_info.get('name', 'Unknown'),
            'created_at': key_info.get('created_at'),
            'rate_limit': key_info.get('rate_limit', 100),
            'active': key_info.get('active', True),
            'usage_last_hour': recent_usage,
            'total_usage': usage_count
        }

# Global API key manager
api_key_manager = APIKeyManager()

def require_api_key(f):
    """Decorator to require API key authentication."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get API key from headers
        api_key = request.headers.get('x-api-key')
        
        if not api_key:
            return jsonify({
                'success': False,
                'error': 'API key required',
                'message': 'Please provide an API key in the x-api-key header'
            }), 401
        
        # Validate API key
        key_info = api_key_manager.validate_api_key(api_key)
        if not key_info:
            return jsonify({
                'success': False,
                'error': 'Invalid API key',
                'message': 'The provided API key is invalid or inactive'
            }), 401
        
        # Check rate limit
        if not api_key_manager.check_rate_limit(api_key):
            return jsonify({
                'success': False,
                'error': 'Rate limit exceeded',
                'message': 'API key has exceeded the hourly rate limit'
            }), 429
        
        # Store key info for later use
        g.api_key = api_key
        g.key_info = key_info
        
        return f(*args, **kwargs)
    
    return decorated_function

def optional_api_key(f):
    """Decorator for optional API key authentication."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get API key from headers
        api_key = request.headers.get('x-api-key')
        
        if api_key:
            # Validate API key if provided
            key_info = api_key_manager.validate_api_key(api_key)
            if key_info:
                # Check rate limit
                if api_key_manager.check_rate_limit(api_key):
                    g.api_key = api_key
                    g.key_info = key_info
                else:
                    return jsonify({
                        'success': False,
                        'error': 'Rate limit exceeded',
                        'message': 'API key has exceeded the hourly rate limit'
                    }), 429
        
        return f(*args, **kwargs)
    
    return decorated_function

def get_client_info() -> Dict:
    """Get client information for logging."""
    client_info = {
        'ip_address': request.environ.get('HTTP_X_FORWARDED_FOR', request.environ.get('REMOTE_ADDR', 'unknown')),
        'user_agent': request.headers.get('User-Agent', 'unknown'),
        'endpoint': request.endpoint,
        'method': request.method
    }
    
    if hasattr(g, 'api_key'):
        client_info['api_key'] = g.api_key[:8] + '...'  # Only log partial key
        client_info['key_name'] = g.key_info.get('name', 'Unknown')
    
    return client_info

def log_request(response):
    """Log request information."""
    client_info = get_client_info()
    logger.info(f"Request: {client_info['method']} {client_info['endpoint']} from {client_info['ip_address']}")
    return response

def setup_rate_limiting(app):
    """Setup rate limiting for the Flask app."""
    # This is a simplified rate limiting implementation
    # For production, consider using Flask-Limiter or Redis-based rate limiting
    
    app.before_request(lambda: None)  # Placeholder for rate limiting logic
    app.after_request(log_request)

class SecurityMiddleware:
    """Security middleware for the Flask application."""
    
    @staticmethod
    def add_security_headers(response):
        """Add security headers to responses."""
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response.headers['Content-Security-Policy'] = "default-src 'self'"
        
        return response
    
    @staticmethod
    def validate_content_type():
        """Validate request content type."""
        if request.method in ['POST', 'PUT', 'PATCH']:
            content_type = request.headers.get('Content-Type', '')
            if 'application/json' not in content_type:
                return jsonify({
                    'success': False,
                    'error': 'Invalid content type',
                    'message': 'Content-Type must be application/json'
                }), 415
        return None

def get_api_key_manager() -> APIKeyManager:
    """Get the global API key manager instance."""
    return api_key_manager
