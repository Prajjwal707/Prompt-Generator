"""
Monitoring routes for PromptGenius API.
Provides health checks and monitoring endpoints.
"""

from flask import Blueprint, jsonify
import logging
from datetime import datetime, timedelta

from monitoring_utils.monitor import get_request_monitor, get_model_monitor, get_health_monitor
from utils.auth import require_api_key, optional_api_key

logger = logging.getLogger(__name__)

monitoring_bp = Blueprint('monitoring', __name__)

@monitoring_bp.route('/health/detailed', methods=['GET'])
@optional_api_key
def health_check():
    """Comprehensive health check endpoint."""
    try:
        health_monitor = get_health_monitor()
        health_status = health_monitor.health_check()
        
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
        # Get all monitors
        request_monitor = get_request_monitor()
        model_monitor = get_model_monitor()
        health_monitor = get_health_monitor()
        
        # Collect metrics
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'performance': request_monitor.get_performance_stats(),
            'errors': request_monitor.get_error_stats(),
            'endpoints': request_monitor.get_endpoint_stats(),
            'model': model_monitor.get_model_stats(),
            'system': health_monitor.get_system_stats(),
            'application': health_monitor.get_application_stats()
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

@monitoring_bp.route('/metrics/performance', methods=['GET'])
@require_api_key
def get_performance_metrics():
    """Get performance-specific metrics."""
    try:
        request_monitor = get_request_monitor()
        performance_stats = request_monitor.get_performance_stats()
        
        return jsonify({
            'success': True,
            'performance': performance_stats
        })
        
    except Exception as e:
        logger.error(f"Error in get_performance_metrics: {e}")
        
        return jsonify({
            'success': False,
            'error': 'Failed to get performance metrics',
            'message': str(e)
        }), 500

@monitoring_bp.route('/metrics/errors', methods=['GET'])
@require_api_key
def get_error_metrics():
    """Get error statistics."""
    try:
        request_monitor = get_request_monitor()
        error_stats = request_monitor.get_error_stats()
        
        return jsonify({
            'success': True,
            'errors': error_stats
        })
        
    except Exception as e:
        logger.error(f"Error in get_error_metrics: {e}")
        
        return jsonify({
            'success': False,
            'error': 'Failed to get error metrics',
            'message': str(e)
        }), 500

@monitoring_bp.route('/metrics/hourly', methods=['GET'])
@require_api_key
def get_hourly_metrics():
    """Get hourly statistics for the last 24 hours."""
    try:
        request_monitor = get_request_monitor()
        hourly_stats = request_monitor.get_hourly_stats(hours=24)
        
        return jsonify({
            'success': True,
            'hourly_stats': hourly_stats,
            'hours_covered': len(hourly_stats)
        })
        
    except Exception as e:
        logger.error(f"Error in get_hourly_metrics: {e}")
        
        return jsonify({
            'success': False,
            'error': 'Failed to get hourly metrics',
            'message': str(e)
        }), 500

@monitoring_bp.route('/metrics/model', methods=['GET'])
@require_api_key
def get_model_metrics():
    """Get model performance metrics."""
    try:
        model_monitor = get_model_monitor()
        model_stats = model_monitor.get_model_stats()
        
        return jsonify({
            'success': True,
            'model_metrics': model_stats
        })
        
    except Exception as e:
        logger.error(f"Error in get_model_metrics: {e}")
        
        return jsonify({
            'success': False,
            'error': 'Failed to get model metrics',
            'message': str(e)
        }), 500

@monitoring_bp.route('/system/info', methods=['GET'])
@require_api_key
def get_system_info():
    """Get detailed system information."""
    try:
        health_monitor = get_health_monitor()
        system_stats = health_monitor.get_system_stats()
        app_stats = health_monitor.get_application_stats()
        
        return jsonify({
            'success': True,
            'system': system_stats,
            'application': app_stats
        })
        
    except Exception as e:
        logger.error(f"Error in get_system_info: {e}")
        
        return jsonify({
            'success': False,
            'error': 'Failed to get system info',
            'message': str(e)
        }), 500

@monitoring_bp.route('/logs/cleanup', methods=['POST'])
@require_api_key
def cleanup_logs():
    """Clean up old log files."""
    try:
        from logging.monitor import RequestMonitor
        
        # Get days parameter from request
        from flask import request
        data = request.get_json() or {}
        days = data.get('days', 30)
        
        if not isinstance(days, int) or days < 1:
            return jsonify({
                'success': False,
                'error': 'Invalid days parameter. Must be a positive integer.'
            }), 400
        
        # Perform cleanup
        request_monitor = get_request_monitor()
        request_monitor.cleanup_old_logs(days)
        
        return jsonify({
            'success': True,
            'message': f'Cleaned up log files older than {days} days'
        })
        
    except Exception as e:
        logger.error(f"Error in cleanup_logs: {e}")
        
        return jsonify({
            'success': False,
            'error': 'Failed to cleanup logs',
            'message': str(e)
        }), 500

@monitoring_bp.route('/status', methods=['GET'])
@optional_api_key
def get_status():
    """Get basic application status."""
    try:
        health_monitor = get_health_monitor()
        request_monitor = get_request_monitor()
        
        # Basic status information
        status = {
            'status': 'operational',
            'timestamp': datetime.now().isoformat(),
            'uptime_seconds': health_monitor.get_application_stats()['uptime_seconds'],
            'total_requests': request_monitor.get_performance_stats()['total_requests']
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
