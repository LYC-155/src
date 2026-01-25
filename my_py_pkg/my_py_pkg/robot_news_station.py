#！/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.msg import String

class RobotNewsStationNode(Node):#MODIFY NAME

    def __init__(self):
        super().__init__("robot_news_station") #MODIFY NAME
        self.publishers_ = self.create_publisher(String, "robot_news", 10)
        self.timer_ = self.create_timer(0.5, self.pulish_news)
        self.get_logger().info("robot news station has been started")

    def pulish_news(self):
        msg = String()
        msg.data = "hi, lyc"
        self.publishers_.publish(msg)


def main(args = None):
    rclpy.init(args = args)
    node = RobotNewsStationNode()#MODIFY NAME
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()