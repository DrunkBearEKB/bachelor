#!/bin/bash

list_installing_libs=("bachelor_core" "scheduler" "candace")
libs_installing_success=()
libs_installing_failed=()

for lib in "${list_installing_libs[@]}"
do
  echo "Installing" $lib
  cd ./bachelor/src/$lib
  sudo bash ./setup.sh
  return_code=$?
  if [[ $return_code == 0 ]];
  then
    echo $lib "installed successfully"
    libs_installing_success+=($lib)
  else
    echo $lib "installing failed"
    libs_installing_failed+=($lib)
  fi
  cd ../../..
done
echo

if [[ ${#libs_installing_success[@]} != 0 ]];
then
  echo "Installed libs:"
  for lib in "${libs_installing_success[@]}"
  do
    echo " " $lib
  done
fi
echo

if [[ ${#libs_installing_failed[@]} != 0 ]];
then
  echo "Failed installing libs:"
  for lib in "${libs_installing_failed[@]}"
  do
    echo " " $lib
  done
fi
echo

exit ${#libs_installing_failed[@]}