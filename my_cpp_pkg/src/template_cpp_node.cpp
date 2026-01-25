#include "rclcpp/rclcpp.hpp"

class CustomNode : public rclcpp::Node //MODIFY NAME
{
public:
    CustomNode() : Node("node_name")//MODIFY NAME
    {

    }

private:
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<CustomNode>();//MODIFY NAME
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}