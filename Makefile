# Constants
SRC=snippets_test
ENVIRONMENT_FOLDER=.
API_NAME = ${SRC}-server

# Commands
compose_cmd = docker-compose -f docker-compose.yml --env-file=${ENVIRONMENT_FOLDER}/.env
down_cmd = $(compose_cmd) down --remove-orphans
exec_cmd = docker exec -it $(API_NAME)
attach_cmd = docker attach $(API_NAME)

.PHONY: down down_all exec pdb logs start test shell up build celery

down:
	@echo "Removing containers and orphans..."
	@$(down_cmd)

down_all:
	@echo "Removing containers with their volumes and images..."
	@$(down_cmd) --volumes

exec:
	@$(exec_cmd) bash

pdb:
	@$(attach_cmd)

logs:
	@$(compose_cmd) logs --tail=all -f | grep $(API_NAME)

start:
	@$(compose_cmd) start

test:
	docker exec -w /code/$(SRC) $(API_NAME) poetry run pytest --ds=settings.test

shell:
	docker exec -it -w /code/$(SRC) $(API_NAME) poetry run python manage.py shell_plus

up:
	@$(compose_cmd) up -d

build:
	@$(compose_cmd) build --no-cache --build-arg PROJECT_NAME=${SRC}

celery:
	@$(compose_cmd) exec server bash -c "celery -A django_snippets worker -E -l info"
