#!/bin/bash

# Create necessary folders with permissions
mkdir -p ./data
chmod -R 777 ./data

# Move to the docker folder and launch Label Studio
cd "$(dirname "$0")"
docker compose up
