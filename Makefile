.PHONY: backend frontend flask database

up:
	$(MAKE) database
	$(MAKE) frontend
	$(MAKE) flask

down:
	docker-compose -f backend_rewrite/tools/database/docker-compose.yml down
#	 docker-compose -f backend/database/docker/docker-compose.yml down

backend:
	$(MAKE) database
	$(MAKE) flask

frontend:
	cd angular-frontend && npx ng serve

flask:
	@bash -c "cd backend_rewrite && pwd && ./tools/launchBackend.sh"
#	pip install -r backend/requirements.txt
#	python3 backend/app.py

database:
	docker-compose -f backend_rewrite/tools/database/docker-compose.yml up -d
#	docker-compose -f backend/database/docker/docker-compose.yml up -d
