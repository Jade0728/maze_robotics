from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

import os

def generate_launch_description():
    config_path=os.path.join(
        get_package_share_directory('maze_robot_control'),
        'config',
        'gesture_mapping.yaml'
    )

    gesture_to_cmd_node=Node(
        package='maze_robot_control',
        executable='gesture_to_cmd',
        name='gesture_to_cmd_node',
        parameters=[config_path],
        output='screen'
    )

    return LaunchDescription([
        generate_to_cmd_node
    ])