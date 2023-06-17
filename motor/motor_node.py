import sys
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
import numpy
import struct
from std_msgs.msg import String

from can_plugins2.msg import Frame
import motor.modules.dcmotor_control as dcmotor_control


speed = 1
can_id = 0x160
mode = 5


class TestControl(Node):
    def mode_pub(node_class, can_id, mode):
        #NodeClass内で使用する.
        #publisher(self.pub)を作ってモードをPublishする.
        #self.pub, self.can_id を上書きしてはいけない.
        node_class.pub = node_class.create_publisher(String, 'can_tx2', 10)
        node_class.can_id = can_id
        frame = Frame()
        frame.id = can_id
        #frame.data = numpy.array([mode, 0, 0, 0, 0, 0, 0, 0], dtype=numpy.uint8)
        frame.data = [0x005, 0x000, 0x000, 0x000, 0x000, 0x000, 0x000, 0x000]
        frame.dlc = 1
        msg = String()
        msg.data = f'sss'
        node_class.pub.publish(msg)#
        dcmotor_control.frame_get_logger_pub(node_class, frame)

    def speed_control_pub(node_class, speed):
        #NodeClass内で使用する.
        #速度(speed rad/s)で回す. 
        frame = Frame()
        frame.id = node_class.can_id + 1
        frame.dlc = 4
        frame.data = dcmotor_control.byteslist_of_float(speed)
        msg = String()
        msg.data = f'st'
        node_class.pub.publish(msg)#
        dcmotor_control.frame_get_logger_pub(node_class, frame)


    def __init__(self):
        super().__init__('motor_node')
        self.i = 0

        self.mode_pub(can_id, mode)
        self.timer = self.create_timer(1, lambda: self.timer_callback())


    def timer_callback(self):
        ispeed = speed + speed * (self.i % 2)
        self.speed_control_pub(ispeed)
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