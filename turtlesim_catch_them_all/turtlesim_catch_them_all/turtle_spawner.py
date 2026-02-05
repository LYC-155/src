#！/usr/bin/env python3
from os import kill
import turtle
from urllib import request
from sympy import im
import rclpy
from rclpy.node import Node
from rclpy.task import Future
from turtlesim.srv import Spawn
from turtlesim.srv import Kill
from functools import partial
import random
import math
from my_robot_interfaces.msg import Turtle
from my_robot_interfaces.msg import TurtleArray
from my_robot_interfaces.srv import CatchTurtle

class TurtleSpawnerNode(Node):#MODIFY NAME

    def __init__(self):
        super().__init__("turtle_spawner") #MODIFY NAME
        self.declare_parameter("turtle_name_prefix_", "turtle")
        self.declare_parameter("spawn_frequency", 1.0)

        self.turtle_name_prefix_ = self.get_parameter("turtle_name_prefix_").value
        self.turtle_counter_ = 1
        self.alive_turtles_ = []
        self.alive_turtle_publisher = self.create_publisher(TurtleArray, "alive_turtle", 10)
        self.spawn_client_ = self.create_client(Spawn, "/spawn")
        self.kill_client_ = self.create_client(Kill, "/kill")
        self.catch_turtle_service_ = self.create_service(CatchTurtle, 
                                                    "catch_turtle", self.callback_catch_turtle)
        self.spawn_frequency = self.get_parameter("spawn_frequency").value
        self.timer_  = self.create_timer(1.0/self.spawn_frequency, self.callback_timer_spawn_new_turtle)
    
    def callback_catch_turtle(self, request:CatchTurtle.Request, response:CatchTurtle.Response):
        self.call_kill_service(request.name)
        response.success = True
        return response

    def publish_alive_turtle(self):
        msg = TurtleArray()
        msg.turtles = self.alive_turtles_
        self.alive_turtle_publisher.publish(msg)

    def callback_timer_spawn_new_turtle(self):
        self.turtle_counter_ += 1
        name = self.turtle_name_prefix_ + str(self.turtle_counter_)
        x = random.uniform(0.0, 11.0)
        y = random.uniform(0.0, 11.0)
        theta = random.uniform(0.0, 2*math.pi)
        self.call_spawn_service(name, x, y, theta)

    def call_spawn_service(self, turtle_name:str, x:float, y:float, theta:float):
        while not self.spawn_client_.wait_for_service(1.0):
            self.get_logger().warn("waiting for turtle spawn service...")
        request = Spawn.Request()
        request.name = turtle_name
        request.x = x
        request.y = y
        request.theta = theta

        future = self.spawn_client_.call_async(request)
        future.add_done_callback(partial(self.callback_call_spawn_service, request=request))
    
    def callback_call_spawn_service(self,future:Future, request:Spawn.Request):
        response:Spawn.Response = future.result()  # type: ignore[assignment]
        if response.name != "": 
            self.get_logger().info("new turtle name: " + response.name)
            new_turtle = Turtle()
            new_turtle.name = response.name
            new_turtle.x = request.x
            new_turtle.y = request.y
            new_turtle.theta = request.theta
            self.alive_turtles_.append(new_turtle)
            self.publish_alive_turtle()
        
    def call_kill_service(self, turtle_name):
        while not self.kill_client_.wait_for_service(1.0):
            self.get_logger().warn("waiting for turtle kill service...")

        request = Kill.Request()
        request.name = turtle_name

        future = self.kill_client_.call_async(request)
        future.add_done_callback(partial(self.callback_call_kill_service, turtle_name=turtle_name))

    def callback_call_kill_service(self, future, turtle_name):
        for (i, turtle) in enumerate(self.alive_turtles_):
            if turtle.name == turtle_name:
                del self.alive_turtles_[i]
                self.publish_alive_turtle()
                break



def main(args = None):
    rclpy.init(args = args)
    node = TurtleSpawnerNode()#MODIFY NAME
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()