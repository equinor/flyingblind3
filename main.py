#!/usr/bin/env python

from __future__ import print_function
import bfs

import rospy

import random
import math

from dronelib import Drone
import util

from ascend_msgs.srv import GlobalMap
from geometry_msgs.msg import Pose, PoseArray


def goal_callback(msg):
    global goal
    goal = msg.position

def dynamic_obstacles_callback(msg):
    global obstacles
    obstacles = msg.poses

def boost_callback(msg):
    global boosts
    boosts = msg.poses

def goto(x,y,rospy,rate,drone):
    print('goal is', goal)
    x = x + 0.5
    y = y + 0.5
    loccounter = 0

    while not rospy.is_shutdown():
        rate.sleep()
        # -------------------------------
        # ------Replace this example-----
        # ---------with your code!-------
        # -------------------------------
        # Find how far we are away from target
        distance_to_target = ((x - drone.position.x)**2 +
                              (y - drone.position.y)**2)**0.5

        # Do special action if we are close
        if distance_to_target < 0.1:
            loccounter = loccounter+1
            # Print current distance to goal. Note that we 
            # wont reach the goal, since we just move randomly
            distance_to_goal = ((drone.position.x - x)**2 +
                                (drone.position.y - y)**2)**0.5

            print("Distance to goal is now", distance_to_goal)
            if loccounter > 3:
                loccounter=0
                break

            # Generate some random point and rotation
        target_x = x #random.randint(-3, 3)
        target_y = y #random.randint(-3, 3)
            
        print('current position',x,y,drone.position.x,drone.position.y)
            # Move to random point
        drone.set_target(target_x, target_y)
        print("distance to target:", distance_to_target)

def main():
    # Init ROS node
    rospy.init_node('task', anonymous=True)

    # Create subscriber for position, goal, boost points, and obstacles
    rospy.Subscriber('/goal', Pose, goal_callback)
    rospy.Subscriber('/boost', PoseArray, boost_callback)
    rospy.Subscriber("/dynamic_obstacles", PoseArray, dynamic_obstacles_callback)

    # Wait for resources to become active
    goal = rospy.wait_for_message("/goal", Pose).position
    boosts = rospy.wait_for_message("/boost", PoseArray).poses
    obstacles = rospy.wait_for_message("/dynamic_obstacles", PoseArray).poses

    # Create map service client
    getMap = rospy.ServiceProxy('/GlobalMap', GlobalMap)
    rospy.wait_for_service('/GlobalMap')

    try:
        raw_map = getMap()
    except rospy.ServiceException as e:
        print("Map service error: " + str(e))
        return

    # Get map as 2D list
    world_map = util.parse_map(raw_map)

    shortest_path = bfs.bfs(world_map, (0,0), (goal.y, goal.x))

    # Print resources
    print("Wall layout:")
    util.print_map(world_map)
    print("Boost points:")
    util.print_positions(boosts)
    print("Obstacles at start:")
    util.print_positions(obstacles)

    # Initialize drone
    drone = Drone()
    drone.takeoff()

    # -- For example code --
    target_x = 0
    target_y = 0
    drone.set_target(target_x, target_y)

    rate = rospy.Rate(30)
    print('there is a test')
    i = 0
    targets = [[0,0],[1,0],[1,7],[2,7],[16,7],[17,7],[19,7],[19,20]]


    for t in targets:
        goto(t[0],t[1],rospy,rate,drone)


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        print('exception happened')
        pass
