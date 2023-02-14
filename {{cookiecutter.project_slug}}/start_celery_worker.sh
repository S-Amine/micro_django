#!/usr/bin/env bash

celery -A {{cookiecutter.project_slug}}.celery worker --loglevel=info ;
