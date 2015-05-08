#!/usr/bin/env python
import rospy
import sys

import tf
from sensor_msgs.msg import JointState
from tf.transformations import quaternion_from_euler
import time

class FlirPublisher():
    def __init__(self):
        rospy.Subscriber('/ptu/state', JointState, self.on_ptu_state_msg)

    def on_ptu_state_msg(self, msg):
        pan1 = -msg.position[0]
        pan_q = quaternion_from_euler(0, 0, -pan1)
        tilt_q = quaternion_from_euler(0, -msg.position[1], 0)
        b2 = tf.TransformBroadcaster()
        b2.sendTransform( (0.0, 0, 0.065),
                        tilt_q, 
                        rospy.Time.from_sec(time.time()),
                        'rover_amalia_turret_tilt_hinge',
                        'rover_amalia_turret_tilt_base')
        

if __name__ == "__main__":
    rospy.init_node("flir_tf_publisher_tilt")
    odom_publisher = FlirPublisher()
    rospy.spin()
