#!/bin/bash
rosrun tf static_transform_publisher 0 0 0 0 0 0 map odom $(( 1000/30)) &
rosrun tf static_transform_publisher 0 0 0 0 0 0 base_footprint base_link $(( 1000/30)) &
