"""
Monitoring routes for PromptGenius API.
Provides health checks and monitoring endpoints.
"""

from flask import Blueprint, jsonify
import logging
from datetime import datetime, timedelta

from utils.auth import require_api_key, optional_api_key
from utils.model_loader import get_model_loader
from services.prompt_enhancer import get_prompt_enhancer
from utils.cache import get_prompt_cache
import psutil
import time

logger = logging.getLogger(__name__)

monitoring_bp = Blueprint('monitoring', __name__)

@monitoring_bp.route('/health/detailed', methods=['GET'])
@optional_api_key
def health_check():
    """Comprehensive health check endpoint."""
    try:
        # Get system stats
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Get model status
        model_loader = get_model_loader()
        model_loaded = model_loader.is_loaded()
        
        # Get cache stats
        cache = get_prompt_cache()
        cache_stats = cache.get_stats()
        
        health_status = {
            'status': 'healthy' if model_loaded else 'degraded',
            'timestamp': datetime.now().isoformat(),
            'system': {
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'disk_usage_percent': (disk.used / disk.total) * 100
            },
            'model': {
                'loaded': model_loaded,
                'model_path': model_loader.model_path
            },
            'cache': cache_stats
        }
        
        return jsonify({
            'success': True,
            'health': health_status
        })
        
    except Exception as e:
        logger.error(f"Error in health_check: {e}")
        
        return jsonify({
            'success': False,
            'error': 'Health check failed',
            'message': str(e)
        }), 500

@monitoring_bp.route('/metrics', methods=['GET'])
@require_api_key
def get_metrics():
    """Get application metrics and statistics."""
    try:
        # Get basic metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Get model status
        model_loader = get_model_loader()
        model_loaded = model_loader.is_loaded()
        
        # Get cache stats
        cache = get_prompt_cache()
        cache_stats = cache.get_stats()
        
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'system': {
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'memory_available_gb': memory.available / (1024**3),
                'disk_usage_percent': (disk.used / disk.total) * 100,
                'disk_free_gb': disk.free / (1024**3)
            },
            'model': {
                'loaded': model_loaded,
                'model_path': model_loader.model_path
            },
            'cache': cache_stats,
            'uptime_seconds': time.time()  # Simple uptime
        }
        
        return jsonify({
            'success': True,
            'metrics': metrics
        })
        
    except Exception as e:
        logger.error(f"Error in get_metrics: {e}")
        
        return jsonify({
            'success': False,
            'error': 'Failed to get metrics',
            'message': str(e)
        }), 500

# Simplified monitoring endpoints
@monitoring_bp.route('/status', methods=['GET'])
@optional_api_key
def get_status():
    """Get basic application status."""
    try:
        model_loader = get_model_loader()
        cache = get_prompt_cache()
        
        status = {
            'status': 'operational' if model_loader.is_loaded() else 'degraded',
            'timestamp': datetime.now().isoformat(),
            'uptime_seconds': time.time(),
            'cache_entries': cache.get_stats()['total_entries']
        }
        
        return jsonify({
            'success': True,
            'status': status
        })
        
    except Exception as e:
        logger.error(f"Error in get_status: {e}")
        
        return jsonify({
            'success': False,
            'error': 'Failed to get status',
            'message': str(e)
        }), 500
