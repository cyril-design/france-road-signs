"""HTML parsing utilities for the web crawler."""

import logging
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import requests


class Parser:
    """Handles HTML parsing and data extraction."""

    def __init__(self, logger: logging.Logger):
        """Initialize the parser.

        Args:
            logger: Logger instance
        """
        self.logger = logger

    def parse_html(self, html_content: str, base_url: str) -> Optional[BeautifulSoup]:
        """Parse HTML content.

        Args:
            html_content: HTML content to parse
            base_url: Base URL for resolving relative URLs

        Returns:
            BeautifulSoup object or None if parsing fails
        """
        try:
            soup = BeautifulSoup(html_content, "lxml")
            self.logger.debug("Successfully parsed HTML content")
            return soup
        except Exception as e:
            self.logger.error(f"Error parsing HTML: {str(e)}")
            return None

    def extract_links(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """Extract all links from parsed HTML.

        Args:
            soup: BeautifulSoup object
            base_url: Base URL for resolving relative URLs

        Returns:
            List of absolute URLs
        """
        links = []
        try:
            for link in soup.find_all("a", href=True):
                url = urljoin(base_url, link["href"])
                # Only include same-domain links
                if self._is_same_domain(url, base_url):
                    links.append(url)
            self.logger.debug(f"Extracted {len(links)} links")
            return links
        except Exception as e:
            self.logger.error(f"Error extracting links: {str(e)}")
            return []

    def extract_text(self, soup: BeautifulSoup) -> str:
        """Extract text content from HTML.

        Args:
            soup: BeautifulSoup object

        Returns:
            Extracted text
        """
        try:
            text = soup.get_text(separator=" ", strip=True)
            self.logger.debug(f"Extracted {len(text)} characters of text")
            return text
        except Exception as e:
            self.logger.error(f"Error extracting text: {str(e)}")
            return ""

    def extract_metadata(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Extract metadata from HTML.

        Args:
            soup: BeautifulSoup object

        Returns:
            Dictionary of metadata
        """
        metadata = {}
        try:
            # Title
            title_tag = soup.find("title")
            metadata["title"] = title_tag.string if title_tag else ""

            # Meta description
            meta_desc = soup.find("meta", attrs={"name": "description"})
            metadata["description"] = (
                meta_desc.get("content", "") if meta_desc else ""
            )

            # Meta keywords
            meta_keywords = soup.find("meta", attrs={"name": "keywords"})
            metadata["keywords"] = (
                meta_keywords.get("content", "") if meta_keywords else ""
            )

            self.logger.debug("Successfully extracted metadata")
            return metadata
        except Exception as e:
            self.logger.error(f"Error extracting metadata: {str(e)}")
            return metadata

    @staticmethod
    def _is_same_domain(url: str, base_url: str) -> bool:
        """Check if URL is from the same domain.

        Args:
            url: URL to check
            base_url: Base URL

        Returns:
            True if same domain, False otherwise
        """
        try:
            url_domain = urlparse(url).netloc
            base_domain = urlparse(base_url).netloc
            return url_domain == base_domain
        except Exception:
            return False
