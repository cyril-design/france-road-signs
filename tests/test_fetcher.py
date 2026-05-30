"""Tests for fetcher module."""

import pytest
from unittest.mock import Mock, patch
from src.config import Config
from src.fetcher import Fetcher
from src.logger import setup_logger


@pytest.fixture
def config():
    """Create a test configuration."""
    return Config()


@pytest.fixture
def logger(config):
    """Create a test logger."""
    return setup_logger(config)


@pytest.fixture
def fetcher(config, logger):
    """Create a test fetcher."""
    return Fetcher(config, logger)


def test_fetcher_initialization(fetcher):
    """Test fetcher initialization."""
    assert fetcher.config is not None
    assert fetcher.session is not None
    assert fetcher.last_request_time == 0.0


def test_fetcher_session_creation(fetcher):
    """Test that session is properly configured."""
    assert fetcher.session is not None
    assert "User-Agent" in fetcher.session.headers


@patch("requests.Session.get")
def test_fetcher_fetch_success(mock_get, fetcher):
    """Test successful fetch."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = "<html></html>"
    mock_get.return_value = mock_response

    result = fetcher.fetch("https://example.com")
    assert result is not None


@patch("requests.Session.get")
def test_fetcher_fetch_failure(mock_get, fetcher):
    """Test fetch failure handling."""
    mock_get.side_effect = Exception("Connection error")

    result = fetcher.fetch("https://example.com")
    assert result is None


def test_fetcher_context_manager(config, logger):
    """Test context manager functionality."""
    with Fetcher(config, logger) as fetcher:
        assert fetcher is not None
