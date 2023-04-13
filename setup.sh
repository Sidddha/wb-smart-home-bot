#!/bin/bash

# Define variables for the script
SERVICE_NAME="wb-bot"
WORKING_DIR="/mnt/data/wb-smart-home-bot"
APP_DIR="$WORKING_DIR"
VENV_NAME="venv"
VENV_DIR="$WORKING_DIR/$VENV_NAME"
COMPOSE_FILE="$WORKING_DIR/docker-compose.yml"

mv $WORKING_DIR/dotenv_template $WORKING_DIR/.env

# Check if $USER is empty
if [ -z "$USER" ]; then
  # If $USER is empty, use whoami to get the actual user
  CURRENT_USER=$(whoami)
else
  # If $USER is not empty, use it as the user
  CURRENT_USER=$USER
fi

sudo apt-get update
sudo apt-get install \
    ca-certificates \
    curl \
    gnupg
    
# Install Docker (if not already installed)


if ! command -v docker &> /dev/null
then
    sudo install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    sudo chmod a+r /etc/apt/keyrings/docker.gpg
    echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt-get update
    sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    sudo usermod -aG docker $CURRENT_USER
fi

# Install Docker Compose (if not already installed)
if ! command -v docker-compose &> /dev/null
then
    sudo curl -L "https://github.com/docker/compose/releases/v2.17.2/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi

# Install pip (if not already installed)
if ! command -v pip &> /dev/null
then
    sudo apt-get -y install python3-pip
fi

sudo apt-get -y install python3-venv
# Install dependencies in a virtual environment
python3 -m venv $VENV_DIR
source $VENV_DIR/bin/activate
pip install -r $APP_DIR/requirements.txt

# Create a systemd service file
sudo cat <<EOF > /etc/systemd/system/$SERVICE_NAME.service
[Unit]
Description=WB Bot
After=network.target

[Service]
User=$CURRENT_USER
Group=$CURRENT_USER
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