import os
import launch
from launch.substitutions import LaunchConfiguration
import launch_ros.actions

def generate_launch_description():
    pkgPath = launch_ros.substitutions.FindPackageShare(package='robot_description').find('robot_description')
    urdfModelPath = os.path.join(pkgPath, 'urdf', 'robot_example.urdf')  # Adjusted to include the file extension
    rvizConfigPath = os.path.join(pkgPath, 'config', 'config.rviz')

    print(urdfModelPath)

    with open(urdfModelPath, 'r') as infp:
        robot_desc = infp.read()

    params = {'robot_description': robot_desc}

    robot_state_publisher_node = launch_ros.actions.Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[params]
    )

    joint_state_publisher_node = launch_ros.actions.Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        parameters=[params]
    )

    joint_state_publisher_gui_node = launch_ros.actions.Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        condition=launch.conditions.IfCondition(LaunchConfiguration('gui'))
    )

    rviz_node = launch_ros.actions.Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rvizConfigPath]
    )

    return launch.LaunchDescription([
        launch.actions.DeclareLaunchArgument(
            name='gui', default_value='True',
            description='Flag to enable joint_state_publisher_gui'
        ),
        robot_state_publisher_node,
        joint_state_publisher_node,
        joint_state_publisher_gui_node,
        rviz_node
    ])
