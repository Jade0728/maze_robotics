from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

import os


def generate_launch_description():
    package_name = 'maze_robot_driver'

    config_path = os.path.join(
        get_package_share_directory(package_name),
        'config',
        'driver_params.yaml'
    )

    driver_node = Node(
        package=package_name,
        executable='robot_driver_node',
        name='robot_driver_node',
        output='screen',
        parameters=[config_path]
    )

    return LaunchDescription([
        driver_node
    ])