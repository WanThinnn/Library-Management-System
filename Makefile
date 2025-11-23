.PHONY: help setup build up down restart logs clean migrate makemigrations createsuperuser shell initdata
.PHONY: prod-build prod-up prod-down prod-restart prod-logs prod-migrate prod-makemigrations prod-initdata prod-shell

help:
	@echo "Library Management System - Docker Commands"
	@echo ""
	@echo "=== DEVELOPMENT (default) ==="
	@echo "  make build          - Build Docker images"
	@echo "  make up             - Start all services"
	@echo "  make down           - Stop all services"
	@echo "  make restart        - Restart all services"
	@echo "  make logs           - View logs"
	@echo "  make makemigrations - Create new migrations"
	@echo "  make migrate        - Run database migrations"
	@echo "  make initdata       - Initialize sample data"
	@echo "  make shell          - Open Django shell"
	@echo ""
	@echo "=== PRODUCTION (add --prod) ==="
	@echo "  make --prod build   - Pull and build production"
	@echo "  make --prod up      - Start production services"
	@echo "  make --prod down    - Stop production services"
	@echo "  make --prod restart - Restart production services"
	@echo "  make --prod logs    - View production logs"
	@echo "  make --prod makemigrations - Create migrations (prod)"
	@echo "  make --prod migrate - Run migrations (prod)"
	@echo "  make --prod initdata - Initialize data (prod)"
	@echo "  make --prod shell   - Open Django shell (prod)"
	@echo ""
	@echo "=== OTHER ==="
	@echo "  make setup          - Initial setup (certificates, .env)"
	@echo "  make createsuperuser - Create Django superuser"
	@echo "  make clean          - Remove containers and volumes"
	@echo "  make rebuild        - Clean rebuild"
	@echo ""

setup:
	@bash scripts/setup.sh

# Check if --prod flag is present
PROD := $(filter --prod,$(MAKECMDGOALS))
ifneq ($(PROD),)
	COMPOSE = docker compose -f docker-compose.prod.yml
	ENV_NAME = production
else
	COMPOSE = docker compose
	ENV_NAME = development
endif

# Remove --prod from goals so it doesn't cause errors
--prod:
	@:

build:
ifneq ($(PROD),)
	$(COMPOSE) pull
	$(COMPOSE) build
else
	$(COMPOSE) build
endif

up:
	$(COMPOSE) up -d
	@echo "[$(ENV_NAME)] Services started. Access at https://library.cyberfortress.local"

down:
	$(COMPOSE) down

restart:
	$(COMPOSE) restart

logs:
	$(COMPOSE) logs -f

makemigrations:
	$(COMPOSE) exec web python manage.py makemigrations

migrate:
	$(COMPOSE) exec web python manage.py migrate

initdata:
	$(COMPOSE) exec web python init_data.py

createsuperuser:
	$(COMPOSE) exec web python manage.py createsuperuser

shell:
	$(COMPOSE) exec web python manage.py shell

collectstatic:
	$(COMPOSE) exec web python manage.py collectstatic --noinput

clean:
	$(COMPOSE) down -v
	docker system prune -f

rebuild:
	$(COMPOSE) down
	$(COMPOSE) build --no-cache
	$(COMPOSE) up -d
