"""Tests for configuration module."""

import os
import pytest
from src.config import Config


@pytest.fixture
def temp_env_file(tmp_path):
    """Create a temporary .env file."""
    env_file = tmp_path / ".env"
    env_file.write_text(
        """
LOG_LEVEL=DEBUG
REQUEST_TIMEOUT=20
MAX_RETRIES=5
"""
    )
    return str(env_file)


def test_config_initialization(temp_env_file):
    """Test configuration initialization."""
    config = Config(temp_env_file)
    assert config.log_level == "DEBUG"
    assert config.request_timeout == 20
    assert config.max_retries == 5


def test_config_default_values():
    """Test configuration default values."""
    config = Config()
    assert config.log_level == "INFO"
    assert config.request_timeout == 10
    assert config.max_retries == 3


def test_config_output_directory_creation(tmp_path):
    """Test that output directory is created."""
    env_file = tmp_path / ".env"
    env_file.write_text(f"OUTPUT_DIR={tmp_path / 'test_output'}\n")
    
    config = Config(str(env_file))
    assert os.path.exists(config.output_dir)


def test_config_repr():
    """Test configuration string representation."""
    config = Config()
    repr_str = repr(config)
    assert "Config(" in repr_str
    assert "log_level" in repr_str
