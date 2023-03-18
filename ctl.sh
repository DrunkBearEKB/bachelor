#!/bin/bash

# sudo ./ctl.sh start scheduler
# sudo ./ctl.sh stop scheduler

# sudo ./ctl.sh start worker
# sudo ./ctl.sh stop worker

# sudo ./ctl.sh start bukin
# sudo ./ctl.sh stop bukin

apps=("scheduler" "worker" "bukin")

install_libs() {
  sudo ./install_libs.sh
}

function check_is_help() {
  local possible_app="$1"
  if [[ "$possible_app" == "help" ]];
  then
    echo "True"
    return
  fi
  echo "False"
  return
}

function check_is_app_correct() {
  local app="$1"
  if [[ " ${apps[*]} " =~ " ${app} " ]];
  then
    echo "True"
    return
  fi
  echo "False"
  return
}

function echo_start_help() {
  echo "Usage: ./ctl.sh start <option>" >&2
  echo >&2
  echo "Installing all required libs and start app" >&2
  echo >&2
  echo "Possible options:" >&2
  echo "  <app>  app which is gonna be started" >&2
  echo "         - Example: sudo ./ctl.sh start worker" >&2
  echo "  help   command for showing this message" >&2
  echo "         - Example: sudo ./ctl.sh start help" >&2
}

function start_app() {
  local app=$1

  if [ ! -f ./src/"$app"/"$app".py ];
  then
      echo "Executable file not found!" >&2
      return
  fi
  if [ -f PID-"$app" ];
  then
      echo "'$app' is already started!" >&2
      return
  fi

  echo "Starting $app" >&2
  sudo python3 ./src/"$app"/"$app".py &
  local pid=$!
  echo $pid > PID-"$app"
  echo "Started: $app" >&2
}

function echo_stop_help() {
  echo "Usage: ./ctl.sh stop <option>" >&2
  echo >&2
  echo "Stop app" >&2
  echo >&2
  echo "Possible options:" >&2
  echo "  <app>  app which is gonna be started" >&2
  echo "         - Example: sudo ./ctl.sh stop worker" >&2
  echo "  help   command for showing this message" >&2
  echo "         - Example: sudo ./ctl.sh stop help" >&2
}

function stop_app() {
  local app=$1

  if [ ! -f PID-"$app" ];
  then
      echo "'$app' is not started!" >&2
      return
  fi

  echo "Stopping $app" >&2
  local pid=$(cat PID-"$app")
  sudo kill "$pid"
  sudo rm "PID-$app"
  echo "Stopped: $app" >&2
}

function echo_help() {
  echo "Usage: ./ctl.sh <command> <options>" >&2
  echo >&2
  echo "Possible commands:" >&2
  echo "  install_libs  installing all required libs" >&2
  echo "                - Example: sudo ./ctl.sh install_libs" >&2
  echo "  start <app>   installing all required libs and start app" >&2
  echo "                - Example: sudo ./ctl.sh start worker" >&2
  echo "  stop <app>    stop app" >&2
  echo "                - Example: sudo ./ctl.sh stop worker" >&2
  echo "  help          show this help message and exit" >&2
  echo "                - Example: sudo ./ctl.sh help" >&2
}

function echo_undefined() {
  echo "Undefined command $1!" >&2
  echo "Run './ctl.sh' help to see help" >&2
}

case $1 in
install_libs)
  install_libs
  ;;
start)
  res_check_is_help=$(check_is_help "$2")
  if [[ "$res_check_is_help" == "True" ]];
  then
    echo_start_help
  else
    res_check_is_app_correct=$(check_is_app_correct "$2")
    if [[ "$res_check_is_app_correct" == "False" ]];
    then
      echo "App '$2' not found!"
      echo
      exit 1
    fi
    install_libs
    start_app "$2"
  fi
  ;;
stop)
  res_check_is_help=$(check_is_help "$2")
  if [[ "$res_check_is_help" == "True" ]];
  then
    echo_stop_help
  else
    res_check_is_app_correct=$(check_is_app_correct "$2")
    if [[ "$res_check_is_app_correct" == "False" ]];
    then
      echo "App '$2' not found!"
      echo
      exit 1
    fi
    stop_app "$2"
  fi
  ;;
help)
  echo_help
  ;;
*)
  echo_undefined "$1"
  ;;
esac

echo
exit 0