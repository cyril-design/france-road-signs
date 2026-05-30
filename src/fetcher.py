"""HTTP request handling for the web crawler."""

import time
import logging
from typing import Optional, Dict
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from src.config import Config


class Fetcher:
    """Handles HTTP requests with retry logic and rate limiting."""

    def __init__(self, config: Config, logger: logging.Logger):
        """Initialize the fetcher.

        Args:
            config: Configuration object
            logger: Logger instance
        """
        self.config = config
        self.logger = logger
        self.session = self._create_session()
        self.last_request_time = 0.0

    def _create_session(self) -> requests.Session:
        """Create a requests session with retry strategy.

        Returns:
            Configured requests session
        """
        session = requests.Session()

        # Setup retry strategy
        retry_strategy = Retry(
            total=self.config.max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"],
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        # Set headers
        session.headers.update({"User-Agent": self.config.user_agent})

        return session

    def fetch(self, url: str, **kwargs) -> Optional[requests.Response]:
        """Fetch a URL with retry logic and rate limiting.

        Args:
            url: URL to fetch
            **kwargs: Additional arguments to pass to requests

        Returns:
            Response object or None if request fails
        """
        # Rate limiting
        self._apply_rate_limit()

        try:
            self.logger.debug(f"Fetching: {url}")
            response = self.session.get(
                url, timeout=self.config.request_timeout, **kwargs
            )
            response.raise_for_status()
            self.logger.debug(f"Successfully fetched: {url} (Status: {response.status_code})")
            return response

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching {url}: {str(e)}")
            return None

    def _apply_rate_limit(self) -> None:
        """Apply rate limiting based on configuration."""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.config.delay_between_requests:
            sleep_time = self.config.delay_between_requests - elapsed
            self.logger.debug(f"Rate limiting: sleeping for {sleep_time:.2f}s")
            time.sleep(sleep_time)
        self.last_request_time = time.time()

    def close(self) -> None:
        """Close the session."""
        self.session.close()
        self.logger.debug("Fetcher session closed")

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
