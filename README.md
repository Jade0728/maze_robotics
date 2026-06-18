# Hand Gesture Maze Robot

사용자의 손동작을 실시간으로 인식하고, ROS2 토픽 통신을 통해 TurtleBot을 제어하여 Gazebo 미로를 탈출하는 로봇 프로젝트입니다.

## Project Overview

본 프로젝트는 노트북 카메라로 손동작을 인식한 뒤, 이를 로봇 이동 명령으로 변환하여 Gazebo 시뮬레이션 환경의 TurtleBot을 제어합니다.

## System Architecture

Hand Gesture Node  
→ Gesture to Command Node  
→ Robot Driver Node  
→ TurtleBot / Gazebo

## Features

- MediaPipe 기반 손동작 인식
- ROS2 Publisher / Subscriber 기반 노드 통신
- 손동작 명령을 로봇 주행 명령으로 변환
- Gazebo 미로 환경 구성
- TurtleBot3 Burger 시뮬레이션 주행

## Demo
youtube demo: https://www.youtube.com/watch?v=ViuENF6v88c
발표 demo: 

## RUN, LAUNCH, 웹캠 연결
Node, Gazebo, TurtleBot run, launch
```
source install/setup.bash
ros2 run maze_robot_gesture manual_gesture_publisher
ros2 run maze_robot_gesture hand_gesture_node
ros2 run maze_robot_control gesture_to_cmd
ros2 run maze_robot_driver robot_driver_node
ros2 launch maze_robot_gazebo gazebo.launch.py
ros2 launch maze_robot_sim spawn_turtlebot.launch.py
```
웹캠 연결: 노트북 환경에 따라 연결 방법이 다를 수 있음, powershell 을 통해 연결
```
usbipd bind --busid 1-6
usbipd attach --wsl --busid 1-6
```

## Project Structure

```text
maze_robotics/
├── src/
│   ├── maze_robot_gesture/
│   ├── maze_robot_control/
│   ├── maze_robot_driver/
│   ├── maze_robot_gazebo/
│   └── maze_robot_sim/
├── README.md
└── .gitignore
