import os
from pathlib import Path
from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration

from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

def generate_launch_description():

  robot_description = ParameterValue(
    Command(
    [
        "xacro ", 
        os.path.join(get_package_share_directory("puma560_description"),"urdf","puma560_description.urdf.xacro")
    ]
    ), value_type=str
  )


  robot_state_publisher = Node(
    package="robot_state_publisher",
    executable="robot_state_publisher",
    parameters=[{"robot_description": robot_description}]
  )

  joint_state_broadcaster_spawner = Node(
    package = "controller_manager",
    executable = "spawner",
    arguments = [
        "joint_state_broadcaster",
        "--controller-manager",
        "/controller_manager"
    ]
  )

  arm_controller_spawner = Node(
    package = "controller_manager",
    executable = "spawner",
    arguments = [
        "arm_controller",
        "--controller-manager",
        "/controller_manager"
    ]
  )

  gripper_controller_spawner = Node(
    package = "controller_manager",
    executable = "spawner",
    arguments = [
        "gripper_controller",
        "--controller-manager",
        "/controller_manager"
    ]
  )

# Retorna a configuração do lançamento, incluindo os nós e argumentos.
  return LaunchDescription([
    robot_state_publisher,
    joint_state_broadcaster_spawner,
    arm_controller_spawner,
    gripper_controller_spawner      
  ])