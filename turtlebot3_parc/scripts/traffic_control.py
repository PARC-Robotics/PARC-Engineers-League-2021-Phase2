#!/usr/bin/env python


import os
import time
import rospy
from gazebo_msgs.srv import SpawnModel, DeleteModel
from geometry_msgs.msg import Pose


class TrafficControl():

    def __init__(self):
        # set spawn service
        self.reset_proxy = rospy.ServiceProxy('gazebo/spawn_sdf_model', SpawnModel)
        
        # initialize traffic state
        self.traffic_state = 1
        
        # set durations
        self.red_green_duration = rospy.get_param("red_green_duration")
        self.yellow_red_duration = rospy.get_param("yellow_red_duration")
        self.green_yellow_duration = rospy.get_param("green_yellow_duration")

        self.rate = rospy.Rate(1)

        # initialize traffic signal pose
        self.initial_pose = Pose()
        self.initial_pose.position.x = 0.00
        self.initial_pose.position.y = 1.75
        self.initial_pose.position.z = 0.08
        self.initial_pose.orientation.x = 0
        self.initial_pose.orientation.y = 0
        self.initial_pose.orientation.z = -0.707
        self.initial_pose.orientation.w = 0.707

        self.loadTrafficModel()
        self.controlTraffic()

    
    def loadTrafficModel(self):

        # set the model directory:
        model_dir_path = os.path.dirname(os.path.realpath(__file__))
        model_dir_path = model_dir_path.replace(
            '/turtlebot3_parc/scripts',
            '/turtlebot3_simulations/turtlebot3_gazebo/models/turtlebot3_autorace_2020')

        # load the traffic light models:
            # red
        red_light_path = model_dir_path + '/traffic_light_red/model.sdf'
        red_light_model = open(red_light_path, 'r')
        self.red_light_model = red_light_model.read()

            # yellow
        yellow_light_path = model_dir_path + '/traffic_light_yellow/model.sdf'
        yellow_light_model = open(yellow_light_path, 'r')
        self.yellow_light_model = yellow_light_model.read()

            # green
        green_light_path = model_dir_path + '/traffic_light_green/model.sdf'
        green_light_model = open(green_light_path, 'r')
        self.green_light_model = green_light_model.read()


    def controlTraffic(self):
        
        # continuous loop
        while not rospy.is_shutdown():
            if self.traffic_state == 1: # initial RED state
                rospy.wait_for_service('gazebo/spawn_sdf_model')

                spawn_model_prox = rospy.ServiceProxy('gazebo/spawn_sdf_model', SpawnModel)
                spawn_model_prox(
                    'traffic_light_red',
                    self.red_light_model,
                    "robot_ns",
                    self.initial_pose,
                    "world")

                self.traffic_state = 2
                self.current_time = time.time()


            # elif self.traffic_state == 2: # YELLOW state
            #     if abs(self.current_time - time.time()) > self.red_yellow_duration:
            #         rospy.wait_for_service('gazebo/spawn_sdf_model')

            #         spawn_model_prox = rospy.ServiceProxy('gazebo/spawn_sdf_model', SpawnModel)
            #         spawn_model_prox(
            #             'traffic_light_yellow',
            #             self.yellow_light_model,
            #             "robot_ns",
            #             self.initial_pose,
            #             "world")

            #         del_model_prox = rospy.ServiceProxy('gazebo/delete_model', DeleteModel)
            #         del_model_prox('traffic_light_red')

            #         self.traffic_state = 3
            #         self.current_time = time.time()


            elif self.traffic_state == 2: # GREEN state
                if abs(self.current_time - time.time()) > self.red_green_duration:
                    rospy.wait_for_service('gazebo/spawn_sdf_model')

                    spawn_model_prox = rospy.ServiceProxy('gazebo/spawn_sdf_model', SpawnModel)
                    spawn_model_prox(
                        'traffic_light_green',
                        self.green_light_model,
                        "robot_ns",
                        self.initial_pose,
                        "world")

                    del_model_prox = rospy.ServiceProxy('gazebo/delete_model', DeleteModel)
                    del_model_prox('traffic_light_red')

                    self.traffic_state = 3
                    self.current_time = time.time()

            elif self.traffic_state == 3: # YELLOW state
                if abs(self.current_time - time.time()) > self.green_yellow_duration:
                    rospy.wait_for_service('gazebo/spawn_sdf_model')

                    spawn_model_prox = rospy.ServiceProxy('gazebo/spawn_sdf_model', SpawnModel)
                    spawn_model_prox(
                        'traffic_light_yellow',
                        self.yellow_light_model,
                        "robot_ns",
                        self.initial_pose,
                        "world")

                    del_model_prox = rospy.ServiceProxy('gazebo/delete_model', DeleteModel)
                    del_model_prox('traffic_light_green')

                    self.traffic_state = 4
                    self.current_time = time.time()


            elif self.traffic_state == 4: # RED state
                if abs(self.current_time - time.time()) > self.yellow_red_duration:
                    rospy.wait_for_service('gazebo/spawn_sdf_model')

                    spawn_model_prox = rospy.ServiceProxy('gazebo/spawn_sdf_model', SpawnModel)
                    spawn_model_prox(
                        'traffic_light_red',
                        self.red_light_model,
                        "robot_ns",
                        self.initial_pose,
                        "world")

                    del_model_prox = rospy.ServiceProxy('gazebo/delete_model', DeleteModel)
                    del_model_prox('traffic_light_yellow')

                    self.traffic_state = 2
                    self.current_time = time.time()



def main():
    rospy.init_node('traffic_control')
    try:
        tc = TrafficControl()
    except rospy.ROSInterruptException:
        pass


if __name__ == '__main__':
    main()