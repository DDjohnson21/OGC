.PHONY: help install build deploy test demo clean

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	poetry install --no-interaction

build: ## Build smart contracts
	@echo "🔨 Building contracts..."
	@for contract in *vault*.py *contract*.py; do \
		if [ -f "$$contract" ]; then \
			echo "Building $$contract..."; \
			poetry run python "$$contract"; \
		fi; \
	done
	@echo "✅ Contracts built in artifacts/"

deploy: ## Deploy to LocalNet
	@for deploy in deploy_*.py *_deploy.py; do \
		if [ -f "$$deploy" ]; then \
			echo "Running $$deploy..."; \
			poetry run python "$$deploy"; \
			break; \
		fi; \
	done

test: ## Run test suite
	@for test in test_*.py *_test.py; do \
		if [ -f "$$test" ]; then \
			echo "Running $$test..."; \
			poetry run python "$$test"; \
		fi; \
	done

demo: ## Run demos
	@for demo in *demo*.py demo_*.py; do \
		if [ -f "$$demo" ]; then \
			echo "Running $$demo..."; \
			poetry run python "$$demo"; \
		fi; \
	done

clean: ## Clean artifacts
	rm -rf artifacts/
	rm -rf __pycache__/
	rm -rf .pytest_cache/

localnet-start: ## Start LocalNet
	algokit localnet start

localnet-stop: ## Stop LocalNet
	algokit localnet stop

ci: install build test demo ## Run full CI pipeline