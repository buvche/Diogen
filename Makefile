.PHONY: help install dev db-up db-down run test tests migrate lint clean

help:
	@echo "Diogen - DevOps Metrics Tracker"
	@echo ""
	@echo "Usage:"
	@echo "  make install    Install dependencies"
	@echo "  make dev        Run development server"
	@echo "  make db-up      Start PostgreSQL container"
	@echo "  make db-down    Stop PostgreSQL container"
	@echo "  make test       Run tests"
	@echo "  make migrate    Run database migrations"
	@echo "  make lint       Run linters"
	@echo "  make clean      Clean cache files"

install:
	pip install -r requirements.txt

dev:
	uvicorn api.main:app --reload

db-up:
	docker compose up -d

db-down:
	docker compose down

test:
	python -m pytest -v

tests: test

migrate:
	alembic upgrade head

lint:
	ruff check .
	mypy .

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .mypy_cache .ruff_cache
