.PHONY: lint format

lint:
	ruff check . && ruff check . --diff

format:
	ruff check . --fix && ruff format .

test:
	pytest -s -x --cov=src -vv

post_test:
	coverage html
