from setuptools import setup
import os
from glob import glob

package_name = 'maze_robot_control'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
         ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),

        # launch 파일 설치
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),

        # config 파일 설치
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Seo Yeong',
    maintainer_email='syeong8663@gmail.com',
    description='Convert hand gestures to robot commands',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'gesture_to_cmd=maze_robot_control.gesture_to_cmd:main',
        ],
    },
)