clear
exit
ls
colcon build
source install/setup.bash
clear
ros2 run my_cpp_pubsub simple_publisher 
exit
ls
cd ..
ls
cd ..
ls
exit
exit
source install/setup.bash
ros2 node list
ros2 topic list
ros2 services list
ros2 service list
rqt
ros2 node info /my_turtle
ros2 node info /listener 
ros2 topic echo /turtle1/cmd_vel
exit
ls
source install/setup.bash
colcon build
source install/setup.bash
ros2 run demo_nodes_cpp talker
exit
ls
source install/setup.bash
colcon build
source install/setup.bash
colcon build
source install/setup.bash
colcon build
ros2 run demo_nodes_cpp listener
ros2 run demo_nodes_cpp talker
ros2 node list
