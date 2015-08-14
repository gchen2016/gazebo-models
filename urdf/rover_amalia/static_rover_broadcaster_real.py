#!/usr/bin/env python

import rospy
import sys

import tf
import time
from sensor_msgs.msg import Imu
from time import sleep

class StaticPublisher():
    def __init__(self):
        self.tf_broadcaster = tf.TransformBroadcaster()
        while(True):
            self.publish_all()
            sleep(0.001)

    def to_q(self, e):
        return tf.transformations.quaternion_from_euler(e[0], e[1], e[2])

    def publish_all(self):
        self.publish_tf('rover_amalia_leg_bar_f_r', 'rover_amalia_leg_wheel_f_r', (0, 0.075, -0.2), (0, 0, 0, 1))
        self.publish_tf('rover_amalia_leg_bar_f_l', 'rover_amalia_leg_wheel_f_l', (0, -0.075, -0.2), (0, 0, 0, 1))
        self.publish_tf('rover_amalia_leg_bar_b_r', 'rover_amalia_leg_wheel_b_r', (0, 0.075, -0.2), (0, 0, 0, 1))
        self.publish_tf('rover_amalia_leg_bar_b_l', 'rover_amalia_leg_wheel_b_l', (0, -0.075, -0.2), (0, 0, 0, 1))
        self.publish_tf('rover_amalia_chassis', 'rover_amalia_leg_bar_f_r', (0.13776, 0.17, -0.06), (0, 0, 0, 1))
        self.publish_tf('rover_amalia_chassis', 'rover_amalia_leg_bar_f_l', (0.13776, -0.17, -0.06), (0, 0, 0, 1))
        self.publish_tf('rover_amalia_chassis', 'rover_amalia_leg_bar_b_r', (-0.13776, 0.17, -0.06), (0, 0, 0, 1))
        self.publish_tf('rover_amalia_chassis', 'rover_amalia_leg_bar_b_l', (-0.13776, -0.17, -0.06), (0, 0, 0, 1))
        self.publish_tf('rover_amalia_chassis', 'rover_amalia_turret_bar', (0.195, 0, 0.11), (0, 0, 0, 1))
        self.publish_tf('rover_amalia_chassis', 'rover_amalia_rangefinder_front', (0.236, 0, -0.11), (0, 0, 0, 1))
        self.publish_tf('rover_amalia_chassis', 'rover_amalia_rangefinder_rear', (-0.236, 0, -0.11), (0, 0, 0, 1))
        self.publish_tf('rover_amalia_turret_tilt_hinge', 'rover_amalia_turret_depth_camera_link', (0, 0, 0), self.to_q((1.57, 3.1415, 1.57)))
        self.publish_tf('rover_amalia_turret_depth_camera_link', 'SwissRanger', (0, 0, 0), (0, 0, 0, 1))
        self.publish_tf('rover_amalia_turret_depth_camera_link', 'stereo', (0, 0, 0), (0, 0, 0, 1))
        self.publish_tf('odom', 'rover_amalia_chassis', (0, 0, 0), (0, 0, 0, 1))

    def publish_tf(self, from_name, to_name, v, q): 
        br = tf.TransformBroadcaster()
        br.sendTransform(v,
                        q,
                        rospy.Time.from_sec(time.time()),
                        to_name,
                        from_name)


if __name__ == "__main__":
    rospy.init_node("static_publisher")
    imu_publisher = StaticPublisher()
