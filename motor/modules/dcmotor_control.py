import numpy
import struct


from can_plugins2.msg import Frame


def byteslist_of_float(n):
    bytes_n = struct.pack('>d', n)
    bytes_list = [0] * 8

    for i in range(8):
        bytes_list[i] = bytes_n[i]
    return bytes_list


def frame_get_logger_pub(node_class, frame):
    node_class.get_logger().info(f'Publish: id= {frame.id}, data= {frame.data}, dlc= {frame.dlc}')


def mode_pub(node_class, can_id, mode):
    #NodeClass内で使用する.
    #publisher(self.pub)を作ってモードをPublishする.
    #self.pub, self.can_id を上書きしてはいけない.
    node_class.pub = node_class.create_publisher(Frame, 'can_tx', 10)
    node_class.can_id = can_id
    frame = Frame()
    frame.id = can_id
    #frame.data = numpy.array([mode, 0, 0, 0, 0, 0, 0, 0], dtype=numpy.uint8)
    frame.data = [0x005, 0x000, 0x000, 0x000, 0x000, 0x000, 0x000, 0x000]
    frame.dlc = 1
    node_class.pub.publish(frame)
    frame_get_logger_pub(node_class, frame)


def speed_control_pub(node_class, speed):
    #NodeClass内で使用する.
    #速度(speed rad/s)で回す. 
    frame = Frame()
    frame.id = node_class.can_id + 1
    frame.dlc = 4
    frame.data = byteslist_of_float(speed)
    node_class.pub.publish(frame)
    frame_get_logger_pub(node_class, frame)