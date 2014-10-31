# Team Diana Gazebo Models

This repository contains the .sdf models for [gazebo]() used by Team Diana

The models are defined using sdf 1.5 and tested under Gazebo 4.0

In order to make changes more easily the contents of this repository are split in two directories:

- **definitions**
  contains the xacro files of the models
- **models**
  contains the built sdf models that can be used under **gazebo**. 

The **build.py** script run xacro on the files in **definitions** and writes the updated models in **models**
