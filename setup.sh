#!/bin/bash

# Define variables for the script
SERVICE_NAME="wb-bot"
USER_NAME="root"
WORKING_DIR="/opt/tgbot"
APP_DIR="$WORKING_DIR"
VENV_NAME="venv"
VENV_DIR="$WORKING_DIR/$VENV_NAME"
COMPOSE_FILE="$WORKING_DIR/docker-compose.yml"

mv $WORKING_DIR/.env.template $WORKING_DIR/.env


# Install Docker (if not already installed)
if ! command -v docker &> /dev/null
then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    rm get-docker.sh
fi

# Install dependencies in a virtual environment
python3 -m venv $VENV_DIR
source $VENV_DIR/bin/activate
pip install -r $APP_DIR/requirements.txt

# Create a systemd service file
cat <<EOF > /etc/systemd/system/$SERVICE_NAME.service
[Unit]
Description=WB Bot
After=network.target

[Service]
User=$USER_NAME
Group=$USER_NAME
Type=simple
WorkingDirectory=$WORKING_DIR
Environment="PATH=$VENV_DIR/bin"
ExecStart=$VENV_DIR/bin/python $APP_DIR/app.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd daemon to pick up new service file
systemctl daemon-reload

# Enable and start the service
systemctl enable $SERVICE_NAME.service
systemctl start $SERVICE_NAME.service

# Run docker-compose
cd $WORKING_DIR
docker-compose -f $COMPOSE_FILE up -d