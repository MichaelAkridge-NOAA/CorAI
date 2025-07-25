#!/bin/bash

# Create necessary folders with permissions
mkdir -p ~/labelstudio/data
chmod -R 777 ~/labelstudio/data
mkdir -p ~/docker
chmod -R 777 ~/docker

# Move to the docker folder and launch Label Studio
cd "$(dirname "$0")"
docker compose up
