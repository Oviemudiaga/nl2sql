import logging
import sys

def setup_logging(name: str) -> logging.Logger:
    """Setup logging configuration."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Console handler - prints to terminal
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    
    # Formatter - how messages look
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    
    # Avoid duplicate handlers
    if not logger.handlers:
        logger.addHandler(handler)
    
    return logger