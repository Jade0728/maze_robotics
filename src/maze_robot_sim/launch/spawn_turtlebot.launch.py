import os

from launch import LaunchDescription
from launch.actions import ExecuteProcess, TimerAction
from launch.substitutions import EnvironmentVariable
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    turtlebot3_model = EnvironmentVariable('TURTLEBOT3_MODEL', default_value='burger')

    turtlebot3_gazebo_dir = get_package_share_directory('turtlebot3_gazebo')

    urdf_path = os.path.join(
        turtlebot3_gazebo_dir,
        'models',
        'turtlebot3_burger',
        'model.sdf'
    )

    # turtle bot이 처음 등장하는 위치
    spawn_turtlebot = ExecuteProcess(
        cmd=[
            'ros2', 'run', 'gazebo_ros', 'spawn_entity.py',
            '-entity', 'turtlebot3_burger',
            '-file', urdf_path,
            '-x', '-6.0',
            '-y', '-4.0',
            '-z', '0.01'
        ],
        output='screen'
    )

    return LaunchDescription([
        TimerAction(
            period=2.0,
            actions=[spawn_turtlebot]
        )
    ])