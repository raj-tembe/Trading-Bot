"""
Logging configuration for the trading bot.
Sets up file and console handlers for structured logging.
"""
import logging
import os


def setup_logging(log_file: str = "trading_bot.log") -> logging.Logger:
    """
    Configure logging with file and console handlers.
    
    Args:
        log_file: Path to the log file (default: trading_bot.log)
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger("trading_bot")
    logger.setLevel(logging.DEBUG)
    
    # Prevent adding duplicate handlers
    if logger.handlers:
        return logger
    
    # Create formatters
    log_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # File handler (DEBUG level - captures everything)
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)
    
    # Console handler (INFO level - user-facing)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)
    
    return logger
