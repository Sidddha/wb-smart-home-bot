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
    gnupg \
    lsb-release
    
    
# Install Docker (if not already installed)


if ! command -v docker &> /dev/null
then
    # Run wb-release command and capture output
    output=$(wb-release)

    # Extract the version number from the output
    version=$(echo "$output" | cut -d ' ' -f 2)

    # Compare the version number to the minimum required version
    if [[ $version == "wb-2304" || $version > "wb-2304" ]]; then
      echo "wb release is newer then wb-2304. Performing additional actions..."
      apt install -y iptables
      update-alternatives --set iptables /usr/sbin/iptables-legacy
      update-alternatives --set ip6tables /usr/sbin/ip6tables-legacy
    fi

    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
    curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    mkdir /mnt/data/etc/docker && ln -s /mnt/data/etc/docker /etc/docker
    mkdir /mnt/data/.docker
    sudo cat << EOF > /etc/docker/daemon.json
{
  "data-root": "/mnt/data/.docker"
}
EOF

    apt update && apt install docker-ce docker-ce-cli containerd.io docker-compose

fi

# Install Docker Compose (if not already installed)
if ! command -v docker-compose &> /dev/null
then
    sudo curl -L "https://github.com/docker/compose/releases/v2.17.2/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi

# Run docker-compose
cd $WORKING_DIR
docker-compose -f $COMPOSE_FILE up -d