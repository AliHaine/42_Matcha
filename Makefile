.PHONY: backend frontend flask database

up:
	$(MAKE) database
	$(MAKE) frontend
	$(MAKE) flask

down:
	docker-compose -f backend_rewrite/tools/database/docker-compose.yml down

backend:
	$(MAKE) database
	$(MAKE) flask

frontend:
	cd angular-frontend && npm install && npx ng serve

flask:
	@bash -c "cd backend_rewrite && pwd && ./tools/launchBackend.sh"

database:
	docker-compose -f backend_rewrite/tools/database/docker-compose.yml up -d
