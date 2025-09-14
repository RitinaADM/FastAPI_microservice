# Makefile for running tests in Docker

# Default target
.PHONY: help
help:
	@echo "Available commands:"
	@echo "  make test              - Run all tests in Docker"
	@echo "  make test-unit         - Run unit tests in Docker"
	@echo "  make test-integration  - Run integration tests in Docker"
	@echo "  make test-coverage     - Run tests with coverage in Docker"
	@echo "  make up               - Start all services"
	@echo "  make down             - Stop all services"

# Run all tests in Docker
.PHONY: test
test:
	docker-compose run --rm test-runner

# Run unit tests in Docker
.PHONY: test-unit
test-unit:
	docker-compose run --rm test-runner python -m pytest tests/unit/ -v

# Run integration tests in Docker
.PHONY: test-integration
test-integration:
	docker-compose run --rm test-runner python -m pytest tests/integration/ -v

# Run tests with coverage in Docker
.PHONY: test-coverage
test-coverage:
	docker-compose run --rm test-runner python -m pytest tests/ --cov=src/ --cov-report=html --cov-report=term

# Start all services
.PHONY: up
up:
	docker-compose up --build

# Stop all services
.PHONY: down
down:
	docker-compose down

# Clean up Docker resources
.PHONY: clean
clean:
	docker-compose down -v --remove-orphans
	docker system prune -f