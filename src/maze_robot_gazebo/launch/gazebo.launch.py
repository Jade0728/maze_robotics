import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition, UnlessCondition
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    package_name = 'maze_robot_gazebo'

    world_path = os.path.join(
        get_package_share_directory(package_name),
        'worlds',
        'maze.world'
    )

    gui = LaunchConfiguration('gui')

    declare_gui = DeclareLaunchArgument(
        'gui',
        default_value='true',
        description='Set to false to run gzserver only'
    )

    gzserver = ExecuteProcess(
        cmd=[
            'gzserver',
            '--verbose',
            world_path,
            '-s',
            'libgazebo_ros_init.so',
            '-s',
            'libgazebo_ros_factory.so'
        ],
        output='screen'
    )

    gzclient = ExecuteProcess(
        cmd=['gzclient'],
        output='screen',
        condition=IfCondition(gui)
    )

    return LaunchDescription([
        declare_gui,
        gzserver,
        gzclient,
    ])