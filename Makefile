.PHONY: backend frontend flask database

up:
	$(MAKE) database
	$(MAKE) frontend
	$(MAKE) flask

down:
	 docker-compose -f backend/database/docker/docker-compose.yml down

backend:
	$(MAKE) database
	$(MAKE) flask

frontend:
	cd angular-frontend && npx ng serve

flask:
	pip install -r backend/requirements.txt
	python backend/app.py

database:
	docker-compose -f backend/database/docker/docker-compose.yml up -d
