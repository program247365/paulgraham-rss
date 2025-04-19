.PHONY: ci-setup ci-install ci-run ci-commit

# CI-specific tasks
ci-setup:
	curl -LsSf https://astral.sh/uv/install.sh | sh
	uv venv --python 3.13
	. .venv/bin/activate

ci-install:
	. .venv/bin/activate && uv pip install -e .

ci-run:
	. .venv/bin/activate && \
	if [ "$(DEBUG)" = "true" ]; then \
		echo "Debug mode enabled - Running with verbose output"; \
		python3 -v main.py; \
		echo "Checking if rss.xml exists and its contents:"; \
		ls -la rss.xml 2>/dev/null || echo "rss.xml does not exist"; \
		[ -f rss.xml ] && echo "rss.xml contents:" && cat rss.xml; \
	else \
		python3 main.py; \
	fi

ci-commit:
	@echo "Current git status:"
	git status
	@echo "\nGit diff output:"
	git diff rss.xml
	git config --global user.email "rss-bot@example.com"
	git config --global user.name "RSS-bot"
	if [ "$(DEBUG)" = "true" ]; then \
		echo "Debug mode enabled - Showing detailed git information"; \
		echo "Current branch:"; \
		git branch; \
		echo "\nGit remote -v:"; \
		git remote -v; \
		echo "\nGit status -s:"; \
		git status -s; \
		echo "\nGit diff rss.xml:"; \
		git diff rss.xml; \
	fi
	if [ -n "$$(git diff rss.xml)" ]; then \
		echo "Changes detected in rss.xml"; \
		git add rss.xml; \
		git commit -m "Updated RSS feed"; \
		git push; \
	else \
		echo "No changes detected in rss.xml"; \
	fi 