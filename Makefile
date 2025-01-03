.DEFAULT_GOAL := help

.PHONY: help
help:  ## Show this help.
	@grep -E '^\S+:.*?## .*$$' $(firstword $(MAKEFILE_LIST)) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "%-30s %s\n", $$1, $$2}'

.PHONY: build
build: ## Build the docker image
	docker compose build

.PHONY: add-package
add-package:
	@read -p "Dependency to install: " PACKAGE_NAME; \
	docker compose run --rm --no-deps lift poetry add $$PACKAGE_NAME
	make build

.PHONY: test
test: ## Run tests
	docker compose run --rm lift poetry run pytest test -ra

.PHONY: coverage
coverage:
	docker compose run --rm lift poetry run coverage run --branch -m pytest test
	docker compose run --rm lift poetry run coverage html
	@echo "You can open the report at ${PWD}/htmlcov/index.html"

.PHONY: format
format:
	docker compose run --rm --no-deps lift poetry run ruff format src test

.PHONY: check-format
check-format:
	docker compose run --rm --no-deps lift poetry run ruff format --check src test

.PHONY: check-lint
check-lint:
	docker compose run --rm --no-deps lift poetry run ruff check src test

.PHONY: lint
lint:
	docker compose run --rm --no-deps lift poetry run ruff check --fix src test

.PHONY: check-typing
check-typing:
	 docker compose run --rm --no-deps lift poetry run mypy .

.PHONY: local-setup
local-setup:
	scripts/local-setup.sh
	make install

.PHONY: install
install:
	docker compose run --rm --no-deps lift poetry install

.PHONY: pre-commit
pre-commit: check-typing check-format check-lint test

.PHONY: watch
watch:
	docker compose run --rm lift poetry run ptw