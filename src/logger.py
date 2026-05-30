"""Logging configuration for the web crawler."""

import logging
import logging.handlers
from typing import Optional
from src.config import Config


def setup_logger(config: Config) -> logging.Logger:
    """Setup logging configuration.

    Args:
        config: Configuration object

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger("crawler")
    logger.setLevel(getattr(logging, config.log_level))

    # Create formatters
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # File handler
    file_handler = logging.handlers.RotatingFileHandler(
        config.log_file, maxBytes=10485760, backupCount=5  # 10MB
    )
    file_handler.setLevel(getattr(logging, config.log_level))
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, config.log_level))
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
