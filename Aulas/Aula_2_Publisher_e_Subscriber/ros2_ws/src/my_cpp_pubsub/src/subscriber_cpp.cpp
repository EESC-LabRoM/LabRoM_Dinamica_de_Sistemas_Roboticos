#include <chrono>
#include <functional>
#include <memory>
#include <string>
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

// Função callback que será chamada quando uma nova mensagem chegar
void topic_callback(const std_msgs::msg::String::SharedPtr msg)
{
  RCLCPP_INFO(rclcpp::get_logger("Subscriber_cpp"), "I heard: '%s'", msg->data.c_str());
}

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);

  // Cria um nó ROS
  auto node = rclcpp::Node::make_shared("Subscriber_cpp");

  // Cria o subscriber que escuta no tópico "topic"
  auto subscription = node->create_subscription<std_msgs::msg::String>(
    "topic_exemplo", 10, topic_callback);

  // Mantém o nó em execução
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}
