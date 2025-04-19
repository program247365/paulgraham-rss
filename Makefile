.PHONY: ci-setup ci-install ci-run ci-commit

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
	@echo "Current git status:"
	git status
	@echo "\nGit diff output:"
	git diff rss.xml
	git config --global user.email "rss-bot@example.com"
	git config --global user.name "RSS-bot"
	if [ -f rss.xml ]; then \
		echo "rss.xml exists and has the following content:"; \
		cat rss.xml; \
		if [ -n "$$(git diff rss.xml)" ]; then \
			echo "Changes detected in rss.xml"; \
			git add rss.xml; \
			git commit -m "Updated RSS feed"; \
			git push origin main; \
		else \
			echo "No changes detected in rss.xml"; \
		fi; \
	else \
		echo "rss.xml does not exist!"; \
	fi