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


# Check if the current user is root
if [[ "$CURRENT_USER" == "root" ]]; then
  # Output a warning message
  echo "WARNING: Installing this application as root can be a security vulnerability. Do you want to continue? (yes/no)"

  # Read user input
  read CONTINUE

  # Check if user input is "yes"
  if [[ "$CONTINUE" == "yes" ]]; then
    echo "Continuing the script..."
  else
    echo "Aborting the script."
    exit 1
  fi
fi

# Install Docker (if not already installed)
if ! command -v docker &> /dev/null
then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $CURRENT_USER
    rm get-docker.sh
fi


sudo apt-get -y install python3-venv
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