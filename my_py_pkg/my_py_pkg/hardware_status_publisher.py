import rclpy
from rclpy.node import Node
from my_robot_interfaces.msg import HardwareStatus

class HardwareStatusPulisherNode(Node):

    def __init__(self):
        super().__init__("hardware_status_pulisher") 
        self.hw_status_pub_ = self.create_publisher(HardwareStatus, "hardware_status", 10)
        self.timer_ = self.create_timer(1.0, self.callback_hw_status_pub)
        self.get_logger().info("hardware_status_pulisher has been started.")

    def callback_hw_status_pub(self):
        msg = HardwareStatus()
        msg.temperature = 43.7
        msg.are_motors_ready = True
        msg.debug_message = "noting special"
        self.hw_status_pub_.publish(msg)
        
def main(args = None):
    rclpy.init(args = args)
    node = HardwareStatusPulisherNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()