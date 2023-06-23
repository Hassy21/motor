import sys
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
import numpy
import struct
from std_msgs.msg import String
import ctypes

from can_plugins2.msg import Frame
import motor.modules.dcmotor_control as dcmotor_control


speed = 1
can_id = 0x16C
mode = 5


class TestControl(Node):
    
    def __init__(self):
        super().__init__('motor_node')
        self.i = 0

        dcmotor_control.mode_pub(self, can_id, mode)
        self.timer = self.create_timer(1, lambda: self.timer_callback())


    def timer_callback(self):
        if(self.i < 3):
            dcmotor_control.mode_pub(self, can_id, mode)
            self.i += 1
        else:
            ispeed = speed + speed * (self.i % 2)
            dcmotor_control.speed_control_pub(self, ispeed)
            self.i += 1
    


def main():
    rclpy.init()
    node = TestControl()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    except ExternalShutdownException:
        sys.exit(1)
    finally:
        node.destroy_node()
        rclpy.try_shutdown()