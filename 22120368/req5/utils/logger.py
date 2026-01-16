"""
Logger utility for consistent logging across the project
"""
import logging
import os
from datetime import datetime
from config.config import Config


class Logger:
    """Custom logger class for test automation"""
    
    @staticmethod
    def get_logger(name=__name__):
        """
        Get a configured logger instance
        
        Args:
            name: Logger name (typically __name__ from calling module)
            
        Returns:
            Configured logger instance
        """
        logger = logging.getLogger(name)
        
        # Only add handlers if logger doesn't have any
        if not logger.handlers:
            logger.setLevel(logging.DEBUG)
            
            # Create logs directory if it doesn't exist
            log_dir = Config.REPORT_PATH
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
            
            # File handler for all logs
            log_file = os.path.join(
                log_dir, 
                f"automation_{datetime.now().strftime('%Y%m%d')}.log"
            )
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.DEBUG)
            
            # Console handler for important logs
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            
            # Formatter
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)
            
            logger.addHandler(file_handler)
            logger.addHandler(console_handler)
        
        return logger
    
    @staticmethod
    def log_test_start(test_name):
        """Log the start of a test"""
        logger = Logger.get_logger()
        logger.info("=" * 80)
        logger.info(f"Starting Test: {test_name}")
        logger.info("=" * 80)
    
    @staticmethod
    def log_test_end(test_name, status="PASSED"):
        """Log the end of a test"""
        logger = Logger.get_logger()
        logger.info("=" * 80)
        logger.info(f"Test {status}: {test_name}")
        logger.info("=" * 80)
