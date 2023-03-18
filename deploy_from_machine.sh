#!/bin/bash

HOST=$1
USER=$2


# Preparing source files and directories structure
chmod +x ./deploy/preparing.sh
./deploy/preparing.sh "$HOST" "$USER"

# Installing requirements
chmod +x ./deploy/installing_requirements.sh
./deploy/installing_requirements.sh "$HOST"

# Restarting services
chmod +x ./deploy/restarting_services.sh
./deploy/restarting_services.sh "$HOST"
