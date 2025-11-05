# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This project is an automated RSS feed generator for Paul Graham's essays. It scrapes paulgraham.com/articles.html, extracts article metadata, and generates an RSS feed that is published via GitHub Pages. The RSS feed updates daily through GitHub Actions.

## Development Setup

This project uses `uv` for Python package management (not pip). Python 3.13 is required.

**Initial setup:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv --python 3.13
source .venv/bin/activate
uv pip install -e .
```

**For development with linting:**
```bash
uv pip install -e ".[dev]"
```

## Common Commands

All development tasks are managed through the Makefile:

- `make ci-run` - Generate the RSS feed (runs `python3 main.py`)
- `make code-format` - Format code using ruff (also available: `ruff check --fix .`)
- `make rss-validate` - Validate the RSS feed using W3C validator (opens in browser)
- `make ci-setup` - Set up Python environment with uv
- `make ci-install` - Install package dependencies
- `make ci-commit` - Commit and push RSS feed changes (used by CI)

**Running the generator:**
```bash
python main.py
```

Set `DEBUG=true` environment variable for verbose logging during development.

## Architecture

### Core Components

**main.py** - Single-file RSS feed generator with three main functions:
- `create_rss_feed()` - Main orchestrator: fetches articles, generates RSS XML, writes output
- `get_article_date(url)` - Scrapes individual article pages to extract publication dates using regex patterns (tries "Month YYYY" then fallback to just "YYYY")
- `generate_rss_xml(articles)` - Constructs RFC-compliant RSS 2.0 XML with Atom namespace

**src/paulgraham_rss/scripts/** - Utility scripts (not part of main RSS generation flow):
- `save.py` - Converts JSON/HTML input to HTML format (utility script)
- `readability.js` - Browser script for extracting readable content using Mozilla Readability

### Key Implementation Details

**Date extraction strategy:**
The RSS feed requires publication dates, but Paul Graham's articles don't have consistent date metadata. The `get_article_date()` function:
1. Fetches each article's HTML
2. Searches text for "Month YYYY" patterns (e.g., "March 2025")
3. Falls back to searching for standalone years (e.g., "1997")
4. Returns current date if no pattern found, or 1970-01-01 on errors

**Special date handling:**
Certain articles have hardcoded dates because their content lacks reliable date information:
- `progbot.html` - Fixed to January 1, 1997
- `noop.html` and `fix.html` - Fixed to March 16, 2002 (chronologically placed between specific essays)

**Duplicate prevention:**
The `generate_rss_xml()` function deduplicates articles by URL using a set before generating XML items.

### Dependencies

Core dependencies (defined in pyproject.toml):
- `requests` - HTTP fetching
- `beautifulsoup4` + `lxml` - HTML parsing
- `feedgen` - Listed but not actually imported in main.py (RSS XML is manually constructed)

Dev dependencies:
- `ruff` - Linting and formatting (configured for Python 3.13, line length 88)

## CI/CD Pipeline

GitHub Actions workflow (`.github/workflows/build.yml`) runs daily at 1:05 AM UTC:
1. Checks out repo with full history (`fetch-depth: 0`)
2. Sets up Python environment via `make ci-setup`
3. Installs dependencies via `make ci-install`
4. Generates RSS feed via `make ci-run`
5. Commits and pushes changes via `make ci-commit` (only if rss.xml changed)

**Authentication:** Requires `RSS_BOT_GITHUB_TOKEN` secret with `repo` scope for automated commits.

**Manual triggering:** Workflow supports `workflow_dispatch` with optional `debug` input for verbose logging.

## Code Style

Ruff configuration (pyproject.toml):
- Line length: 88 characters
- Target: Python 3.13
- Selected rules: E, F, I, N, W, B, UP, PL, RUF
- First-party imports: `paulgraham_rss`

Format code before committing: `make code-format`

## Output

Generated `rss.xml` is committed to the repository and served via GitHub Pages at:
https://program247365.github.io/paulgraham-rss/rss.xml
