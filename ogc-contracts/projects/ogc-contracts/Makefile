.PHONY: help install build deploy test demo clean

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	poetry install --no-interaction

build: ## Build smart contracts
	poetry run python working_vault.py
	@echo "✅ Contracts built in artifacts/"

deploy: ## Deploy to LocalNet
	poetry run python deploy_working.py

test: ## Run test suite
	poetry run python test_vault.py

demo: ## Run OGC demo
	poetry run python ogc_demo.py

clean: ## Clean artifacts
	rm -rf artifacts/
	rm -rf __pycache__/
	rm -rf .pytest_cache/

localnet-start: ## Start LocalNet
	algokit localnet start

localnet-stop: ## Stop LocalNet
	algokit localnet stop

ci: install build test demo ## Run full CI pipeline