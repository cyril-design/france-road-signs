# France Road Signs Web Crawler

A professional, well-structured web crawler application for gathering and analyzing French road signs data. This project demonstrates best practices for web scraping, error handling, logging, and configuration management in Python.

## Features

- 🕷️ Efficient web crawling with configurable settings
- 🔄 Retry logic with exponential backoff
- 📝 Comprehensive logging
- ⚙️ Environment-based configuration
- 🧪 Unit tests included
- 📦 Clean project structure
- 🔒 Respectful crawling (robots.txt, rate limiting)
- 💾 Multiple output formats (JSON, CSV)

## Project Structure

```
france-road-signs/
├── src/
│   ├── __init__.py
│   ├── crawler.py           # Main crawler class
│   ├── fetcher.py           # HTTP request handling
│   ├── parser.py            # HTML parsing utilities
│   ├── storage.py           # Data storage
│   ├── logger.py            # Logging configuration
│   └── config.py            # Configuration management
├── tests/
│   ├── __init__.py
│   ├── test_crawler.py
│   ├── test_fetcher.py
│   └── test_parser.py
├── data/                     # Output data directory
├── logs/                     # Application logs
├── .env.example              # Environment variables template
├── .gitignore
├── requirements.txt          # Python dependencies
├── setup.py                  # Package setup
├── main.py                   # Entry point
└── README.md
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/cyril-design/france-road-signs.git
cd france-road-signs
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your settings
```

## Usage

### Basic Usage

```python
from src.crawler import WebCrawler
from src.config import Config

config = Config()
crawler = WebCrawler(config)
results = crawler.crawl("https://example.com/road-signs")
```

### Command Line

```bash
python main.py --url https://example.com/road-signs --max-pages 10 --output json
```

## Configuration

See `.env.example` for all available configuration options:

- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)
- `REQUEST_TIMEOUT`: Timeout for HTTP requests (seconds)
- `MAX_RETRIES`: Maximum number of retries for failed requests
- `DELAY_BETWEEN_REQUESTS`: Delay between requests (seconds)
- `USER_AGENT`: User agent string
- `OUTPUT_FORMAT`: Output format (json, csv)
- `MAX_PAGES`: Maximum number of pages to crawl

## Testing

Run the test suite:

```bash
pytest tests/ -v
```

With coverage:

```bash
pytest tests/ --cov=src --cov-report=html
```

## Best Practices Implemented

- ✅ Type hints throughout the codebase
- ✅ Comprehensive error handling
- ✅ Structured logging
- ✅ Configuration management via environment variables
- ✅ Separation of concerns (fetching, parsing, storage)
- ✅ Respect for robots.txt and rate limiting
- ✅ Unit tests with pytest
- ✅ Documentation and docstrings
- ✅ Clean git history with meaningful commits

## Dependencies

- `requests`: HTTP library
- `beautifulsoup4`: HTML parsing
- `python-dotenv`: Environment variable management
- `pytest`: Testing framework
- `pytest-cov`: Coverage reporting

## License

MIT License - see LICENSE file for details
