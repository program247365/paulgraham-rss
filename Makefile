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
	git diff
	git config --global user.email "rss-bot@example.com"
	git config --global user.name "RSS-bot"
	git diff --quiet rss.xml || (git add rss.xml && git commit -m "Updated RSS feed")
	git push origin main