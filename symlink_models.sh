#!/bin/bash

SCRIPT_DIR="$( cd -P "$( dirname "$0" )" && pwd )" 
GAZEBO_MODELS_DIR=~/.gazebo/models/

add_symlink () {
  model_dir="$SCRIPT_DIR/$1"
  echo "Adding $model_dir"
  ln -s $model_dir $GAZEBO_MODELS_DIR
}

# Add symbolic links to the models inside ~/.gazebo

models=( rover_amalia )

for model in ${models[@]}; do
  add_symlink $model
done
