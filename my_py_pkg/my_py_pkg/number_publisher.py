#！/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter
from example_interfaces.msg import Int64

class NumberPublisherNode(Node):

    def __init__(self):
        super().__init__("number_publisher") #node name
        self.declare_parameter("number", 2)
        self.declare_parameter("timer", 1.0)
        self.number_ = self.get_parameter("number").value
        self.get_timer_para = self.get_parameter("timer").value
        self.add_post_set_parameters_callback(self.parameters_callback)
        
        self.number_publishers_ = self.create_publisher(Int64, "number",10) #topic name leading "/" which mean cannot change namespace
        self.number_timer_ = self.create_timer(self.get_timer_para, self.callback_publish_number)
        self.get_logger().info("numer_publisher has been started")

    def callback_publish_number(self):
        msg = Int64()
        msg.data = self.number_
        self.number_publishers_.publish(msg)

    def parameters_callback(self, params: list[Parameter]):
        for param in params:
            if param.name == "number":
                self.number_ = param.value

def main(args = None):
    rclpy.init(args = args)
    node = NumberPublisherNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()