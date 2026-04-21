"""
Input validators for PromptGenius API.
Ensures data integrity and security.
"""

import re
import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class ValidationError(Exception):
    """Custom validation error."""
    pass

def validate_enhance_request(prompt: str, task_type: str) -> Dict[str, Any]:
    """
    Validate prompt enhancement request.
    
    Args:
        prompt: User prompt to enhance
        task_type: Type of task
        
    Returns:
        Validation result with errors if any
    """
    errors = []
    warnings = []
    
    # Validate prompt
    if not prompt:
        errors.append("Prompt cannot be empty")
    else:
        # Length validation
        if len(prompt) < 3:
            errors.append("Prompt is too short (minimum 3 characters)")
        elif len(prompt) > 2000:
            errors.append("Prompt is too long (maximum 2000 characters)")
        
        # Content validation
        if prompt.strip() != prompt:
            warnings.append("Prompt has leading/trailing whitespace")
        
        # Check for potentially malicious content
        if _contains_suspicious_content(prompt):
            errors.append("Prompt contains potentially malicious content")
        
        # Check for excessive repetition
        if _has_excessive_repetition(prompt):
            warnings.append("Prompt contains excessive repetition")
    
    # Validate task type
    valid_task_types = ['general', 'image', 'code', 'ppt', 'website']
    if not task_type:
        errors.append("Task type cannot be empty")
    elif task_type not in valid_task_types:
        errors.append(f"Invalid task type. Must be one of: {', '.join(valid_task_types)}")
    
    return {
        'valid': len(errors) == 0,
        'errors': errors,
        'warnings': warnings
    }

def _contains_suspicious_content(text: str) -> bool:
    """Check for potentially malicious content."""
    suspicious_patterns = [
        r'<script[^>]*>.*?</script>',  # Script tags
        r'javascript:',  # JavaScript protocol
        r'on\w+\s*=',  # Event handlers
        r'eval\s*\(',  # eval function
        r'document\.',  # Document object access
        r'window\.',  # Window object access
        r'__import__',  # Python import
        r'exec\s*\(',  # Python exec
        r'subprocess\.',  # Subprocess calls
        r'os\.system',  # OS system calls
        r'rm\s+-rf',  # Dangerous commands
        r'del\s+.*\\',  # Windows delete commands
    ]
    
    text_lower = text.lower()
    for pattern in suspicious_patterns:
        if re.search(pattern, text_lower, re.IGNORECASE):
            return True
    
    return False

def _has_excessive_repetition(text: str) -> bool:
    """Check for excessive character or word repetition."""
    # Check for character repetition (more than 3 same chars in a row)
    if re.search(r'(.)\1{3,}', text):
        return True
    
    # Check for word repetition
    words = text.lower().split()
    if len(words) > 10:
        # Count word frequencies
        word_counts = {}
        for word in words:
            word_counts[word] = word_counts.get(word, 0) + 1
        
        # If any word appears more than 50% of the time
        max_count = max(word_counts.values())
        if max_count > len(words) * 0.5:
            return True
    
    return False

def sanitize_input(text: str) -> str:
    """
    Sanitize user input to prevent injection attacks.
    
    Args:
        text: Input text to sanitize
        
    Returns:
        Sanitized text
    """
    if not text:
        return ""
    
    # Remove null bytes
    text = text.replace('\x00', '')
    
    # Normalize whitespace
    text = ' '.join(text.split())
    
    # Escape HTML entities (basic)
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('"', '&quot;')
    text = text.replace("'", '&#x27;')
    
    return text.strip()

def validate_api_key(api_key: str) -> bool:
    """
    Validate API key format.
    
    Args:
        api_key: API key to validate
        
    Returns:
        True if valid format
    """
    if not api_key:
        return False
    
    # Basic format validation (alphanumeric, 32 chars)
    if not re.match(r'^[a-zA-Z0-9]{32}$', api_key):
        return False
    
    return True

def validate_batch_request(prompts: List[str], task_type: str) -> Dict[str, Any]:
    """
    Validate batch enhancement request.
    
    Args:
        prompts: List of prompts to enhance
        task_type: Task type for all prompts
        
    Returns:
        Validation result
    """
    errors = []
    warnings = []
    
    # Validate prompts list
    if not isinstance(prompts, list):
        errors.append("Prompts must be an array")
        return {'valid': False, 'errors': errors, 'warnings': warnings}
    
    if len(prompts) == 0:
        errors.append("Prompts array cannot be empty")
    elif len(prompts) > 10:
        errors.append("Maximum batch size is 10 prompts")
    
    # Validate each prompt
    for i, prompt in enumerate(prompts):
        if not isinstance(prompt, str):
            errors.append(f"Prompt at index {i} must be a string")
            continue
        
        if not prompt.strip():
            errors.append(f"Prompt at index {i} cannot be empty")
        elif len(prompt) > 2000:
            errors.append(f"Prompt at index {i} is too long (maximum 2000 characters)")
    
    # Validate task type
    valid_task_types = ['general', 'image', 'code', 'ppt', 'website']
    if task_type not in valid_task_types:
        errors.append(f"Invalid task type. Must be one of: {', '.join(valid_task_types)}")
    
    return {
        'valid': len(errors) == 0,
        'errors': errors,
        'warnings': warnings
    }

def validate_file_upload(file_data: bytes, max_size: int = 10 * 1024 * 1024) -> Dict[str, Any]:
    """
    Validate uploaded file.
    
    Args:
        file_data: File content as bytes
        max_size: Maximum file size in bytes
        
    Returns:
        Validation result
    """
    errors = []
    
    # Check file size
    if len(file_data) > max_size:
        errors.append(f"File too large. Maximum size is {max_size // (1024*1024)}MB")
    
    # Check for empty file
    if len(file_data) == 0:
        errors.append("File cannot be empty")
    
    # Basic content validation (check for suspicious patterns)
    content_str = file_data.decode('utf-8', errors='ignore')
    if _contains_suspicious_content(content_str):
        errors.append("File contains potentially malicious content")
    
    return {
        'valid': len(errors) == 0,
        'errors': errors
    }

def log_validation_error(endpoint: str, errors: List[str], warnings: List[str] = None):
    """
    Log validation errors for monitoring.
    
    Args:
        endpoint: API endpoint
        errors: List of validation errors
        warnings: List of validation warnings
    """
    if errors:
        logger.warning(f"Validation failed at {endpoint}: {'; '.join(errors)}")
    
    if warnings:
        logger.info(f"Validation warnings at {endpoint}: {'; '.join(warnings)}")
