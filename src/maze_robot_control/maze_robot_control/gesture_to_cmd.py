import rclpy
from rclpy.node import Node

from std_msgs.msg import String

class GestureToCmdNode(Node):
    def __init__(self):
        super().__init__('gesture_to_cmd_node')

        self.declare_parameter('gesture_mapping.THUMBS_UP','FORWARD')
        self.declare_parameter('gesture_mapping.POINT_LEFT','MOVE_LEFT')
        self.declare_parameter('gesture_mapping.POINT_RIGHT','MOVE_RIGHT')
        self.declare_parameter('gesture_mapping.PALM','STOP')

        self.gesture_mapping={
            'THUMBS_UP': self.get_parameter('gesture_mapping.THUMBS_UP').value,
            'POINT_LEFT':self.get_parameter('gesture_mapping.POINT_LEFT').value,
            'POINT_RIGHT':self.get_parameter('gesture_mapping.POINT_RIGHT').value,
            'PALM': self.get_parameter('gesture_mapping.PALM').value
        }

        self.subscription=self.create_subscription(
            String,
            '/hand_gesture',
            self.gesture_callback,
            10
        )

        self.publisher=self.create_publisher(
            String,
            '/robot_command',
            10
        )

        self.get_logger().info('Gesture to Command node started')
        self.get_logger().info(f'Gesture mapping: {self.gesture_mapping}')


    def gesture_callback(self, msg):
        gesture=msg.data.strip()

        if gesture not in self.gesture_mapping:
            self.get_logger().warn(f'Unknown gesture received: {gesture}')
            return

        command=self.gesture_mapping[gesture]

        command_msg=String()
        command_msg.data=command

        self.publisher.publish(command_msg)

        self.get_logger().info(f'{gesture} -> {command}')


def main(args=None):
    rclpy.init(args=args)

    node=GestureToCmdNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Gesture to Command node stopped')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
