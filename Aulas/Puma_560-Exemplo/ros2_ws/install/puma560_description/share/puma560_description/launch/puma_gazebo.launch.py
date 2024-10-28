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
  
    puma560_description_dir = get_package_share_directory("puma560_description")

    model_arg = DeclareLaunchArgument(
        name="model", 
        default_value=os.path.join(puma560_description_dir,"urdf","puma560_description.urdf.xacro"),
        description="Caminho absoluto para o arquivo URDF do robô"
    )

    gazebo_resource_path = SetEnvironmentVariable(
        name="GZ_SIM_RESOURCE_PATH",
        value=[str(Path(puma560_description_dir).parent.resolve())]
    )

    ros_distro = os.environ["ROS_DISTRO"]
    physics_engine = "" if ros_distro == "humble" else "--physics-engine gz-physics-bullet-featherstone-plugin"

    robot_description = ParameterValue(
        Command(['xacro ', LaunchConfiguration('model')]), 
        value_type=str
    )

    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[{"robot_description": robot_description, "use_sim_time": True}]
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [os.path.join(get_package_share_directory("ros_gz_sim"), "launch", "gz_sim.launch.py")]
        ),
        launch_arguments=[
            ("gz_args", ["-v 4 -r empty.sdf ", physics_engine])
        ]
    )

    gz_spawn_entity = Node(
        package="ros_gz_sim",
        executable="create",
        output="screen",
        arguments=["-topic", "robot_description", "-name", "puma560"]
    )

    gz_ros2_bridge = Node(
        package="ros_gz_bridge", 
        executable="parameter_bridge", 
        arguments=["/clock@rosgraph_msgs/msg/Clock[gz.msg.Clock]"]
    )

    # Retorna a configuração do lançamento, incluindo os nós e argumentos.
    return LaunchDescription([
        model_arg,
        gazebo_resource_path, 
        robot_state_publisher_node,
        gazebo, 
        gz_spawn_entity,
        gz_ros2_bridge
    ])
