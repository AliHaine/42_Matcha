
all:
	@echo "Please specify a target. Available targets:"
	@echo "$(TAB)dev commands: dev, dev-down, dev-logs, dev-rmv"
	@echo "$(TAB)prod commands: prod, prod-down, prod-logs, prod-rmv"
	@echo "$(TAB)other commands: down, frontend, flask, flask-bash, switch-prod, switch-dev"
	@echo "To run the frontend and backend in development mode, use: make dev"
	@echo "To run the production environment, use: make prod"


frontend:
	cd angular-frontend && npm install && npx ng serve

flask-bash:
	@bash -c "cd backend_rewrite && pwd && ./tools/launchBackend.sh"

flask:
	pip install -r backend_rewrite/requirements.txt
	python3 backend_rewrite/run.py

HOSTNAME=$(shell hostname -I | cut -d' ' -f1)
TAB=$(shell printf '\t')
PROD_KEY=$(shell python3 ./backend_rewrite/tools/generateSecretKey.py)

UNAME_S := $(shell uname -s)
FLASK_EXEC = flask
ifeq ($(UNAME_S),Linux)
	FLASK_EXEC = flask-bash
else ifeq ($(UNAME_S),Darwin)
	FLASK_EXEC = flask-bash
else ifeq ($(OS),Windows_NT)
	FLASK_EXEC = flask
endif

switch-prod:
	@echo "Switching to production mode..."
	@sed -i "/server_name/c\$(TAB)server_name $(HOSTNAME)" ./nginx/default.conf
	@sed -i "/HOSTNAME=/c\HOSTNAME=0.0.0.0" ./settings/.flask.env
	@sed -i "/NGINX_HOST=/c\NGINX_HOST=$(HOSTNAME)" ./settings/.flask.env
	@sed -i "/SECRET_KEY=dev/c\SECRET_KEY=$(PROD_KEY)" ./settings/.flask.env
	@sed -i "/DEBUG=/c\DEBUG=False" ./settings/.flask.env
	@sed -i "/export const backendIP =/c\export const backendIP = window.location.hostname + ':' + window.location.port;" ./angular-frontend/src/app/app.config.ts
	@sed -i "/POSTGRES_HOST=/c\POSTGRES_HOST=postgres" ./settings/.database.env

switch-dev:
	@echo "Switching to development mode..."
	@sed -i "/server_name/c\$(TAB)server_name localhost" ./nginx/default.conf
	@sed -i "/HOSTNAME=/c\HOSTNAME=localhost" ./settings/.flask.env
	@sed -i "/NGINX_HOST=/c\NGINX_HOST=localhost" ./settings/.flask.env
	@sed -i "/SECRET_KEY=/c\SECRET_KEY=dev" ./settings/.flask.env
	@sed -i "/DEBUG=/c\DEBUG=True" ./settings/.flask.env
	@sed -i "/export const backendIP =/c\export const backendIP = window.location.hostname + ':5000';" ./angular-frontend/src/app/app.config.ts
	@sed -i "/POSTGRES_HOST=/c\POSTGRES_HOST=localhost" ./settings/.database.env

prod: dev-rmv switch-prod
	@echo "Building and running production containers..."
	@docker compose --env-file ./settings/.database.env -f ./docker-compose.yml up -d

prod-down:
	@docker compose -f ./docker-compose.yml down

prod-logs:
	@docker compose -f ./docker-compose.yml logs -f

prod-rmv:
	@docker compose -f ./docker-compose.yml down --volumes


dev: prod-rmv switch-dev
	@docker compose -f ./backend_rewrite/tools/database/docker-compose.yml --env-file ./settings/.database.env up -d
	@npx concurrently --names "FRONTEND, BACKEND" "make frontend" "make $(FLASK_EXEC)"

dev-down:
	@docker compose -f ./backend_rewrite/tools/database/docker-compose.yml --env-file ./settings/.database.env down

dev-logs:
	@docker compose -f ./backend_rewrite/tools/database/docker-compose.yml --env-file ./settings/.database.env logs -f

dev-rmv:
	@docker compose -f ./backend_rewrite/tools/database/docker-compose.yml --env-file ./settings/.database.env down --volumes

down: dev-down prod-down