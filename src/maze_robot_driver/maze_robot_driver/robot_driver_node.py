import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist


class RobotDriverNode(Node):
    def __init__(self):
        super().__init__('robot_driver_node')

        # -----------------------------
        # Parameters
        # -----------------------------
        self.declare_parameter('cmd_vel_topic', '/cmd_vel')
        self.declare_parameter('robot_command_topic', '/robot_command')
        self.declare_parameter('max_linear_x', 0.5)
        self.declare_parameter('max_angular_z', 1.0)
        self.declare_parameter('command_timeout', 0.7)
        self.declare_parameter('publish_rate', 10.0)

        self.cmd_vel_topic = self.get_parameter('cmd_vel_topic').value
        self.robot_command_topic = self.get_parameter('robot_command_topic').value
        self.max_linear_x = self.get_parameter('max_linear_x').value
        self.max_angular_z = self.get_parameter('max_angular_z').value
        self.command_timeout = self.get_parameter('command_timeout').value
        self.publish_rate = self.get_parameter('publish_rate').value

        # -----------------------------
        # Sub/Pub
        # -----------------------------
        self.robot_command_sub = self.create_subscription(
            String,
            self.robot_command_topic,
            self.robot_command_callback,
            10
        )
        self.cmd_vel_pub = self.create_publisher(
            Twist,
            self.cmd_vel_topic,
            10
        )

        # 마지막으로 변환된 Twist 명령 저장
        self.current_cmd = Twist()
        self.last_command_time = self.get_clock().now()

        # 일정 주기로 /cmd_vel 발행
        timer_period = 1.0 / self.publish_rate
        self.timer = self.create_timer(timer_period, self.publish_cmd_vel)

        self.get_logger().info('Robot Driver Node Started')
        self.get_logger().info(f'Subscribing: {self.robot_command_topic}')
        self.get_logger().info(f'Publishing: {self.cmd_vel_topic}')
        self.get_logger().info(
            f'Max linear.x={self.max_linear_x}, '
            f'Max angular.z={self.max_angular_z}, '
            f'Timeout={self.command_timeout}s'
        )

    def robot_command_callback(self, msg: String):
        """
        /robot_command 토픽에서 String 명령을 받는다.
        예: MOVE_FORWARD, TURN_LEFT, TURN_RIGHT, STOP
        받은 문자열 명령을 Twist 속도 명령으로 변환한다.
        """

        command = msg.data
        twist = Twist()

        # 전진
        if command in ['MOVE_FORWARD', 'FORWARD']:
            twist.linear.x = self.max_linear_x
            twist.angular.z = 0.0

        # 좌회전
        elif command in ['MOVE_LEFT', 'POINT_LEFT']:
            twist.linear.x = 0.2
            twist.angular.z = self.max_angular_z

        # 우회전
        elif command in ['MOVE_RIGHT', 'POINT_RIGHT']:
            twist.linear.x = 0.2
            twist.angular.z = -self.max_angular_z
        
        # 정지
        elif command in ['STOP', 'PALM']:
            twist.linear.x = 0.0
            twist.angular.z = 0.0

        # 알 수 없는 명령
        else:
            self.get_logger().warn(f'Unknown robot command: {command}')
            twist.linear.x = 0.0
            twist.angular.z = 0.0

        twist.linear.y = 0.0
        twist.linear.z = 0.0
        twist.angular.x = 0.0
        twist.angular.y = 0.0

        self.current_cmd = twist
        self.last_command_time = self.get_clock().now()

        self.get_logger().info(
            f'Received command: {command} -> '
            f'linear.x={twist.linear.x:.2f}, '
            f'angular.z={twist.angular.z:.2f}'
        )

    def publish_cmd_vel(self):
        """
        일정 주기로 /cmd_vel에 현재 Twist 명령을 발행한다.
        단, command_timeout 동안 새 명령이 없으면 STOP을 발행한다.
        """

        now = self.get_clock().now()
        elapsed = (now - self.last_command_time).nanoseconds / 1e9

        if elapsed > self.command_timeout:
            stop_cmd = Twist()
            self.cmd_vel_pub.publish(stop_cmd)
            self.get_logger().debug('Command timeout. Publishing STOP.')
            return

        self.cmd_vel_pub.publish(self.current_cmd)

    def clamp(self, value, min_value, max_value):
        return max(min(value, max_value), min_value)


def main(args=None):
    rclpy.init(args=args)

    node = RobotDriverNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Robot Driver node stopped by keyboard interrupt')
    finally:
        # 종료 시 로봇 정지 명령 한 번 발행
        stop_cmd = Twist()
        node.cmd_vel_pub.publish(stop_cmd)

        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()