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
	# Note: the following account information will not work on GHES
	git config user.name "github-actions[bot]"
	git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
	git add rss.xml
	git commit -m "generated"
	git push