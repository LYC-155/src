#！/usr/bin/env python3
import rclpy
from rclpy.node import Node
from my_robot_interfaces.msg import LedState
from my_robot_interfaces.srv import SetLed

class BatteryNode(Node):

    def __init__(self):
        super().__init__("battery")
        self.battery_state = "full"
        self.last_time_battery_state_changed = self.get_current_time_second()
        self.battery_timer_ = self.create_timer(0.1, self.callback_battery_timer_check_state)
        self.battery_client_ = self.create_client(SetLed, "set_led_state")
        self.get_logger().info("battery node has been started.")

    def get_current_time_second(self):
        seconds, nanoseconds = self.get_clock().now().seconds_nanoseconds()
        return seconds + nanoseconds / 1000000000.0

    def callback_battery_timer_check_state(self):
        time_now = self.get_current_time_second()
        if self.battery_state == "full":
            if time_now - self.last_time_battery_state_changed > 4.0:

                self.battery_state = "empty"
                self.get_logger().info("battery is empty. charging...")
                self.call_set_led(2, 1)
                self.last_time_battery_state_changed = time_now
        elif self.battery_state == "empty":
            if time_now - self.last_time_battery_state_changed > 6.0:
                self.battery_state = "full"
                self.get_logger().info("battery is full.")
                self.call_set_led(2, 0)
                self.last_time_battery_state_changed = time_now 

    def call_set_led(self, led_number, state):
        while not self.battery_client_.wait_for_service(1.0):
            self.get_logger().warn("waiting for set led server...")

        request = SetLed.Request()
        request.led_numer = led_number
        request.state = state

        future = self.battery_client_.call_async(request)
        future.add_done_callback(self.callback_call_set_sed)

    def callback_call_set_sed(self, future):
        response:SetLed.Response= future.result()
        if response.success:
            self.get_logger().info("led turn on")
        else:
            self.get_logger().info("led not changed")

def main(args = None):
    rclpy.init(args = args)
    node = BatteryNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()