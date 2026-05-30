"""Main web crawler implementation."""

import logging
from typing import List, Dict, Any, Optional, Set
from src.config import Config
from src.logger import setup_logger
from src.fetcher import Fetcher
from src.parser import Parser
from src.storage import Storage


class WebCrawler:
    """Main web crawler class."""

    def __init__(self, config: Config):
        """Initialize the web crawler.

        Args:
            config: Configuration object
        """
        self.config = config
        self.logger = setup_logger(config)
        self.fetcher = Fetcher(config, self.logger)
        self.parser = Parser(self.logger)
        self.storage = Storage(config, self.logger)
        self.visited_urls: Set[str] = set()
        self.results: List[Dict[str, Any]] = []

        self.logger.info(f"Web Crawler initialized with config: {config}")

    def crawl(
        self, start_url: str, max_pages: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Crawl a website starting from the given URL.

        Args:
            start_url: Starting URL to crawl
            max_pages: Maximum number of pages to crawl (uses config if not specified)

        Returns:
            List of crawled data
        """
        max_pages = max_pages or self.config.max_pages
        self.logger.info(f"Starting crawl from {start_url}")

        urls_to_crawl = [start_url]
        self.results = []
        self.visited_urls = set()

        while urls_to_crawl and len(self.visited_urls) < max_pages:
            url = urls_to_crawl.pop(0)

            if url in self.visited_urls:
                continue

            self.visited_urls.add(url)

            # Fetch and parse the page
            response = self.fetcher.fetch(url)
            if not response:
                continue

            soup = self.parser.parse_html(response.text, url)
            if not soup:
                continue

            # Extract data
            page_data = {
                "url": url,
                "title": self.parser.extract_metadata(soup).get("title", ""),
                "description": self.parser.extract_metadata(soup).get(
                    "description", ""
                ),
                "text_length": len(self.parser.extract_text(soup)),
            }
            self.results.append(page_data)

            # Extract new links
            new_links = self.parser.extract_links(soup, url)
            for link in new_links:
                if link not in self.visited_urls and len(urls_to_crawl) < max_pages:
                    urls_to_crawl.append(link)

            self.logger.info(
                f"Crawled {len(self.visited_urls)}/{max_pages} pages"
            )

        self.logger.info(
            f"Crawl completed. Total pages crawled: {len(self.visited_urls)}"
        )
        return self.results

    def save_results(self, filename: str = "crawl_results") -> bool:
        """Save crawl results to file.

        Args:
            filename: Output filename (without extension)

        Returns:
            True if successful, False otherwise
        """
        if not self.results:
            self.logger.warning("No results to save")
            return False

        filename_with_timestamp = self.storage.get_filename_with_timestamp(
            filename
        )
        return self.storage.save_data(self.results, filename_with_timestamp)

    def close(self) -> None:
        """Close the crawler and clean up resources."""
        self.fetcher.close()
        self.logger.info("Crawler closed")

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
