# 개발용 키보드 입력 노드
# 웹캠 없이 테스트용

import rclpy
from rclpy.node import Node 
from std_msgs.msg import String

class ManualGesturePublisher(Node):
    def __init__(self):
        super().__init__('manual_gesture_publisher')

        self.publisher_=self.create_publisher(
            String,
            '/hand_gesture',
            10
        )

        self.get_logger().info('Manual Gesture Publisher started')
        self.get_logger().info('Input keys: w=FORWARD, a=LEFT, d=RIGHT, s=STOP')

    def publish_gesture(self, gesture):
        msg=String()
        msg.data=gesture
        self.publisher_.publish(msg)
        self.get_logger().info('Published gesture: {gesture}')


def main(args=None):
    rclpy.init(args=args)

    node=ManualGesturePublisher()

    key_to_gesture = {
        'w': 'THUMBS_UP',
        'a': 'POINT_LEFT',
        'd': 'POINT_RIGHT',
        's': 'PALM'
    }

    try:
        while rclpy.ok():
            key = input('Enter command [w/a/d/s]: ').strip().lower()

            if key not in key_to_gesture:
                node.get_logger().warn('Invalid key. Use w/a/d/s.')
                continue

            gesture = key_to_gesture[key]
            node.publish_gesture(gesture)


    except KeyboardInterrupt:
        node.get_logger().info('Manual Gesture Publisher stopped')

    finally:
        node.destroy_node()
        rclpy.shutdown()



if __name__ == '__main__':
    main()