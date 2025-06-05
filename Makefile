SHELL := /bin/bash

env-setup:
	rm -rf venv
	python3 -m venv venv; \
	source venv/bin/activate; \
	pip install -r requirements.txt


run-local:
	source venv/bin/activate; \
	python3 manage.py makemigrations; \
	python3 manage.py migrate; \
	black .; \
	python3 manage.py runserver 8000