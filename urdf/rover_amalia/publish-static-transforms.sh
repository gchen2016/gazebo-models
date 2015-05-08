#!/bin/bash
kill -9 $(ps aux | grep broadcaster | awk '{ print $2 }' | tr '\n' ' ')
kill -9 $(ps aux | grep static_transform_publisher | awk '{ print $2 }' | tr '\n' ' ')
rosrun tf static_transform_publisher 0 0 0 0 0 0 map odom $(( 1000/30)) &
rosrun tf static_transform_publisher 0 0 0 0 0 0 base_footprint base_link $(( 1000/30)) &
python2 imu_tf_broadcaster.py base_link rover_amalia_chassis /imu_data &
python2 odom_tf_broadcaster.py odom base_footprint /rover_amalia/odom &
