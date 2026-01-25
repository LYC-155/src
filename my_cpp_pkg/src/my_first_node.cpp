#include "rclcpp/rclcpp.hpp"

class SmartphoneNode : public rclcpp::Node
{
private:
    void timerCallback()
    {
        RCLCPP_INFO(this->get_logger(), "hello%d", counter_);
        counter_ ++;
    }
    rclcpp::TimerBase::SharedPtr timer_;
    int counter_;
    
public:
    SmartphoneNode() : Node("cpp_test"), counter_(0)
    {
        RCLCPP_INFO(this->get_logger(), "LYC");
        timer_ = this->create_wall_timer(std::chrono::seconds(1),
                                        std::bind(&SmartphoneNode::timerCallback,this));
    }
    
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<SmartphoneNode>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}