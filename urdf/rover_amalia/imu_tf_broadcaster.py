#!/usr/bin/env python

import rospy
import sys

import tf
from sensor_msgs.msg import Imu

class ImuPublisher():
    def __init__(self, from_tf_name, to_tf_name, imu_topic):
        rospy.Subscriber(imu_topic, Imu, self.on_imu_msg)
        self.tf_broadcaster = tf.TransformBroadcaster()

    def on_imu_msg(self, msg):
        q = msg.orientation
        self.tf_broadcaster.sendTransform( (0, 0, 0),
                        (q.x, q.y, q.z, q.w),
                        msg.header.stamp,
                        to_tf_name,
                        from_tf_name)
        

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print ("Usage: " + sys.argv[0] + " from_tf_name to_tf_name /imu_topic ")
        sys.exit(-1)
    rospy.init_node("imu_tf_publisher")
    from_tf_name = sys.argv[1]
    to_tf_name = sys.argv[2]
    imu_topic = sys.argv[3]
    imu_publisher = ImuPublisher(from_tf_name, to_tf_name, imu_topic)
    rospy.spin()
