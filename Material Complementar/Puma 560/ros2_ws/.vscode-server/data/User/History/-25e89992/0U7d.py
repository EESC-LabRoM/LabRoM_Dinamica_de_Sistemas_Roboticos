import os
from pathlib import Path
from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable, IncludeLaunchDescription
from launch.generate_launch_description_source import PythonLaunchDescriptionSource
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
    value=[
      str(Path(puma560_descritpion_dir).parent.resolve())]
  )

  ros_distro = os.environ["ROS_DISTRO"]
  phsics_engine = "" if ros_distro== "humble" else "--physics-engine gz-physics-bullet-featherstone-plugin"

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

  gazebo = IncludeLaunchDescription(
    PythonLaunchDescriptionSource([
      os.oath.join(
        get_package_share_directory("ros_gz_sim"),
        "launch"
        ),"/gz_sim.launch.py"]
    )
    launch_arguments=[
      ("gz_args", [" -v 4 -r empty.sdf ", phsics_engine])
    ]
  )

  gz_spawn_entity = Node(
    package = "ros_gz_sim",
    executable = "create",
    output = "screen",
    arguments = ["-topic", "robot_description",
                  "-name", "puma560"]
  )

  gz_ros2_bridge = Node(
    package = "ros_gz_bridge", 
    executable = "parameter_bridge", 
    arguments = [
      "/clock@rosgraph_msgs/msg/Clock[gz.msg.Clock]" 
    ]
  )

   # Retorna a configuração do lançamento, incluindo os nós e argumentos.
  return LaunchDescription([
      model_arg,
      robot_state_publisher_node, 
      joint_state_publisher_gui,
      rviz_node
  ])
