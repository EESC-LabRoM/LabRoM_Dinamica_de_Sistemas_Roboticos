// publicador_cpp.cpp
#include <chrono>
#include <functional>
#include <memory>
#include <string>
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

using namespace std::chrono_literals;


int main(int argc, char *argv[])
{
  rclcpp::init(argc, argv);

  auto node = rclcpp::Node::make_shared("Publicador_cpp");
  auto publisher = node->create_publisher<std_msgs::msg::String>("topico_exemplo", 10);

	// Define a frequência de publicação (500ms)
  rclcpp::WallRate loop_rate(500ms);

  size_t count = 0;
  
  while (rclcpp::ok()) {
    auto message = std_msgs::msg::String();
    message.data = "Hello, ROS 2: " + std::to_string(count++);
    RCLCPP_INFO(node->get_logger(), "Publishing: '%s'", message.data.c_str());

    // Publica a mensagem
    publisher->publish(message);

    // Aguarda o próximo ciclo de publicação
    loop_rate.sleep();
  }

  rclcpp::shutdown();
  return 0;
}
