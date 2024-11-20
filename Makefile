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
