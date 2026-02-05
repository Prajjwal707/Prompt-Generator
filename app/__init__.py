"""
PromptGenius Flask Application.
Production-ready backend API for prompt enhancement.
"""

from flask import Flask
from flask_cors import CORS
import logging
import os
from pathlib import Path

def create_app(config_name='development'):
    """Application factory pattern."""
    app = Flask(__name__)
    
    # Configure CORS
    CORS(app, origins=["*"], methods=["GET", "POST", "PUT", "DELETE"])
    
    # Setup logging
    setup_logging(app)
    
    # Register blueprints
    register_blueprints(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Setup monitoring middleware
    setup_monitoring(app)
    
    # Add health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return {
            'status': 'healthy',
            'service': 'PromptGenius Backend',
            'version': '1.0.0'
        }
    
    app.logger.info("PromptGenius Flask application created")
    return app

def setup_logging(app):
    """Setup application logging."""
    log_level = os.getenv('LOG_LEVEL', 'INFO')
    
    # Create logs directory if it doesn't exist
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / 'app.log'),
            logging.StreamHandler()
        ]
    )
    
    app.logger.info(f"Logging configured at level: {log_level}")

def register_blueprints(app):
    """Register Flask blueprints."""
    from app.routes.enhance import enhance_bp
    from app.routes.model import model_bp
    from app.routes.finetune import finetune_bp
    from app.routes.monitoring import monitoring_bp
    
    app.register_blueprint(enhance_bp, url_prefix='/api')
    app.register_blueprint(model_bp, url_prefix='/api')
    app.register_blueprint(finetune_bp, url_prefix='/api')
    app.register_blueprint(monitoring_bp, url_prefix='/api')

def register_error_handlers(app):
    """Register error handlers."""
    
    @app.errorhandler(400)
    def bad_request(error):
        return {'error': 'Bad request', 'message': str(error)}, 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        return {'error': 'Unauthorized', 'message': str(error)}, 401
    
    @app.errorhandler(403)
    def forbidden(error):
        return {'error': 'Forbidden', 'message': str(error)}, 403
    
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Not found', 'message': str(error)}, 404
    
    @app.errorhandler(429)
    def rate_limit_exceeded(error):
        return {'error': 'Rate limit exceeded', 'message': str(error)}, 429
    
    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f"Internal server error: {error}")
        return {'error': 'Internal server error', 'message': 'Something went wrong'}, 500
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        app.logger.error(f"Unhandled exception: {error}")
        return {'error': 'Internal server error', 'message': str(error)}, 500

def setup_monitoring(app):
    """Setup monitoring middleware."""
    @app.before_request
    def before_request():
        from flask import g
        import time
        g.start_time = time.time()
    
    @app.after_request
    def after_request(response):
        from flask import g, request
        import time
        
        # Calculate response time
        response_time = time.time() - getattr(g, 'start_time', time.time())
        
        # Log request if monitoring is available
        try:
            from monitoring_utils.monitor import get_request_monitor
            from utils.auth import get_client_info
            
            monitor = get_request_monitor()
            client_info = get_client_info()
            
            monitor.log_request(
                endpoint=request.endpoint or 'unknown',
                method=request.method,
                status_code=response.status_code,
                response_time=response_time,
                user_id=client_info.get('key_name'),
                api_key=client_info.get('api_key')
            )
        except Exception as e:
            # Don't let monitoring errors break the app
            app.logger.debug(f"Monitoring error: {e}")
        
        return response
