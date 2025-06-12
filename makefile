.DEFAULT_GOAL := all
sources = src tests

.PHONY: install
install:
	poetry install
	pre-commit install

.PHONY: run
run:
	poetry run python src/server.py

.PHONY: format
format:
	poetry run ruff check --fix $(sources)
	poetry run ruff format $(sources)

.PHONY: lint
lint:
	poetry run ruff check $(sources)
	poetry run ruff format --check $(sources)

.PHONY: run_docker
run_docker:
	docker compose up -d

.PHONY: test
test:
	poetry run pytest

.PHONY: test_docker
test_docker:
	docker compose exec flask poetry run pytest

.PHONY: output_coverage
output_coverage:
	@rm -rf htmlcov
	@mkdir -p htmlcov
	poetry run coverage run -m pytest
	poetry run coverage report
	poetry run coverage html -d htmlcov

.PHONY: output_coverage_docker
output_coverage_docker:
	@docker compose exec flask rm -rf htmlcov
	@docker compose exec flask mkdir -p htmlcov
	docker compose exec flask poetry run coverage run -m pytest
	docker compose exec flask poetry run coverage report
	docker compose exec flask poetry run coverage html -d htmlcov

.PHONY: send_email
send_email:
	poetry run python src/send_email.py

.PHONY: send_email_docker
send_email_docker:
	docker compose exec flask poetry run python src/send_email.py

.PHONY: clean
clean:
	rm -rf htmlcov
	rm -rf .pytest_cache
	rm -f .coverage
	rm -f .coverage.*

.PHONY: all
all: format lint test
