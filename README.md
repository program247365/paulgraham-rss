# Paul Graham RSS Feed Generator

This project generates an RSS feed from Paul Graham's essays, making them easily accessible through your favorite RSS reader.

## RSS Feed URL

The RSS feed is available at: [https://program247365.github.io/paulgraham-rss/rss.xml](https://program247365.github.io/paulgraham-rss/rss.xml)

## Features

- Automatically fetches and parses Paul Graham's essays
- Generates a clean, well-formatted RSS feed
- Updates daily through GitHub Actions
- Maintains a local cache of essays to avoid unnecessary requests

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/paulgraham-rss.git
   cd paulgraham-rss
   ```

2. Install dependencies using `uv`:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   uv venv --python 3.13
   . .venv/bin/activate
   uv pip install -e .
   ```

## Usage

Run the script to generate the RSS feed:
```bash
python main.py
```

The generated RSS feed will be saved as `rss.xml` in the project root.

## Makefile Tasks

The project includes a Makefile with CI-specific tasks:

- `make ci-setup`: Sets up the Python environment
- `make ci-install`: Installs project dependencies
- `make ci-run`: Generates the RSS feed
- `make ci-commit`: Commits and pushes changes if the RSS feed has been updated

## CI/CD Setup

The project uses GitHub Actions to automatically update the RSS feed. The workflow runs:
- Daily at 1:05 AM UTC
- On manual trigger through the GitHub Actions interface

To set this up:
1. Create a Personal Access Token (PAT) with `repo` scope
2. Add it to your repository's secrets as `RSS_BOT_GITHUB_TOKEN`

## License

MIT License - see LICENSE file for details
