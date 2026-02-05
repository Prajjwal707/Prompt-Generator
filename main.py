"""
Main entry point for PromptGenius Backend.
Production-ready Flask application.
"""

import os
import logging
from app import create_app

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def main():
    """Main application entry point."""
    # Get configuration from environment
    config_name = os.getenv('FLASK_ENV', 'development')
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Create Flask app
    app = create_app(config_name)
    
    logger.info(f"Starting PromptGenius Backend on {host}:{port}")
    logger.info(f"Environment: {config_name}")
    logger.info(f"Debug mode: {debug}")
    
    # Run the application
    try:
        app.run(
            host=host,
            port=port,
            debug=debug,
            threaded=True
        )
    except KeyboardInterrupt:
        logger.info("Application stopped by user")
    except Exception as e:
        logger.error(f"Application error: {e}")
        raise

if __name__ == '__main__':
    main()
