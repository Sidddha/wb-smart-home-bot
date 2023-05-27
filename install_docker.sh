#!/bin/bash

# Exit the script if any command fails
set -e

# Check if the script is being run as root
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root"
   exit 1
fi

apt-get update
apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

if ! command -v docker &> /dev/null
then
    # Run wb-release command and capture output
    wb_release=$(wb-release)
    # Extract the version number from the output
    if [[ $wb_release =~ wb-([0-9]{4,}) ]]; then
        version="${BASH_REMATCH[1]}"
        echo "version: $version"
    else
        echo "ERROR: Failed to extract version number from wb-release output"
        exit 1
    fi

    if [[ $version -eq "2304" || $version -gt "2304" ]]; then
        echo "wb release is newer then wb-2304. Performing additional actions..."
        apt install -y iptables
        update-alternatives --set iptables /usr/sbin/iptables-legacy
        update-alternatives --set ip6tables /usr/sbin/ip6tables-legacy
    else 
        echo "wb release is older then wb-2304. This script will not work correctly on it. Update release to wb-2304 or newer."
        exit 1
    fi 
    # Set up repository
    install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    chmod a+r /etc/apt/keyrings/docker.gpg
    echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

    # Set the installation directory
    INSTALL_DIR=/mnt/data/additional_packages
    mkdir -p $INSTALL_DIR/var/lib/dpkg
    cd $INSTALL_DIR
    release=$(lsb-release)
    # Download Docker and its dependencys
    apt-get update
    sudo apt-get download docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

    # Install the downloaded packages to the installation directory

    dpkg --instdir=$INSTALL_DIR --admindir=$INSTALL_DIR/var/lib/dpkg -i $INSTALL_DIR/*.deb


    # Create symbolic links to the standard directories
    ln -s $INSTALL_DIR/usr/share/man/man1/docker.1.gz /usr/share/man/man1/docker.1.gz
    ln -s $INSTALL_DIR/usr/bin/docker /usr/bin/docker
    ln -s $INSTALL_DIR/usr/bin/containerd /usr/bin/containerd
    ln -s $INSTALL_DIR/usr/libexec/docker/cli-plugins/docker-compose /usr/libexec/docker/cli-plugins
else
    echo "Docker already installed."
fi

exit 0






