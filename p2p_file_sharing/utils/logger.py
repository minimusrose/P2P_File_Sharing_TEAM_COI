"""Configuration du système de logs"""
import logging
from .config import LOG_FILE

def setup_logger(name='P2P'):
    """Configure le logger pour l'application"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Console handler
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    
    # File handler
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setLevel(logging.DEBUG)
    
    # Format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    logger.addHandler(console)
    logger.addHandler(file_handler)
    
    return logger
