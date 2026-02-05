#！/usr/bin/env python3
import math
import turtle
from urllib import response
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from my_robot_interfaces.msg import Turtle
from my_robot_interfaces.msg import TurtleArray
from my_robot_interfaces.srv import CatchTurtle
from functools import partial

class TurtleController(Node):#NODE CLASS NAME

    def __init__(self):
        super().__init__("turtle_controller") #NODE NAME
        self.declare_parameter("catch_closest_turtle_first", True)
        self.catch_closest_turtle_first = self.get_parameter("catch_closest_turtle_first").value
        
        self.turtle_to_catch_:Turtle = None # type: ignore[assignment]
        self.pose_:Pose = None              # type: ignore[assignment]
        self.cmd_vel_publisher = self.create_publisher(Twist,
                                                    "/turtle1/cmd_vel", 10)
        self.pose_subscriber_ = self.create_subscription(Pose,
                                                    "/turtle1/pose", self.callback_pose, 10)
        self.alive_subscriber_  = self.create_subscription(TurtleArray, 
                                                    "alive_turtle", self.callback_alive_turtle,10)
        self.catch_turtle_client = self.create_client(CatchTurtle, "catch_turtle")
        self.control_loop_timer = self.create_timer(0.01, self.control_loop)

    def callback_pose(self, pose:Pose):
        self.pose_  = pose

    def callback_alive_turtle(self, msg:TurtleArray):
        if len(msg.turtles) > 0:
            if self.catch_closest_turtle_first:
                closest_turtle = None
                closest_turtle_distance = None

                for turtle in msg.turtles:
                    dis_x = turtle.x - self.pose_.x
                    dis_y = turtle.y - self.pose_.y
                    distance = math.sqrt(dis_x * dis_x + dis_y * dis_y)
                    if closest_turtle ==None or distance < closest_turtle_distance: # type: ignore[assignment]
                        closest_turtle = turtle
                        closest_turtle_distance = distance
                self.turtle_to_catch_ = closest_turtle # type: ignore[assignment]
            else:
                self.turtle_to_catch_ = msg.turtles[0]


    def control_loop(self):
        if self.pose_ == None or self.turtle_to_catch_ == None:
            return
        dis_x = self.turtle_to_catch_.x - self.pose_.x
        dis_y = self.turtle_to_catch_.y - self.pose_.y
        distance = math.sqrt(dis_x * dis_x + dis_y * dis_y)

        cmd = Twist()

        if distance > 0.5:
            #position
            cmd.linear.x = 2*distance

            #orientation
            global_theta = math.atan2(dis_y, dis_x)
            diff = global_theta - self.pose_.theta

            if diff > math.pi:
                diff -= 2*math.pi
            elif diff < -math.pi:
                diff += 2*math.pi

            cmd.angular.z = 6*diff
        else:
            #target reached
            cmd.linear.x = 0.0
            cmd.angular.z = 0.0
            self.call_catch_service(self.turtle_to_catch_.name)
            self.turtle_to_catch_ = None # type: ignore[assignment]

        self.cmd_vel_publisher.publish(cmd)

    def call_catch_service(self, turtle_name):
        while not self.catch_turtle_client.wait_for_service(1.0):
            self.get_logger().warn("waiting for turtle catch service...")

        request = CatchTurtle.Request()
        request.name = turtle_name

        future = self.catch_turtle_client.call_async(request)
        future.add_done_callback(partial(self.callback_call_catch_service, turtle_name=turtle_name))

    def callback_call_catch_service(self, future, turtle_name):
        response:CatchTurtle.Response = future.result()
        if not response.success:
            self.get_logger().error("Turtle " + turtle_name + " could not be removed")

def main(args = None):
    rclpy.init(args = args)
    node = TurtleController()#NODE CLASS NAME
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()