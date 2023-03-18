#!/bin/bash

HOST=$1

echo "Installing requirements: started"
ssh "$HOST" "sudo apt-get update; sudo apt-get install -y systemd"
ssh "$HOST" "curl -sSL https://storage.yandexcloud.net/yandexcloud-yc/install.sh | bash; source /home/grig-ivanenko/.bashrc"
ssh "$HOST" "sudo apt install python3-pip"
ssh "$HOST" "sudo python3 -m pip install –upgrade pip"
ssh "$HOST" "sudo pip3 install -r ./bachelor/requirements.txt"
ssh "$HOST" "sudo ./bachelor/install_libs.sh"
echo "Installing requirements: finished"
echo