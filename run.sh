#!/bin/sh

python3 generate_docker_compose.py
docker-compose up -d
