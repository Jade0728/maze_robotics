from setuptools import setup
import os
from glob import glob
package_name='maze_robot_gesture'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
        ['resource/'+ package_name]),
        ('share/'+package_name,['package.xml']),
        (os.path.join('share',package_name,'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='swu',
    maintainer_email="syeong8663@gmail.com",
    description='Gesture input package for maze robot',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'manual_gesture_publisher=maze_robot_gesture.manual_gesture_publisher:main',
            'hand_gesture_node=maze_robot_gesture.hand_gesture_node:main',
         ],
    },
)