"""Main entry point for the web crawler application."""

import argparse
import logging
from src.config import Config
from src.crawler import WebCrawler


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="France Road Signs Web Crawler",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --url https://example.com
  python main.py --url https://example.com --max-pages 50 --output json
        """,
    )

    parser.add_argument(
        "--url",
        required=True,
        help="Starting URL to crawl",
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        help="Maximum number of pages to crawl",
    )
    parser.add_argument(
        "--output",
        choices=["json", "csv"],
        help="Output format",
    )
    parser.add_argument(
        "--env",
        default=".env",
        help="Path to .env configuration file",
    )

    args = parser.parse_args()

    # Load configuration
    config = Config(args.env)

    # Override config with command line arguments
    if args.max_pages:
        config.max_pages = args.max_pages
    if args.output:
        config.output_format = args.output

    # Create and run crawler
    try:
        with WebCrawler(config) as crawler:
            results = crawler.crawl(args.url)
            crawler.save_results("road_signs_data")

            print(f"\n✓ Crawl completed successfully!")
            print(f"  Total pages crawled: {len(results)}")
            print(f"  Output format: {config.output_format}")
            print(f"  Output directory: {config.output_dir}")

    except Exception as e:
        logging.error(f"Fatal error: {str(e)}", exc_info=True)
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
