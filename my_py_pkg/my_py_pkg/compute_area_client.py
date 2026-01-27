#！/usr/bin/env python3
import rclpy
from rclpy.node import Node
from my_robot_interfaces.srv import ComputeRectangleArea
from functools import partial

class ComputeAreaClient(Node):
    def __init__(self):
        super().__init__("compute_rectangle_area_client")
        self.client_ = self.create_client(ComputeRectangleArea, "compute_rectangle_area")
    
    def call_multiple_two_number(self, a:float, b:float):
        while not self.client_.wait_for_service(1.0):
            self.get_logger().warn("waiting for compute area server...")

        request = ComputeRectangleArea.Request()
        request.length = a
        request.width = b

        future = self.client_.call_async(request)
        future.add_done_callback(
            partial(self.callback_call_add_two_ints, request = request))
    
    def callback_call_add_two_ints(self, future, request):
        response = future.result()
        self.get_logger().info(str(request.length) + " * " + str(request.width) 
                               + " = " +str(response.area))

def main(args = None):
    rclpy.init(args = args)
    node =ComputeAreaClient()
    node.call_multiple_two_number(4.65, 7.85)
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()