from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='maze_robot_gesture',
            executable='manual_gesture_publisher',
            name='manual_gesture_publisher',
            outpu='screen'
        )
    ])

#나중에 mediapipe로 바꾸면 다음과 같이 수정
# executable='hand_gesture_node',
# name='hand_gesture_node',
