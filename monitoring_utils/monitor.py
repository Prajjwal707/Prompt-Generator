"""
Monitoring and logging utilities for PromptGenius.
Provides request logging, error tracking, and performance monitoring.
"""

import logging
import time
import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from collections import defaultdict, deque
import threading

class RequestMonitor:
    """Monitors API requests and performance metrics."""
    
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Performance metrics
        self.request_times = deque(maxlen=1000)  # Last 1000 requests
        self.error_counts = defaultdict(int)
        self.endpoint_counts = defaultdict(int)
        self.hourly_stats = defaultdict(lambda: defaultdict(int))
        
        # Thread safety
        self.lock = threading.Lock()
        
        # Setup loggers
        self.setup_loggers()
    
    def setup_loggers(self):
        """Setup dedicated loggers for monitoring."""
        # Request logger
        self.request_logger = logging.getLogger('request_monitor')
        self.request_logger.setLevel(logging.INFO)
        
        request_handler = logging.FileHandler(self.log_dir / 'requests.log')
        request_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        request_handler.setFormatter(request_formatter)
        self.request_logger.addHandler(request_handler)
        
        # Error logger
        self.error_logger = logging.getLogger('error_monitor')
        self.error_logger.setLevel(logging.ERROR)
        
        error_handler = logging.FileHandler(self.log_dir / 'errors.log')
        error_handler.setFormatter(request_formatter)
        self.error_logger.addHandler(error_handler)
        
        # Performance logger
        self.perf_logger = logging.getLogger('performance_monitor')
        self.perf_logger.setLevel(logging.INFO)
        
        perf_handler = logging.FileHandler(self.log_dir / 'performance.log')
        perf_handler.setFormatter(request_formatter)
        self.perf_logger.addHandler(perf_handler)
    
    def log_request(self, endpoint: str, method: str, status_code: int, 
                   response_time: float, user_id: Optional[str] = None,
                   api_key: Optional[str] = None):
        """Log API request details."""
        with self.lock:
            # Update metrics
            self.request_times.append(response_time)
            self.endpoint_counts[f"{method} {endpoint}"] += 1
            
            if status_code >= 400:
                self.error_counts[f"{method} {endpoint}"] += 1
            
            # Hourly stats
            current_hour = datetime.now().strftime("%Y-%m-%d %H:00")
            self.hourly_stats[current_hour][f"{method} {endpoint}"] += 1
            
            # Log to file
            log_data = {
                'timestamp': datetime.now().isoformat(),
                'endpoint': endpoint,
                'method': method,
                'status_code': status_code,
                'response_time': round(response_time, 3),
                'user_id': user_id,
                'api_key': api_key[:8] + '...' if api_key else None
            }
            
            self.request_logger.info(json.dumps(log_data))
            
            # Performance log
            if response_time > 5.0:  # Log slow requests
                self.perf_logger.warning(f"Slow request: {log_data}")
    
    def log_error(self, error: Exception, endpoint: str, method: str,
                  user_id: Optional[str] = None):
        """Log error details."""
        with self.lock:
            error_data = {
                'timestamp': datetime.now().isoformat(),
                'endpoint': endpoint,
                'method': method,
                'error_type': type(error).__name__,
                'error_message': str(error),
                'user_id': user_id
            }
            
            self.error_logger.error(json.dumps(error_data))
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get current performance statistics."""
        with self.lock:
            if not self.request_times:
                return {
                    'avg_response_time': 0,
                    'min_response_time': 0,
                    'max_response_time': 0,
                    'p95_response_time': 0,
                    'total_requests': 0
                }
            
            times = list(self.request_times)
            times.sort()
            
            return {
                'avg_response_time': round(sum(times) / len(times), 3),
                'min_response_time': round(min(times), 3),
                'max_response_time': round(max(times), 3),
                'p95_response_time': round(times[int(len(times) * 0.95)], 3),
                'total_requests': len(times)
            }
    
    def get_error_stats(self) -> Dict[str, Any]:
        """Get error statistics."""
        with self.lock:
            total_errors = sum(self.error_counts.values())
            total_requests = sum(self.endpoint_counts.values())
            
            error_rate = (total_errors / total_requests * 100) if total_requests > 0 else 0
            
            return {
                'total_errors': total_errors,
                'total_requests': total_requests,
                'error_rate': round(error_rate, 2),
                'error_breakdown': dict(self.error_counts)
            }
    
    def get_endpoint_stats(self) -> Dict[str, Any]:
        """Get endpoint usage statistics."""
        with self.lock:
            return dict(self.endpoint_counts)
    
    def get_hourly_stats(self, hours: int = 24) -> Dict[str, Any]:
        """Get hourly statistics for the last N hours."""
        with self.lock:
            cutoff_time = datetime.now() - timedelta(hours=hours)
            
            filtered_stats = {}
            for hour_key, stats in self.hourly_stats.items():
                hour_dt = datetime.strptime(hour_key, "%Y-%m-%d %H:00")
                if hour_dt >= cutoff_time:
                    filtered_stats[hour_key] = dict(stats)
            
            return filtered_stats
    
    def cleanup_old_logs(self, days: int = 30):
        """Clean up old log files."""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        for log_file in self.log_dir.glob("*.log*"):
            try:
                file_time = datetime.fromtimestamp(log_file.stat().st_mtime)
                if file_time < cutoff_date:
                    log_file.unlink()
                    logging.info(f"Deleted old log file: {log_file}")
            except Exception as e:
                logging.error(f"Error deleting log file {log_file}: {e}")

class ModelMonitor:
    """Monitors model performance and resource usage."""
    
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Model metrics
        self.generation_times = deque(maxlen=100)
        self.token_counts = deque(maxlen=100)
        self.model_load_times = deque(maxlen=10)
        
        # Setup logger
        self.model_logger = logging.getLogger('model_monitor')
        self.model_logger.setLevel(logging.INFO)
        
        model_handler = logging.FileHandler(self.log_dir / 'model.log')
        model_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        model_handler.setFormatter(model_formatter)
        self.model_logger.addHandler(model_handler)
    
    def log_generation(self, prompt_length: int, response_length: int, 
                      generation_time: float, task_type: str):
        """Log model generation metrics."""
        self.generation_times.append(generation_time)
        self.token_counts.append(prompt_length + response_length)
        
        log_data = {
            'timestamp': datetime.now().isoformat(),
            'prompt_length': prompt_length,
            'response_length': response_length,
            'generation_time': round(generation_time, 3),
            'tokens_per_second': round((prompt_length + response_length) / generation_time, 2) if generation_time > 0 else 0,
            'task_type': task_type
        }
        
        self.model_logger.info(json.dumps(log_data))
    
    def log_model_load(self, model_path: str, load_time: float, success: bool):
        """Log model loading metrics."""
        self.model_load_times.append(load_time)
        
        log_data = {
            'timestamp': datetime.now().isoformat(),
            'model_path': model_path,
            'load_time': round(load_time, 3),
            'success': success
        }
        
        self.model_logger.info(json.dumps(log_data))
    
    def get_model_stats(self) -> Dict[str, Any]:
        """Get model performance statistics."""
        if not self.generation_times:
            return {
                'avg_generation_time': 0,
                'avg_tokens_per_second': 0,
                'total_generations': 0
            }
        
        avg_gen_time = sum(self.generation_times) / len(self.generation_times)
        total_tokens = sum(self.token_counts)
        total_time = sum(self.generation_times)
        
        return {
            'avg_generation_time': round(avg_gen_time, 3),
            'avg_tokens_per_second': round(total_tokens / total_time, 2) if total_time > 0 else 0,
            'total_generations': len(self.generation_times),
            'total_tokens_generated': total_tokens
        }

class HealthMonitor:
    """Monitors application health and resource usage."""
    
    def __init__(self):
        self.start_time = datetime.now()
        self.last_check = datetime.now()
        
        try:
            import psutil
            self.psutil = psutil
            self.psutil_available = True
        except ImportError:
            self.psutil_available = False
            logging.warning("psutil not available, resource monitoring disabled")
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get system resource statistics."""
        if not self.psutil_available:
            return {
                'cpu_percent': 'N/A',
                'memory_percent': 'N/A',
                'disk_usage': 'N/A'
            }
        
        try:
            cpu_percent = self.psutil.cpu_percent(interval=1)
            memory = self.psutil.virtual_memory()
            disk = self.psutil.disk_usage('/')
            
            return {
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'memory_available_gb': round(memory.available / (1024**3), 2),
                'disk_usage_percent': disk.percent,
                'disk_free_gb': round(disk.free / (1024**3), 2)
            }
        except Exception as e:
            logging.error(f"Error getting system stats: {e}")
            return {
                'cpu_percent': 'Error',
                'memory_percent': 'Error',
                'disk_usage': 'Error'
            }
    
    def get_application_stats(self) -> Dict[str, Any]:
        """Get application runtime statistics."""
        uptime = datetime.now() - self.start_time
        
        return {
            'start_time': self.start_time.isoformat(),
            'uptime_seconds': int(uptime.total_seconds()),
            'uptime_formatted': str(uptime).split('.')[0],
            'last_check': self.last_check.isoformat()
        }
    
    def health_check(self) -> Dict[str, Any]:
        """Perform comprehensive health check."""
        health_status = {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'checks': {}
        }
        
        # Check system resources
        system_stats = self.get_system_stats()
        health_status['checks']['system'] = system_stats
        
        # Check application uptime
        app_stats = self.get_application_stats()
        health_status['checks']['application'] = app_stats
        
        # Determine overall health
        if self.psutil_available:
            if system_stats['cpu_percent'] > 90:
                health_status['status'] = 'degraded'
                health_status['warnings'] = ['High CPU usage']
            
            if system_stats['memory_percent'] > 90:
                health_status['status'] = 'degraded'
                if 'warnings' not in health_status:
                    health_status['warnings'] = []
                health_status['warnings'].append('High memory usage')
        
        self.last_check = datetime.now()
        return health_status

# Global monitor instances
request_monitor = RequestMonitor()
model_monitor = ModelMonitor()
health_monitor = HealthMonitor()

def get_request_monitor() -> RequestMonitor:
    """Get the global request monitor instance."""
    return request_monitor

def get_model_monitor() -> ModelMonitor:
    """Get the global model monitor instance."""
    return model_monitor

def get_health_monitor() -> HealthMonitor:
    """Get the global health monitor instance."""
    return health_monitor
