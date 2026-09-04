.PHONY: up down build test backend-dev frontend-dev

up:
	docker-compose up -d

down:
	docker-compose down

build:
	docker-compose build

backend-dev:
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

frontend-dev:
	cd frontend && npm run dev

test:
	cd backend && pytest
	cd frontend && npm run test

migrate:
	cd backend && alembic upgrade head
