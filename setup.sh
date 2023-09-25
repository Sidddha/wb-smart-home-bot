#!/bin/bash

# Exit the script if any command fails
set -e

# Define variables for the script
SERVICE_NAME="wb-bot"
WORKING_DIR="/mnt/data/wb-smart-home-bot"
APP_DIR="$WORKING_DIR"
VENV_NAME="venv"
VENV_DIR="$WORKING_DIR/$VENV_NAME"
COMPOSE_FILE="$WORKING_DIR/docker-compose.yml"

#mv $WORKING_DIR/dotenv_template $WORKING_DIR/.env

# Check if $USER is empty
if [ -z "$USER" ]; then
  # If $USER is empty, use whoami to get the actual user
  CURRENT_USER=$(whoami)
else
  # If $USER is not empty, use it as the user
  CURRENT_USER=$USER
fi

# Run docker-compose
cd $WORKING_DIR
docker compose -f $COMPOSE_FILE up -d

# Exit with success status code
exit 0