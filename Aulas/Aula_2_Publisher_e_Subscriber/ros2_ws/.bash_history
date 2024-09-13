source install/setup.bash 
ros2 run my_cpp_pubsub simple_subscriber
ls
source install/setup.bash 
ros2 run my_cpp_pubsub simple_subscriber
source install/setup.bash 
ros2 run my_cpp_pubsub simple_subscriber
exit
ls
source install/setup.bash 
ros2 run my_cpp_pubsub simple_subscriber 
exit
ls
ls
colcon build
source install/setup.bash
cd src/
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_cmake publisher --dependencies rclcpp std_msgs
ls
clear
ros2 pkg create --build-type ament_cmake my_cpp_pubsub --dependencies rclcpp std_msgs
colcon build
source install/setup.bash 
ros2 run my_cpp_pubsub simple_publisher
clear
colcon build
ros2 run my_cpp_pubsub simple_publisher
cd .. 
colcon build
source install/setup.bash
ls
ros2 pkg list | grep my_cpp_pubsub
ros2 run my_cpp_pubsub simple_publisher
exit
