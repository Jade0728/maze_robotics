from setuptools import setup
import os
from glob import glob

package_name = 'maze_robot_driver'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        (
            'share/ament_index/resource_index/packages',
            ['resource/' + package_name]
        ),
        (
            'share/' + package_name,
            ['package.xml']
        ),
        (
            os.path.join('share', package_name, 'launch'),
            glob('launch/*.launch.py')
        ),
        (
            os.path.join('share', package_name, 'config'),
            glob('config/*.yaml')
        ),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Seo Yeong',
    maintainer_email='syeong8663@gmail.com',
    description='Robot driver package for maze robot',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'robot_driver_node = maze_robot_driver.robot_driver_node:main',
        ],
    },
)