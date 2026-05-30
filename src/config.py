"""Configuration management for the web crawler."""

import os
from typing import Optional
from dotenv import load_dotenv


class Config:
    """Configuration class for the web crawler."""

    def __init__(self, env_file: str = ".env"):
        """Initialize configuration from environment variables.

        Args:
            env_file: Path to the .env file
        """
        load_dotenv(env_file)

        # Logging Configuration
        self.log_level: str = os.getenv("LOG_LEVEL", "INFO")
        self.log_file: str = os.getenv("LOG_FILE", "logs/crawler.log")

        # Request Configuration
        self.request_timeout: int = int(os.getenv("REQUEST_TIMEOUT", "10"))
        self.max_retries: int = int(os.getenv("MAX_RETRIES", "3"))
        self.delay_between_requests: float = float(
            os.getenv("DELAY_BETWEEN_REQUESTS", "1")
        )

        # HTTP Headers
        self.user_agent: str = os.getenv(
            "USER_AGENT",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        )

        # Crawler Configuration
        self.max_pages: int = int(os.getenv("MAX_PAGES", "100"))
        self.output_format: str = os.getenv("OUTPUT_FORMAT", "json")
        self.output_dir: str = os.getenv("OUTPUT_DIR", "data")

        # Rate Limiting
        self.respect_robots_txt: bool = (
            os.getenv("RESPECT_ROBOTS_TXT", "True").lower() == "true"
        )
        self.crawl_delay: float = float(os.getenv("CRAWL_DELAY", "1"))

        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)

    def __repr__(self) -> str:
        """Return string representation of configuration."""
        return (
            f"Config(log_level={self.log_level}, "
            f"request_timeout={self.request_timeout}, "
            f"max_retries={self.max_retries}, "
            f"max_pages={self.max_pages})"
        )
