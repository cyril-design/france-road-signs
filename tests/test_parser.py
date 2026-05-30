"""Tests for parser module."""

import pytest
from src.parser import Parser
from src.logger import setup_logger
from src.config import Config


@pytest.fixture
def logger():
    """Create a test logger."""
    config = Config()
    return setup_logger(config)


@pytest.fixture
def parser(logger):
    """Create a test parser."""
    return Parser(logger)


def test_parser_initialization(parser):
    """Test parser initialization."""
    assert parser is not None
    assert parser.logger is not None


def test_parse_html(parser):
    """Test HTML parsing."""
    html = "<html><body><p>Test content</p></body></html>"
    soup = parser.parse_html(html, "https://example.com")
    assert soup is not None
    assert soup.find("p").text == "Test content"


def test_extract_text(parser):
    """Test text extraction."""
    html = "<html><body><p>Hello</p><p>World</p></body></html>"
    soup = parser.parse_html(html, "https://example.com")
    text = parser.extract_text(soup)
    assert "Hello" in text
    assert "World" in text


def test_extract_metadata(parser):
    """Test metadata extraction."""
    html = """
    <html>
        <head>
            <title>Test Page</title>
            <meta name="description" content="Test description">
            <meta name="keywords" content="test, keywords">
        </head>
    </html>
    """
    soup = parser.parse_html(html, "https://example.com")
    metadata = parser.extract_metadata(soup)
    
    assert metadata["title"] == "Test Page"
    assert metadata["description"] == "Test description"
    assert metadata["keywords"] == "test, keywords"


def test_extract_links(parser):
    """Test link extraction."""
    html = """
    <html>
        <body>
            <a href="/page1">Page 1</a>
            <a href="/page2">Page 2</a>
            <a href="https://external.com">External</a>
        </body>
    </html>
    """
    soup = parser.parse_html(html, "https://example.com")
    links = parser.extract_links(soup, "https://example.com")
    
    assert len(links) >= 2
    assert any("example.com/page1" in link for link in links)
    assert any("example.com/page2" in link for link in links)


def test_is_same_domain():
    """Test domain checking."""
    assert Parser._is_same_domain(
        "https://example.com/page1",
        "https://example.com/page2"
    ) is True
    
    assert Parser._is_same_domain(
        "https://other.com/page1",
        "https://example.com/page2"
    ) is False
