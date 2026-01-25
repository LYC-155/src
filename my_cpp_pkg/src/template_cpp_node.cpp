#include "rclcpp/rclcpp.hpp"

class SmartphoneNode : public rclcpp::Node //MODIFY NAME
{
public:
    SmartphoneNode() : Node("node_name")//MODIFY NAME
    {

    }

private:
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<SmartphoneNode>();//MODIFY NAME
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}