.PHONY: backend frontend flask database

both: database
	@bash -c "cd backend_rewrite && pwd && ./tools/resetDatabase.sh"
	@npx concurrently "make frontend" "make flask-bash"

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

flask-bash:
	@bash -c "cd backend_rewrite && pwd && ./tools/launchBackend.sh"

flask:
	pip install -r backend_rewrite/requirements.txt
	python3 -m flask --app backend_rewrite/flask_backend init-db
	python3 backend_rewrite/run.py

database:
	docker-compose -f backend_rewrite/tools/database/docker-compose.yml --env-file ./settings/.database.env up -d
