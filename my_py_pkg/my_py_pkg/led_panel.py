#！/usr/bin/env python3
import rclpy
from rclpy.node import Node
from my_robot_interfaces.msg import LedState
from my_robot_interfaces.srv import SetLed

class LedPanelNode(Node):

    def __init__(self):
        super().__init__("led_panel")
        self.led_states = [0, 0, 0]
        self.pub_led_state_ = self.create_publisher(LedState, "led_state", 10)
        self.server_set_led_ = self.create_service(SetLed, "set_led_state", self.callback_set_led)
        self.timer_ = self.create_timer(4.0, self.callback_pub_led_state)
        self.get_logger().info("led_panel_publisher has been stated.")

    def callback_pub_led_state(self):
        msg = LedState()
        msg.led_states = self.led_states
        self.pub_led_state_.publish(msg)
    
    def callback_set_led(self, request:SetLed.Request, response:SetLed.Response):
        led_number = request.led_numer
        led_state = request.state
        if led_number >= len(self.led_states) or led_number < 0:
            response.success = False
            return response
        
        if led_state not in [0, 1]:
            response.success = False
            return response
        
        self.led_states[led_number] = led_state
        self.callback_pub_led_state()
        response.success = True
        return response



def main(args = None):
    rclpy.init(args = args)
    node = LedPanelNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()