#!/usr/bin/env python

import rospy
import sys

import tf
from nav_msgs.msg import Odometry

class OdomPublisher():
    def __init__(self, from_tf_name, to_tf_name, odom_topic):
        rospy.Subscriber(odom_topic, Odometry, self.on_odom_msg)
        self.tf_broadcaster = tf.TransformBroadcaster()

    def on_odom_msg(self, msg):
        pose = msg.pose.pose.position
        self.tf_broadcaster.sendTransform( (pose.x, pose.y, 0),
                        (0, 0, 0, 1), 
                        msg.header.stamp,
                        #rospy.Time(),
                        to_tf_name,
                        from_tf_name)
        

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print ("Usage: " + sys.argv[0] + " from_tf_name to_tf_name /odom_topic ")
        sys.exit(-1)
    rospy.init_node("odom_tf_publisher")
    from_tf_name = sys.argv[1]
    to_tf_name = sys.argv[2]
    odom_topic = sys.argv[3]
    odom_publisher = OdomPublisher(from_tf_name, to_tf_name, odom_topic)
    rospy.spin()
