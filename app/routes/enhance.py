"""
Enhancement routes for PromptGenius API.
Handles prompt enhancement requests.
"""

from flask import Blueprint, request, jsonify
import logging
import time
from typing import Dict, Any

from services.prompt_enhancer import get_prompt_enhancer
from utils.validators import validate_enhance_request
from utils.auth import require_api_key, optional_api_key

logger = logging.getLogger(__name__)

enhance_bp = Blueprint('enhance', __name__)

@enhance_bp.route('/enhance', methods=['POST'])
@require_api_key
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
        
        # Extract and validate parameters
        prompt = data.get('prompt', '').strip()
        task_type = data.get('task_type', 'general').strip().lower()
        
        # Validate input
        validation_result = validate_enhance_request(prompt, task_type)
        if not validation_result['valid']:
            return jsonify({
                'success': False,
                'error': 'Validation failed',
                'details': validation_result['errors']
            }), 400
        
        # Get prompt enhancer service
        enhancer = get_prompt_enhancer()
        
        # Enhance the prompt
        result = enhancer.enhance_prompt(prompt, task_type)
        
        # Add processing time
        processing_time = time.time() - start_time
        result['processing_time'] = round(processing_time, 3)
        
        # Log the request
        logger.info(f"Enhanced prompt for task_type='{task_type}' in {processing_time:.3f}s")
        
        return jsonify(result)
        
    except Exception as e:
        processing_time = time.time() - start_time
        logger.error(f"Error in enhance_prompt: {e}")
        
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'message': str(e),
            'processing_time': round(processing_time, 3)
        }), 500

@enhance_bp.route('/enhance/batch', methods=['POST'])
@require_api_key
def batch_enhance():
    """Enhance multiple prompts in batch."""
    start_time = time.time()
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'Invalid JSON data'
            }), 400
        
        prompts = data.get('prompts', [])
        task_type = data.get('task_type', 'general').strip().lower()
        
        # Validate batch request
        if not isinstance(prompts, list):
            return jsonify({
                'success': False,
                'error': 'prompts must be an array'
            }), 400
        
        if len(prompts) == 0:
            return jsonify({
                'success': False,
                'error': 'prompts array cannot be empty'
            }), 400
        
        if len(prompts) > 10:  # Limit batch size
            return jsonify({
                'success': False,
                'error': 'Maximum batch size is 10 prompts'
            }), 400
        
        # Get enhancer and process batch
        enhancer = get_prompt_enhancer()
        results = enhancer.batch_enhance(prompts, task_type)
        
        processing_time = time.time() - start_time
        
        response = {
            'success': True,
            'results': results,
            'total_prompts': len(prompts),
            'successful_count': sum(1 for r in results if r.get('success', False)),
            'processing_time': round(processing_time, 3)
        }
        
        logger.info(f"Batch enhanced {len(prompts)} prompts in {processing_time:.3f}s")
        
        return jsonify(response)
        
    except Exception as e:
        processing_time = time.time() - start_time
        logger.error(f"Error in batch_enhance: {e}")
        
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'message': str(e),
            'processing_time': round(processing_time, 3)
        }), 500

@enhance_bp.route('/validate', methods=['POST'])
@optional_api_key
def validate_prompt():
    """Validate a prompt without enhancement."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'Invalid JSON data'
            }), 400
        
        prompt = data.get('prompt', '').strip()
        
        if not prompt:
            return jsonify({
                'success': False,
                'error': 'prompt cannot be empty'
            }), 400
        
        # Get enhancer and validate prompt
        enhancer = get_prompt_enhancer()
        validation_result = enhancer.validate_prompt(prompt)
        
        # Get enhancement suggestions
        suggestions = enhancer.get_enhancement_suggestions(prompt)
        
        response = {
            'success': True,
            'validation': validation_result,
            'suggestions': suggestions
        }
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error in validate_prompt: {e}")
        
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@enhance_bp.route('/stats', methods=['GET'])
@require_api_key
def get_enhancement_stats():
    """Get enhancement statistics."""
    try:
        enhancer = get_prompt_enhancer()
        stats = enhancer.get_statistics()
        
        return jsonify({
            'success': True,
            'statistics': stats
        })
        
    except Exception as e:
        logger.error(f"Error in get_enhancement_stats: {e}")
        
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@enhance_bp.route('/task-types', methods=['GET'])
@optional_api_key
def get_task_types():
    """Get available task types and their examples."""
    try:
        from services.prompt_templates import get_prompt_templates
        
        templates = get_prompt_templates()
        task_types = templates.list_task_types()
        
        task_info = {}
        for task_type in task_types:
            template = templates.get_template(task_type)
            task_info[task_type] = {
                'name': task_type.title(),
                'examples': template.get('examples', [])
            }
        
        return jsonify({
            'success': True,
            'task_types': task_info
        })
        
    except Exception as e:
        logger.error(f"Error in get_task_types: {e}")
        
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'message': str(e)
        }), 500
