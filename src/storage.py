"""Data storage utilities for the web crawler."""

import json
import csv
import logging
from typing import List, Dict, Any
from pathlib import Path
from datetime import datetime


class Storage:
    """Handles data storage in various formats."""

    def __init__(self, config, logger: logging.Logger):
        """Initialize storage handler.

        Args:
            config: Configuration object
            logger: Logger instance
        """
        self.config = config
        self.logger = logger
        self.output_dir = Path(config.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def save_data(self, data: List[Dict[str, Any]], filename: str) -> bool:
        """Save data in the configured format.

        Args:
            data: List of data dictionaries to save
            filename: Output filename (without extension)

        Returns:
            True if successful, False otherwise
        """
        try:
            if self.config.output_format == "json":
                return self._save_json(data, filename)
            elif self.config.output_format == "csv":
                return self._save_csv(data, filename)
            else:
                self.logger.error(
                    f"Unknown output format: {self.config.output_format}"
                )
                return False
        except Exception as e:
            self.logger.error(f"Error saving data: {str(e)}")
            return False

    def _save_json(self, data: List[Dict[str, Any]], filename: str) -> bool:
        """Save data as JSON.

        Args:
            data: List of data dictionaries
            filename: Output filename (without extension)

        Returns:
            True if successful, False otherwise
        """
        try:
            filepath = self.output_dir / f"{filename}.json"
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Data saved to {filepath}")
            return True
        except Exception as e:
            self.logger.error(f"Error saving JSON: {str(e)}")
            return False

    def _save_csv(self, data: List[Dict[str, Any]], filename: str) -> bool:
        """Save data as CSV.

        Args:
            data: List of data dictionaries
            filename: Output filename (without extension)

        Returns:
            True if successful, False otherwise
        """
        try:
            if not data:
                self.logger.warning("No data to save")
                return False

            filepath = self.output_dir / f"{filename}.csv"
            fieldnames = data[0].keys()

            with open(filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)

            self.logger.info(f"Data saved to {filepath}")
            return True
        except Exception as e:
            self.logger.error(f"Error saving CSV: {str(e)}")
            return False

    def get_filename_with_timestamp(self, base_name: str) -> str:
        """Generate filename with timestamp.

        Args:
            base_name: Base filename

        Returns:
            Filename with timestamp
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{base_name}_{timestamp}"
