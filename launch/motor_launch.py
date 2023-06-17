import launch
from launch_ros.actions import ComposableNodeContainer
from launch_ros.descriptions import ComposableNode
from launch_ros.actions import Node


def generate_launch_description():
    """Generate launch description with multiple components."""
    container2 = Node(  package='motor',
                        namespace='motor',
                        executable='motor_node',
                        output='both',)
    
    container = ComposableNodeContainer(
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
    
    

    return launch.LaunchDescription([container, container2])