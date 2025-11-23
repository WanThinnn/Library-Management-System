.PHONY: help setup build up down restart logs clean migrate createsuperuser shell

help:
	@echo "Library Management System - Docker Commands"
	@echo ""
	@echo "Available commands:"
	@echo "  make setup          - Initial setup (certificates, .env)"
	@echo "  make build          - Build Docker images"
	@echo "  make up             - Start all services"
	@echo "  make down           - Stop all services"
	@echo "  make restart        - Restart all services"
	@echo "  make logs           - View logs"
	@echo "  make migrate        - Run Django migrations"
	@echo "  make createsuperuser - Create Django superuser"
	@echo "  make shell          - Open Django shell"
	@echo "  make clean          - Remove containers and volumes"
	@echo ""

setup:
	@bash scripts/setup.sh

build:
	docker-compose build

up:
	docker-compose up -d
	@echo "Services started. Access at https://localhost"

down:
	docker-compose down

restart:
	docker-compose restart

logs:
	docker-compose logs -f

migrate:
	docker-compose exec web python manage.py migrate

createsuperuser:
	docker-compose exec web python manage.py createsuperuser

shell:
	docker-compose exec web python manage.py shell

collectstatic:
	docker-compose exec web python manage.py collectstatic --noinput

clean:
	docker-compose down -v
	docker system prune -f

rebuild:
	docker-compose down
	docker-compose build --no-cache
	docker-compose up -d
