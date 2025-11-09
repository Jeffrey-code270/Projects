import logging
import time
import psutil
import json
from datetime import datetime
from functools import wraps

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/logs/app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class MetricsCollector:
    def __init__(self):
        self.metrics = {
            'pdfs_processed': 0,
            'keywords_extracted': 0,
            'processing_time': [],
            'errors': 0
        }
    
    def log_pdf_processed(self, filename, processing_time, keyword_count):
        self.metrics['pdfs_processed'] += 1
        self.metrics['keywords_extracted'] += keyword_count
        self.metrics['processing_time'].append(processing_time)
        
        logger.info(f"PDF processed: {filename}, Time: {processing_time:.2f}s, Keywords: {keyword_count}")
    
    def log_error(self, error_msg):
        self.metrics['errors'] += 1
        logger.error(f"Processing error: {error_msg}")
    
    def get_system_metrics(self):
        return {
            'cpu_percent': psutil.cpu_percent(),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_usage': psutil.disk_usage('/').percent,
            'timestamp': datetime.now().isoformat()
        }
    
    def export_metrics(self):
        system_metrics = self.get_system_metrics()
        app_metrics = {
            'pdfs_processed': self.metrics['pdfs_processed'],
            'total_keywords': self.metrics['keywords_extracted'],
            'avg_processing_time': sum(self.metrics['processing_time']) / len(self.metrics['processing_time']) if self.metrics['processing_time'] else 0,
            'error_count': self.metrics['errors']
        }
        
        metrics_data = {**system_metrics, **app_metrics}
        
        with open('/app/logs/metrics.json', 'w') as f:
            json.dump(metrics_data, f, indent=2)
        
        return metrics_data

def monitor_performance(func):
    """Decorator to monitor function performance."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            end_time = time.time()
            logger.info(f"{func.__name__} completed in {end_time - start_time:.2f}s")
            return result
        except Exception as e:
            logger.error(f"{func.__name__} failed: {str(e)}")
            raise
    return wrapper