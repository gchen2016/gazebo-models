#!/bin/bash
echo "removing previous instances"
kill -9 $(ps aux | grep static_rover_broadcaster | awk '{ print $2 }' | tr '\n' ' ')
kill -9 $(ps aux | grep flir_pantilt_broadcaster | awk '{ print $2 }' | tr '\n' ' ')
kill -9 $(ps aux | grep flir_pantilt_broadcaster | awk '{ print $2 }' | tr '\n' ' ')
echo "start publishers"
python2 /home/clynamen/teamdiana/gazebo-assets/models/urdf/rover_amalia/static_rover_broadcaster.py &
python2 /home/clynamen/teamdiana/gazebo-assets/models/urdf/rover_amalia/flir_pantilt_broadcaster-pan.py &
python2 /home/clynamen/teamdiana/gazebo-assets/models/urdf/rover_amalia/flir_pantilt_broadcaster-tilt.py &
