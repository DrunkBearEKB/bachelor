#!/bin/bash

HOST=$1
USER=$2

echo "Preparing source files and directories structure: started"
ssh "$HOST" "mkdir bachelor; mkdir bachelor/logs mkdir"
tar -cvf sources.tar.gz ./src ./configs ./services ./ctl.sh ./install_libs.sh ./requirements.txt
scp sources.tar.gz "$HOST":/home/"$USER"/bachelor/sources.tar.gz
ssh "$HOST" "cd bachelor; tar -xvf sources.tar.gz; rm sources.tar.gz"
echo "Preparing source files and directories structure: finished"
echo
