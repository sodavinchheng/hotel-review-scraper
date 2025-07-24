.PHONY: help build up down restart logs clean dev prod

# Default target
help:
	@echo "Available commands:"
	@echo "  make dev      - Start development environment"
	@echo "  make prod     - Start production environment"
	@echo "  make build    - Build all services"
	@echo "  make up       - Start all services"
	@echo "  make down     - Stop all services"
	@echo "  make restart  - Restart all services"
	@echo "  make logs     - Show logs for all services"
	@echo "  make clean    - Clean up containers, images, and volumes"

# Development environment
dev:
	docker-compose up --build -d
	docker-compose exec backend alembic upgrade head

# Production environment
prod:
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml up --build -d

# Build all services
build:
	docker-compose build

# Start all services
up:
	docker-compose up -d

# Stop all services
down:
	docker-compose down

# Restart all services
restart:
	docker-compose restart

# Show logs
logs:
	docker-compose logs -f

# Clean up everything
clean:
	docker-compose down -v
	docker system prune -f
	docker volume prune -f

# Database commands

db-makemigration:
	@read -p "Enter migration message: " message; \
	docker-compose exec backend alembic revision --autogenerate -m "$$message"

db-migrate:
	docker-compose exec backend alembic upgrade head

db-reset:
	docker-compose exec backend alembic downgrade base
	docker-compose exec backend alembic upgrade head

# Install dependencies
install-frontend:
	cd frontend && npm install

install-backend:
	cd backend && pip install -r requirements.txt

openapi:
	docker-compose exec frontend npm run openapi:docker

# Formatting
format:
	docker-compose exec frontend npx lint-staged --verbose
