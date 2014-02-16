.PHONY: requirements static watch
.SILENT: deps

VIRTUALENV_PATH    := $(shell cd env && pwd)
VIRTUALENV_ACTIVATE := $(VIRTUALENV_PATH)/bin/activate
VIRTUALENV_PYTHON   := $(VIRTUALENV_PATH)/bin/python

getdeb    = [ -z "`dpkg -l | grep $(1)`" ] && sudo apt-get install $(1) || :
notify    = @[ -f "$(HOME)/hipchat-message" ] && $(HOME)/hipchat-message $(1) || :

help:
	@echo
	@echo Startup Project
	@echo -----------------------
	@echo
	@echo "install			creates the environment and install the application for production"
	@echo "deps 			Install all system dependencies using apt-get"
	@echo "requirements		Install all python requirements for the project"
	@echo "static			Collect static files and process them for production use"

install: deps env var requirements static
	./env/bin/python manage.py syncdb --migrate
	@echo "project installed Successfully..."


env:
	virtualenv env

var:
	mkdir -p var/cache
	mkdir -p var/log
	mkdir -p var/db
	mkdir -p var/run

requirements:
	./env/bin/pip install -r requirements/project.txt

static:
	$(info - Collect static files and process them for production use)
	mkdir -p public/static
	mkdir -p public/media

	./env/bin/python manage.py collectstatic \
	         -v 0 \
	         --noinput \
	         --traceback \
	         -i django_extensions \
	         -i '*.coffee' \
	         -i '*.rb' \
             -i '*.scss' \
	         -i '*.less' \
	         -i '*.sass'

deps:
	$(info - Installing all system dependencies using apt-get)

	$(call getdeb, postgresql-contrib)
	$(call getdeb, libpq-dev)

