.PHONY: run run_docker test test_docker post_test docker_post_test send_email send_email_docker

run:
	poetry run python src/server.py

run_docker:
	docker compose up -d

test:
	poetry run pytest -s -x --cov=src -vv

test_docker:
	docker compose exec flask poetry run pytest -s -x --cov=src -vv

output_coverage:
	poetry run coverage html

output_coverage_docker:
	docker compose exec flask poetry run coverage html

send_email:
	poetry run python src/send_email.py

send_email_docker:
	docker compose exec flask poetry run python src/send_email.py
