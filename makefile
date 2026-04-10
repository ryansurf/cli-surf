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

.PHONY: lambda-zip
lambda-zip:
	poetry export -f requirements.txt --output requirements.txt --without-hashes
	pip install -r requirements.txt -t ./package
	cp -r src/ ./package/src/
	cd package && zip -r ../terraform/lambda.zip . && cd ..

ECR_REGION ?= us-west-1
ECR_ACCOUNT_ID ?= $(shell aws sts get-caller-identity --query Account --output text)
ECR_REPO = $(ECR_ACCOUNT_ID).dkr.ecr.$(ECR_REGION).amazonaws.com/cli-surf

.PHONY: ecr-login
ecr-login:
	aws ecr get-login-password --region $(ECR_REGION) | docker login --username AWS --password-stdin $(ECR_ACCOUNT_ID).dkr.ecr.$(ECR_REGION).amazonaws.com

.PHONY: docker-build
docker-build:
	docker build --platform linux/amd64 --provenance=false -f Dockerfile.lambda -t cli-surf:latest .

.PHONY: docker-push
docker-push: ecr-login docker-build
	docker tag cli-surf:latest $(ECR_REPO):latest
	docker push $(ECR_REPO):latest

.PHONY: update-lambda
update-lambda:
	$(eval DIGEST := $(shell aws ecr describe-images --repository-name cli-surf --region $(ECR_REGION) --query 'sort_by(imageDetails, &imagePushedAt)[-1].imageDigest' --output text))
	aws lambda update-function-code --function-name cli-surf --region $(ECR_REGION) --image-uri $(ECR_REPO)@$(DIGEST)

.PHONY: deploy
deploy: docker-push update-lambda
	terraform -chdir=terraform apply


