#!/usr/bin/env bash
source activate venv
celery -A your_application.celery worker
