"""
Model routes for PromptGenius API.
Handles model information and management.
"""

from flask import Blueprint, request, jsonify
import logging

from utils.model_loader import get_model_loader
from utils.auth import require_api_key

logger = logging.getLogger(__name__)

model_bp = Blueprint('model', __name__)

@model_bp.route('/model-info', methods=['GET'])
@require_api_key
def get_model_info():
    """Get information about the loaded model."""
    try:
        loader = get_model_loader()
        config = loader.get_config()
        model_info = {
            "loaded": loader.is_loaded(),
            "model_path": loader.model_path,
            "context_size": config.get('n_ctx', 0),
            "threads": config.get('threads', 0),
            "gpu_layers": 0,
            "initialization_time": 0.0
        }
        
        # Ensure only JSON-serializable data is returned
        safe_model_info = {
            "loaded": model_info.get("loaded", False),
            "model_path": model_info.get("model_path", ""),
            "context_size": model_info.get("context_size", 0),
            "threads": model_info.get("threads", 0),
            "gpu_layers": model_info.get("gpu_layers", 0),
            "initialization_time": model_info.get("initialization_time", 0.0)
        }
        
        # Add error if model not loaded
        if "error" in model_info:
            safe_model_info["error"] = model_info["error"]
        
        return jsonify({
            'success': True,
            'model_info': safe_model_info
        })
        
    except Exception as e:
        logger.error(f"Error in get_model_info: {e}")
        
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@model_bp.route('/model-config', methods=['GET'])
def get_model_config():
    """Get current model configuration."""
    try:
        loader = get_model_loader()
        config = loader.get_config()
        
        config_info = {
            'model_path': loader.model_path,
            'context_size': config.get('n_ctx', 0),
            'threads': config.get('threads', 0),
            'gpu_layers': 0,
            'temperature': config.get('temperature', 0.5),
            'top_p': config.get('top_p', 0.8),
            'max_tokens': config.get('max_tokens', 200),
            'repeat_penalty': 1.0,
            'model_exists': True
        }
        
        return jsonify({
            'success': True,
            'config': config_info
        })
        
    except Exception as e:
        logger.error(f"Error in get_model_config: {e}")
        
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@model_bp.route('/model/reload', methods=['POST'])
def reload_model():
    """Reload the model."""
    try:
        loader = get_model_loader()
        loader.unload_model()
        success = loader._load_model()
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Model reloaded successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to reload model'
            }), 500
        
    except Exception as e:
        logger.error(f"Error in reload_model: {e}")
        
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@model_bp.route('/model/unload', methods=['POST'])
def unload_model():
    """Unload the model from memory."""
    try:
        loader = get_model_loader()
        loader.unload_model()
        
        return jsonify({
            'success': True,
            'message': 'Model unloaded successfully'
        })
        
    except Exception as e:
        logger.error(f"Error in unload_model: {e}")
        
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@model_bp.route('/model/test', methods=['POST'])
def test_model():
    """Test model with a simple prompt."""
    try:
        data = request.get_json()
        if not data:
            test_prompt = "Hello, how are you?"
        else:
            test_prompt = data.get('prompt', 'Hello, how are you?')
        
        task_type = data.get('task_type', 'general')
        
        from services.prompt_enhancer import get_prompt_enhancer
        enhancer = get_prompt_enhancer()
        result = enhancer.enhance_prompt(test_prompt, task_type)
        
        # Extract enhanced_prompt from the new dict format
        enhanced_prompt = result.get("enhanced_prompt", "")
        
        return jsonify({
            'success': True,
            'test_prompt': test_prompt,
            'task_type': task_type,
            'result': enhanced_prompt,
            'result_length': len(enhanced_prompt)
        })
        
    except Exception as e:
        logger.error(f"Error in test_model: {e}")
        
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'message': str(e)
        }), 500
