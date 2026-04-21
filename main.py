"""
Simplified main entry point for PromptGenius Backend.
Fast, production-ready Flask application.
"""

import os
import logging
from flask import Flask
from flask_cors import CORS

def create_app():
    """Create and configure Flask application."""
    app = Flask(__name__)
    
    # Configure CORS
    CORS(app, origins=["*"], methods=["GET", "POST"])
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Register blueprints
    from app.routes.enhance import enhance_bp
    from app.routes.finetune import finetune_bp
    from app.routes.model import model_bp
    from app.routes.monitoring import monitoring_bp
    
    app.register_blueprint(enhance_bp, url_prefix='/api')
    app.register_blueprint(finetune_bp, url_prefix='/api')
    app.register_blueprint(model_bp, url_prefix='/api')
    app.register_blueprint(monitoring_bp, url_prefix='/api')
    
    # Preload model at startup
    from utils.model_loader import get_model_loader
    get_model_loader()._load_model()
    
    # Add root health check
    @app.route('/', methods=['GET'])
    def root():
        return {
            'service': 'PromptGenius Backend',
            'version': '2.0.0',
            'status': 'running',
            'endpoints': {
                'enhance': '/api/enhance',
                'health': '/api/health'
            }
        }
    
    app.logger.info("PromptGenius Flask application created")
    return app

if __name__ == '__main__':
    app = create_app()
    
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    print(f"Starting PromptGenius Backend on {host}:{port}")
    print(f"Debug mode: {debug}")
    
    app.run(host=host, port=port, debug=debug, threaded=True)
