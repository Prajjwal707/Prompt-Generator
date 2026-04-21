"""
Simplified enhance route for PromptGenius API.
Fast prompt enhancement endpoint.
"""

from flask import Blueprint, request, jsonify
import logging
import time

from services.prompt_enhancer import get_prompt_enhancer
from utils.validators import validate_enhance_request, log_validation_error

logger = logging.getLogger(__name__)

enhance_bp = Blueprint('enhance', __name__)

@enhance_bp.route('/enhance', methods=['POST'])
def enhance_prompt():
    """Enhance a user prompt."""
    start_time = time.time()
    
    try:
        # Validate request data
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'Invalid JSON data'
            }), 400
        
        # Extract parameters
        prompt = data.get('prompt', '').strip()
        task_type = data.get('task_type', 'general').strip().lower()
        
        # Validate inputs using validators
        validation = validate_enhance_request(prompt, task_type)
        if not validation['valid']:
            log_validation_error('/enhance', validation['errors'], validation.get('warnings', []))
            return jsonify({
                'success': False,
                'errors': validation['errors'],
                'warnings': validation.get('warnings', [])
            }), 400
        
        # Get prompt enhancer service
        enhancer = get_prompt_enhancer()
        
        # Enhance the prompt
        result = enhancer.enhance_prompt(prompt, task_type)
        
        # Add request metadata
        result['request_id'] = f"{int(time.time() * 1000)}"
        result['original_prompt'] = prompt
        
        # Return response
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 500
            
    except Exception as e:
        logger.error(f"Enhancement endpoint error: {e}")
        processing_time = time.time() - start_time
        
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'processing_time': processing_time
        }), 500

@enhance_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    try:
        enhancer = get_prompt_enhancer()
        model_loaded = enhancer.model_loader.is_loaded()
        
        return jsonify({
            'status': 'healthy',
            'service': 'PromptGenius Backend',
            'version': '2.0.0',
            'model_loaded': model_loaded,
            'cache_size': enhancer.cache.get_stats()['total_entries']
        }), 200
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500
