#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/msg/string.hpp"

using namespace std::chrono_literals;

class SmartphoneNode : public rclcpp::Node
{
public:
    SmartphoneNode() : Node("robot_news_station"), robot_name_("lyc")
    {
        pulisher_ = this -> create_publisher<example_interfaces::msg::String>("robot_news", 10);
        timer_ = this -> create_wall_timer(0.5s, std::bind(&SmartphoneNode::pulishNews, this));
        RCLCPP_INFO(this -> get_logger(), "robot news station has been stated");
    }

private:
    void pulishNews()
    {
        auto msg = example_interfaces::msg::String();
        msg.data = std::string("hi, this is ") + robot_name_;
        pulisher_ -> publish(msg);
    }

    std::string robot_name_;
    rclcpp::Publisher<example_interfaces::msg::String>::SharedPtr pulisher_;
    rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<SmartphoneNode>();//MODIFY NAME
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}