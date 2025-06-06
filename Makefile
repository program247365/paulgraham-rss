.PHONY: help ci-setup ci-install ci-run ci-commit code-format rss-validate

# Default target
.DEFAULT_GOAL := help

# Help task
help:
	@echo "Available targets:"
	@echo "  help         - Show this help message"
	@echo "  ci-setup     - Install uv and create virtual environment"
	@echo "  ci-install   - Install package in development mode"
	@echo "  ci-run       - Run the main Python script"
	@echo "  ci-commit    - Commit and push changes to git"
	@echo "  code-format  - Format code using ruff"
	@echo "  rss-validate - Validate the RSS feed using W3C validator"

# CI-specific tasks
ci-setup:
	curl -LsSf https://astral.sh/uv/install.sh | sh
	uv venv --python 3.13
	. .venv/bin/activate

ci-install:
	. .venv/bin/activate && uv pip install -e .

ci-run:
	. .venv/bin/activate && python3 main.py

ci-commit:
	# Note: the following account information will not work on GHES
	git config user.name "github-actions[bot]"
	git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
	git add rss.xml
	git commit -m "Update RSS feed."
	git push

code-format:
	ruff check --fix .

rss-validate:
	open https://validator.w3.org/feed/check.cgi?url=https://program247365.github.io/paulgraham-rss/rss.xml?timestamp=$(shell date +%s)