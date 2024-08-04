#!/bin/bash

set -e
source /opt/ros/humble/setup.bash

# Ensure the ROS workspace directory exists
if [ ! -d "/home/ros2_ws/ros2_ws" ]; then
    mkdir -p /home/ros2_ws/ros2_ws
fi

# Change ownership to the correct user
chown -R ros2_ws:ros2_ws /home/ros2_ws/ros2_ws

exec "$@"
