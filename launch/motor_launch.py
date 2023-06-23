import launch
from launch_ros.actions import ComposableNodeContainer
from launch_ros.descriptions import ComposableNode
from launch_ros.actions import Node


def generate_launch_description():
    """Generate launch description with multiple components."""
    container1 = Node(  package='motor',
                        namespace='',
                        executable='motor_node',
                        output='both',)
    
    container2 = Node(  package='my_happy_topic',
                        namespace ='',
                        executable='my_happy_publisher_node', 
                        output='both',)
    
    container3 = ComposableNodeContainer(
            name='test_node',
            namespace='',
            package='rclcpp_components',
            executable='component_container',
            composable_node_descriptions=[
                ComposableNode(
                    package='can_plugins2',
                    plugin='slcan_bridge::SlcanBridge',
                    name='slcan_bridge'),
            ],
                
            output='both',
        )
    
    

    return launch.LaunchDescription([container1, container3])