PYTHON ?= python3

.PHONY: setup backend-install frontend-install lint test run seed

setup: backend-install frontend-install

backend-install:
	cd backend && $(PYTHON) -m pip install -e .[dev]

frontend-install:
	cd frontend && npm install

lint:
	cd backend && ruff check app tests
	cd backend && mypy app
	cd frontend && npm run lint

test:
	cd backend && pytest
	cd frontend && npm run test:e2e

run:
	docker compose up --build

seed:
	cd backend && $(PYTHON) -m app.db.seed

