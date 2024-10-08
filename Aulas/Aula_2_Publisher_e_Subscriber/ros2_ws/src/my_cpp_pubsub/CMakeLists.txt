cmake_minimum_required(VERSION 3.8)
project(my_cpp_pubsub)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)

# Adiciona o executável para o Publisher
add_executable(publisher_cpp src/publisher_cpp.cpp)
ament_target_dependencies(publisher_cpp rclcpp std_msgs)

# Adiciona o executável para o Subscriber
add_executable(subscriber_cpp src/subscriber_cpp.cpp)
ament_target_dependencies(subscriber_cpp rclcpp std_msgs)

# Instala os binários
install(TARGETS
  publisher_cpp
  subscriber_cpp
  DESTINATION lib/${PROJECT_NAME})

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
