# Here you can config commands when the container is inicialized

#!/bin/bash

set -e
source /opt/ros/humble/setup.bash
# source /opt/ros/humble/setup.zsh
# echo "Provided arguments: $@"

chown -R ros2_ws:ros2_ws /home/ROS/ros2_ws
exec $@