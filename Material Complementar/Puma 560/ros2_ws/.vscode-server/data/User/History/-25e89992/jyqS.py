import os
from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable
from launch.substitutions import Command, LaunchConfiguration

from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
  
  puma560_descritpion_dir = get_package_share_directory("puma560_description")

  model_arg = DeclareLaunchArgument(
    name="model", 
    default_value=os.path.join(puma560_descritpion_dir,"urdf","puma560_description.urdf.xacro"),
    description = "Caminho absoluto para o arquivo URDF do robo"
  )

  gazebo_resource_path = SetEnvironmentVariable(
    name="GZ_SIM_RESOURCE_PATH",
    value=[puma560_descritpion_dir]
  )

   robot_description = ParameterValue(
    Command(['xacro ', LaunchConfiguration('model')]), 
    value_type=str
  )

  robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[{"robot_description": robot_description,
                    "use_sim_time": True}]
  )

   # Retorna a configuração do lançamento, incluindo os nós e argumentos.
  return LaunchDescription([
      model_arg,
      robot_state_publisher_node, 
      joint_state_publisher_gui,
      rviz_node
  ])
