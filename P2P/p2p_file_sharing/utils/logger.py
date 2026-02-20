"""Configuration du système de logs"""
import logging
from .config import LOG_FILE

def setup_logger(name='P2P'):
    """Configure le logger pour l'application"""
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(logging.DEBUG)
    
    # Console handler
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    
    # File handler
    try:
        file_handler = logging.FileHandler(LOG_FILE)
        file_handler.setLevel(logging.DEBUG)
    except Exception:
        file_handler = None

    # Format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console.setFormatter(formatter)
    if file_handler:
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    logger.addHandler(console)
    
    return logger
