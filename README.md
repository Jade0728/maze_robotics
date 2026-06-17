# Hand Gesture Maze Robot Game

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