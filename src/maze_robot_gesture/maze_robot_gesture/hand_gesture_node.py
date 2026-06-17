import cv2
import mediapipe as mp

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class HandGestureNode(Node):
    def __init__(self):
        super().__init__('hand_gesture_node')

        self.publisher = self.create_publisher(String, '/hand_gesture', 10)

        self.declare_parameter('camera_index', 0)
        self.declare_parameter('publish_rate', 10.0)
        self.declare_parameter('show_window', True)

        self.camera_index = self.get_parameter('camera_index').value
        self.publish_rate = self.get_parameter('publish_rate').value
        self.show_window = self.get_parameter('show_window').value

        self.cap = cv2.VideoCapture(self.camera_index, cv2.CAP_V4L2)

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 320)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

        if not self.cap.isOpened():
            self.get_logger().error('Camera open failed. Check /dev/video0 or camera_index.')
        else:
            self.get_logger().info('Camera opened successfully.')

        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils

        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            model_complexity=1,
            min_detection_confidence=0.6,
            min_tracking_confidence=0.6
        )

        self.last_gesture = 'NONE' 

        # 0.1초마다 한 번씩 카메라 프레임을 읽고 손동작을 판단
        timer_period = 1.0 / self.publish_rate
        self.timer = self.create_timer(timer_period, self.timer_callback)

        self.get_logger().info('MediaPipe hand gesture node started.')

    def timer_callback(self):
        ret, frame = self.cap.read()

        if not ret:
            self.get_logger().warn('Failed to read frame from camera.')
            return

        frame = cv2.flip(frame, 1) # 좌우반전

        # OpenCV는 BGR, MediaPipe는 RGB 사용
        # frame = cv2.flip(frame, 1) #좌우 반전
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        result = self.hands.process(rgb_frame)

        gesture = 'NONE' # 일단 NONE으로 초기화(손이 안보이거나 판단이 애매하면 NONE이 됨)

        # 손이 인식되면 landmark 가져오기
        if result.multi_hand_landmarks:
            self.get_logger().info('Hand detected') # 로그
            hand_landmarks = result.multi_hand_landmarks[0]
            gesture = self.classify_gesture(hand_landmarks)
            # 손관절을 화면에 그리기
            if self.show_window:
                self.mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS
            )
        else:
            self.get_logger().info('No Hand Detected') # 로그
        

        # 테스트용
        msg = String()
        msg.data = gesture
        self.publisher.publish(msg)

        self.get_logger().info(f'Published gesture: {gesture}')
        self.last_gesture = gesture
        # opencv 창 위에 현재 인식된 손동작을 글자로 보여줌 ex) Gesture: THUMBS_UP
        if self.show_window:
            cv2.putText(
                frame,
                f'Gesture: {gesture}',
                (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )
            
            # 창 크기 조절
            if self.show_window:
                cv2.namedWindow('MediaPipe Hand Gesture', cv2.WINDOW_NORMAL)
                cv2.imshow('MediaPipe Hand Gesture', frame)
                cv2.resizeWindow('MediaPipe Hand Gesture', 700, 580)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'): # q를 누르면 QUIT publish
                self.publish_quit()

    def classify_gesture(self, hand_landmarks):
        lm = hand_landmarks.landmark

        def dist(a, b):
            return ((a.x - b.x) ** 2 + (a.y - b.y) ** 2) ** 0.5


        # landmark 번호
        # thumb: 4, index: 8, middle: 12, ring: 16, pinky: 20
        # 손가락 관절 기준점: index 6, middle 10, ring 14, pinky 18

        wrist=lm[0]

        thumb_tip = lm[4]
        thumb_ip = lm[3]

        index_mcp = lm[5]
        index_tip = lm[8]
        index_pip = lm[6]

        middle_tip = lm[12]
        middle_pip = lm[10]

        ring_tip = lm[16]
        ring_pip = lm[14]

        pinky_tip = lm[20]
        pinky_pip = lm[18]

        # 손 크기 기준값: 손이 카메라에서 멀어지면 threshold도 같이 줄어들게
        hand_size=dist(wrist, index_mcp)

        # y 좌표는 화면 위쪽이 작고, 아래쪽이 큼
        index_up = index_tip.y < index_pip.y
        middle_up = middle_tip.y < middle_pip.y
        ring_up = ring_tip.y < ring_pip.y
        pinky_up = pinky_tip.y < pinky_pip.y
        thumb_up = thumb_tip.y < thumb_ip.y

        # 1. 손바닥: 네 손가락이 모두 펴진 상태
        if index_up and middle_up and ring_up and pinky_up:
            return 'PALM'

        # 2. 엄지척: 엄지만 위로, 나머지 손가락은 접힘
        if thumb_up and not index_up and not middle_up and not ring_up and not pinky_up:
            return 'THUMBS_UP'

        # 3. 검지로 좌우 판단
        dx=index_tip.x - index_mcp.x
        dy=index_tip.y - index_mcp.y
        
        # 검지가 펴져있는지
        index_extended=dist(index_tip, index_mcp)>dist(index_pip, index_mcp) * 1.2

        # 검지가 수평방향인지
        index_horizontal=abs(dx)>abs(dy)*0.8

        # 손 크기에 따른 동적 threshold
        direction_threshold=hand_size*0.25

        index_horizontal_left=dx < -direction_threshold
        index_horizontal_right=dx > direction_threshold

        # 나머지 손가락이 졉혀있는지 확인
        # tip이 pip 보다 아래에 있으면 접힌 것으로 판단
        middle_folded = middle_tip.y > middle_pip.y
        ring_folded = ring_tip.y > ring_pip.y
        pinky_folded = pinky_tip.y > pinky_pip.y

        folded_count = sum([middle_folded, ring_folded, pinky_folded])
        other_fingers_folded = folded_count >= 2

        if index_extended and index_horizontal and other_fingers_folded:
            if index_horizontal_left:
                return 'POINT_LEFT'
            elif index_horizontal_right:
                return 'POINT_RIGHT'

        return 'NONE'


    def destroy_node(self):
        if self.cap.isOpened():
            self.cap.release()
        cv2.destroyAllWindows()
        self.hands.close()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = HandGestureNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Keyboard interrupt.')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()