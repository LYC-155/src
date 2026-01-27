#！/usr/bin/env python3
import rclpy
from rclpy.node import Node
from my_robot_interfaces.srv import ComputeRectangleArea

class ComputeAreaServerNode(Node):

    def __init__(self):
        super().__init__("compute_rectangle_area_server") 
        self.server_ = self.create_service(ComputeRectangleArea, "compute_rectangle_area", self.callback_multiple_two_number)
        self.get_logger().info("compute rectangle area server has been started.")
    
    def callback_multiple_two_number(self, request:ComputeRectangleArea.Request, response:ComputeRectangleArea.Response):
        response.area = request.length * request.width
        self.get_logger().info(str(request.length) + "*" + str(request.width) + "=" +str(response.area))
        return response


def main(args = None):
    rclpy.init(args = args)
    node = ComputeAreaServerNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()