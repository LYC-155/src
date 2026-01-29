from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld  = LaunchDescription()
    
    number_pulisher = Node(
        package="my_py_pkg",
        executable="number_publisher"
    )

    number_counter = Node(
        package="my_py_pkg",
        executable="number_counter"
    )

    ld.add_action(number_pulisher)
    ld.add_action(number_counter)
    return ld