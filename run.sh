#!/bin/bash

SERVICE_NAME="app"

docker compose exec "$SERVICE_NAME" bash -c "pipenv run python -m src.main"