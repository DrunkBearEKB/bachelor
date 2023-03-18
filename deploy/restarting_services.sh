#!/bin/bash

HOST=$1

echo "Restarting services: started"
ssh "$HOST" "sudo cp ./bachelor/services/* /etc/systemd/system/"
ssh "$HOST" "sudo systemctl daemon-reload"
ssh "$HOST" "sudo systemctl restart bachelor.service"
echo "Restarting services: finished"
echo
