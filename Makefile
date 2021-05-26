DOCKER_COMPOSE := docker-compose
PROJECT_NAME := test-flask

ifdef NO_CACHE
	BUILD_CACHE_FLAG := --no-cache
endif

ifdef FILE
	FILE_FLAG := --file ${FILE}
endif

up:
	${DOCKER_COMPOSE} up

help:
	@echo "Execute an action within mindata api project"
	@echo
	@echo "USAGE:"
	@echo "  make [COMMAND]"
	@echo
	@echo "COMMANDS:"
	@echo "  cov                      runs coverage tests"
	@echo "  help                     displays this"
	@echo "  images [NO_CACHE]        just build the environment"
	@echo "  migrate                  run migration queries"
	@echo "  sh                       opens bash terminal in ${PROJECT_NAME}"
	@echo "  test [FILE=file_to_test] run tests"
	@echo "  up                       just start the environment"


###########################
####### DEVELOPMENT #######
###########################

migrate:
	${DOCKER_COMPOSE} run --rm ${PROJECT_NAME}-api sh -c 'flask db migrate'

upgrade:
	${DOCKER_COMPOSE} run --rm ${PROJECT_NAME}-api sh -c 'flask db upgrade'

downgrade:
	${DOCKER_COMPOSE} run --rm ${PROJECT_NAME}-api sh -c 'flask db downgrade'

sh:
	@$(DOCKER_COMPOSE) run ${PROJECT_NAME}-api sh

test:
	${DOCKER_COMPOSE} run --rm ${PROJECT_NAME}-api sh -c '`echo flask test ${FILE_FLAG}`'

cov:
	${DOCKER_COMPOSE} run --rm ${PROJECT_NAME}-api sh -c 'flask cov'

flake8:
	${DOCKER_COMPOSE} run --rm ${PROJECT_NAME}-api sh -c 'flake8 --max-line-length 120 project'
