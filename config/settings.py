"""
Application settings and configuration management.
Loads configuration from environment variables and .env file.
"""

import os
from pathlib import Path
from typing import List, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """Application settings class."""
    
    # Flask Configuration
    FLASK_ENV: str = os.getenv('FLASK_ENV', 'development')
    DEBUG: bool = os.getenv('DEBUG', 'False').lower() == 'true'
    HOST: str = os.getenv('HOST', '0.0.0.0')
    PORT: int = int(os.getenv('PORT', '5000'))
    
    # Logging Configuration
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    
    # Model Configuration
    MODEL_DIR: str = os.getenv('MODEL_DIR', 'models')
    MODEL_NAME: str = os.getenv('MODEL_NAME', 'llama-2-7b-chat.Q4_K_M.gguf')
    N_CTX: int = int(os.getenv('N_CTX', '2048'))
    N_THREADS: int = int(os.getenv('N_THREADS', '4'))
    N_GPU_LAYERS: int = int(os.getenv('N_GPU_LAYERS', '0'))
    VERBOSE: bool = os.getenv('VERBOSE', 'False').lower() == 'true'
    
    # Inference Parameters
    TEMPERATURE: float = float(os.getenv('TEMPERATURE', '0.7'))
    TOP_P: float = float(os.getenv('TOP_P', '0.9'))
    MAX_TOKENS: int = int(os.getenv('MAX_TOKENS', '300'))
    REPEAT_PENALTY: float = float(os.getenv('REPEAT_PENALTY', '1.1'))
    
    # API Configuration
    API_KEYS: List[str] = [key.strip() for key in os.getenv('API_KEYS', '').split(',') if key.strip()]
    RATE_LIMIT_PER_HOUR: int = int(os.getenv('RATE_LIMIT_PER_HOUR', '100'))
    
    # Security Configuration
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    CORS_ORIGINS: str = os.getenv('CORS_ORIGINS', '*')
    
    # Database Configuration
    DATABASE_URL: str = os.getenv('DATABASE_URL', 'sqlite:///promptgenius.db')
    
    # Monitoring Configuration
    ENABLE_MONITORING: bool = os.getenv('ENABLE_MONITORING', 'True').lower() == 'true'
    MONITOR_LOG_RETENTION_DAYS: int = int(os.getenv('MONITOR_LOG_RETENTION_DAYS', '30'))
    
    # Fine-tuning Configuration
    FINETUNE_OUTPUT_DIR: str = os.getenv('FINETUNE_OUTPUT_DIR', 'finetune/checkpoints')
    FINETUNE_BATCH_SIZE: int = int(os.getenv('FINETUNE_BATCH_SIZE', '4'))
    FINETUNE_LEARNING_RATE: float = float(os.getenv('FINETUNE_LEARNING_RATE', '2.0e-4'))
    FINETUNE_EPOCHS: int = int(os.getenv('FINETUNE_EPOCHS', '3'))
    
    # Hardware Configuration
    DEVICE: str = os.getenv('DEVICE', 'auto')
    MIXED_PRECISION: str = os.getenv('MIXED_PRECISION', 'fp16')
    GRADIENT_CHECKPOINTING: bool = os.getenv('GRADIENT_CHECKPOINTING', 'True').lower() == 'true'
    
    # External Services
    WANDB_API_KEY: Optional[str] = os.getenv('WANDB_API_KEY')
    HUGGINGFACE_TOKEN: Optional[str] = os.getenv('HUGGINGFACE_TOKEN')
    
    # File Paths
    BASE_DIR: Path = Path(__file__).parent.parent
    LOGS_DIR: Path = BASE_DIR / 'logs'
    CONFIG_DIR: Path = BASE_DIR / 'config'
    MODELS_DIR: Path = BASE_DIR / MODEL_DIR
    
    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.FLASK_ENV == 'development'
    
    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.FLASK_ENV == 'production'
    
    @property
    def model_path(self) -> Path:
        """Get full model path."""
        return self.MODELS_DIR / self.MODEL_NAME
    
    def validate(self) -> List[str]:
        """Validate configuration and return list of issues."""
        issues = []
        
        # Check required directories
        if not self.LOGS_DIR.exists():
            try:
                self.LOGS_DIR.mkdir(exist_ok=True)
            except Exception as e:
                issues.append(f"Cannot create logs directory: {e}")
        
        if not self.CONFIG_DIR.exists():
            try:
                self.CONFIG_DIR.mkdir(exist_ok=True)
            except Exception as e:
                issues.append(f"Cannot create config directory: {e}")
        
        # Check model file
        if not self.model_path.exists():
            issues.append(f"Model file not found: {self.model_path}")
        
        # Check API keys
        if not self.API_KEYS and self.is_production:
            issues.append("No API keys configured for production")
        
        # Check security settings
        if self.is_production and self.SECRET_KEY == 'dev-secret-key-change-in-production':
            issues.append("Default secret key being used in production")
        
        return issues
    
    def get_cors_origins(self) -> List[str]:
        """Get CORS origins as a list."""
        if self.CORS_ORIGINS == '*':
            return ['*']
        return [origin.strip() for origin in self.CORS_ORIGINS.split(',')]
    
    def get_database_config(self) -> dict:
        """Get database configuration."""
        return {
            'url': self.DATABASE_URL,
            'echo': self.DEBUG
        }
    
    def get_monitoring_config(self) -> dict:
        """Get monitoring configuration."""
        return {
            'enabled': self.ENABLE_MONITORING,
            'log_retention_days': self.MONITOR_LOG_RETENTION_DAYS,
            'logs_dir': str(self.LOGS_DIR)
        }
    
    def get_finetune_config(self) -> dict:
        """Get fine-tuning configuration."""
        return {
            'output_dir': self.FINETUNE_OUTPUT_DIR,
            'batch_size': self.FINETUNE_BATCH_SIZE,
            'learning_rate': self.FINETUNE_LEARNING_RATE,
            'epochs': self.FINETUNE_EPOCHS,
            'device': self.DEVICE,
            'mixed_precision': self.MIXED_PRECISION,
            'gradient_checkpointing': self.GRADIENT_CHECKPOINTING
        }

# Global settings instance
settings = Settings()

def get_settings() -> Settings:
    """Get the global settings instance."""
    return settings

def validate_settings() -> List[str]:
    """Validate application settings."""
    return settings.validate()

def get_model_config() -> dict:
    """Get model configuration as dictionary."""
    return {
        'model_path': str(settings.model_path),
        'n_ctx': settings.N_CTX,
        'n_threads': settings.N_THREADS,
        'n_gpu_layers': settings.N_GPU_LAYERS,
        'verbose': settings.VERBOSE,
        'temperature': settings.TEMPERATURE,
        'top_p': settings.TOP_P,
        'max_tokens': settings.MAX_TOKENS,
        'repeat_penalty': settings.REPEAT_PENALTY
    }

def get_api_config() -> dict:
    """Get API configuration as dictionary."""
    return {
        'api_keys': settings.API_KEYS,
        'rate_limit_per_hour': settings.RATE_LIMIT_PER_HOUR,
        'secret_key': settings.SECRET_KEY,
        'cors_origins': settings.get_cors_origins()
    }
