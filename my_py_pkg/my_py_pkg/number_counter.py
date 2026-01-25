#！/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.msg import Int64
from example_interfaces.srv import SetBool

class NumberCounterNode(Node):

    def __init__(self):
        super().__init__("number_counter") 
        self.counter_ = 0
        self.number_subscriber_ = self.create_subscription(Int64, "number", 
                                                           self.callback_number, 10)
        self.number_count_publisher_ = self.create_publisher(Int64, 
                                                             "number_count", 10)
        self.reset_counter_service_ = self.create_service(SetBool, "reset_couter",
                                                           self.callback_reset_counter)
        
        self.get_logger().info("number counter has been started")
    
    def callback_number(self, msg:Int64):
        #self.get_logger().info(msg.data)
        self.counter_ += msg.data
        new_msg = Int64()
        new_msg.data = self.counter_ - 2
        self.number_count_publisher_.publish(new_msg)
    
    def callback_reset_counter(self,request:SetBool.Request, response:SetBool.Response):
        if request.data:
            self.counter_ = 0
            response.success = True
            response.message = "counter has been reseted."
        else:
            response.success = False
            response.message = "counter has not been reseted."
        return response
        

def main(args = None):
    rclpy.init(args = args)
    node = NumberCounterNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()