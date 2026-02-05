"""
Model routes for PromptGenius API.
Handles model information and management.
"""

from flask import Blueprint, request, jsonify
import logging

from utils.model_loader import get_model_loader
from config.model_config import get_config

logger = logging.getLogger(__name__)

model_bp = Blueprint('model', __name__)

@model_bp.route('/model-info', methods=['GET'])
def get_model_info():
    """Get information about the loaded model."""
    try:
        loader = get_model_loader()
        model_info = loader.get_model_info()
        
        return jsonify({
            'success': True,
            'model_info': model_info
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
        config = get_config()
        
        config_info = {
            'model_path': str(config.get_model_path()),
            'context_size': config.N_CTX,
            'threads': config.N_THREADS,
            'gpu_layers': config.N_GPU_LAYERS,
            'temperature': config.TEMPERATURE,
            'top_p': config.TOP_P,
            'max_tokens': config.MAX_TOKENS,
            'repeat_penalty': config.REPEAT_PENALTY,
            'model_exists': config.model_exists()
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
        success = loader.reload_model()
        
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
    """Test the model with a simple prompt."""
    try:
        data = request.get_json()
        if not data:
            test_prompt = "Hello, how are you?"
        else:
            test_prompt = data.get('prompt', 'Hello, how are you?')
        
        task_type = data.get('task_type', 'general')
        
        loader = get_model_loader()
        result = loader.generate_prompt(test_prompt, task_type)
        
        return jsonify({
            'success': True,
            'test_prompt': test_prompt,
            'task_type': task_type,
            'result': result,
            'result_length': len(result)
        })
        
    except Exception as e:
        logger.error(f"Error in test_model: {e}")
        
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'message': str(e)
        }), 500
