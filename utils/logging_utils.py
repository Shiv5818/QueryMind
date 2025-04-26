import sys
import os
from pathlib import Path
from loguru import logger
from config.settings import settings

def setup_logging():
    """Configure application logging with loguru."""
    # Clear any existing handlers
    logger.remove()
    
    # Set up console logging
    log_format = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    
    # Add console handler with appropriate log level
    logger.add(
        sys.stderr,
        format=log_format,
        level=settings.LOG_LEVEL,
        backtrace=True,
        diagnose=True,
    )
    
    # Add file handler for persistent logs
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    logger.add(
        log_dir / "app.log",
        rotation="10 MB",
        retention="1 week",
        format=log_format,
        level=settings.LOG_LEVEL,
        backtrace=True,
        diagnose=True,
    )
    
    # Log startup information
    logger.info(f"Logging initialized at level {settings.LOG_LEVEL}")
    
    return logger