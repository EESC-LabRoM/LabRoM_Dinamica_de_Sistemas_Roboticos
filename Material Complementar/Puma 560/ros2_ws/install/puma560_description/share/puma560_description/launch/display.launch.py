import os
import launch
from launch.substitutions import LaunchConfiguration
import launch_ros.actions

def generate_launch_description():
    # Get the path to the puma560_description package
    pkgPath = launch_ros.substitutions.FindPackageShare(package='puma560_description').find('puma560_description')
    # Path to the URDF file
    urdfModelPath = os.path.join(pkgPath, 'urdf', 'puma560_description.xacro')
    # Path to the RViz configuration file
    rvizConfigPath = os.path.join(pkgPath, 'rviz2', 'puma560_config.rviz')

    # Ensure paths are correct
    print(f"URDF Path: {urdfModelPath}")
    print(f"RViz Config Path: {rvizConfigPath}")

    # Read the URDF file
    with open(urdfModelPath, 'r') as infp:
        robot_desc = infp.read()

    # Parameters for the nodes
    params = {'robot_description': robot_desc}

    # Define the nodes
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

    # Launch description
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

if __name__ == '__main__':
    generate_launch_description()
