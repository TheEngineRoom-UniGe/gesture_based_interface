#!/usr/bin/env python

import sys
import rospy
from BaxterGBI_pbr.srv import *
from BaxterGBI_pbr.msg import *


import os


"""
Node used to test the pbr_server.
Based on the input it will ask for record or playback service from the pbr_server.
"""

def call_playback(filename, loops, scale_vel):
    """Call the playback function provided by pbr_server."""
    rospy.wait_for_service('playback')
    try:
        playback = rospy.ServiceProxy('playback', Playback)
        msg = playback_msg()
        msg.filename = filename
        msg.loops = loops
        msg.scale_vel = scale_vel
        isOk = playback(msg)
    except rospy.ServiceException, e:
        rospy.logerr("Service call failed: %s"%e)

def call_record(filename, record_rate, mode):
    """Call the record function provided by pbr_server."""
    if mode == 1:
        rospy.wait_for_service('record_start')
        try:
            record_start = rospy.ServiceProxy('record_start', RecordStart)
            isOk = record_start(filename, record_rate)
        except rospy.ServiceException, e:
            rospy.logerr("Service call failed: %s"%e)
    elif mode == 0:
        rospy.wait_for_service('record_stop')
        try:
            record_stop = rospy.ServiceProxy('record_stop', RecordStop)
            isOk = record_stop()
        except rospy.ServiceException, e:
            rospy.logerr( "Service call failed: %s"%e)
        

def call_list_files():

    rospy.wait_for_service('files')
    try:
        files = rospy.ServiceProxy('files', ListFiles)
        list_files = files()
        rospy.loginfo(list_files.list_files)
    except rospy.ServiceException, e:
        rospy.logerr("Service call failed: %s"%e)


def call_delete_file(filename):

    rospy.wait_for_service('delete_file')
    try:
        deleteFile = rospy.ServiceProxy('delete_file', DeleteFile)
        response = deleteFile(filename)
        if response.isError == 0:
            rospy.loginfo("Deletion Completed!")
        else:
            rospy.logwarn("Error during deletion")
        
    except rospy.ServiceException, e:
        rospy.logerr("Service call failed: %s"%e)
        

def call_rename_file(old,new):

    rospy.wait_for_service('rename_file')
    try:
        renameFile = rospy.ServiceProxy('rename_file', RenameFile)
        response = renameFile(old,new)
        if response.isError == 0:
            rospy.loginfo("File renamed correctly!")
        else:
            rospy.logwarn("Error during renaming")
        
    except rospy.ServiceException, e:
        rospy.logerr("Service call failed: %s"%e)


def call_gripper(limb, mode):
    rospy.wait_for_service('gripper')
    try:
        gripper = rospy.ServiceProxy('gripper', Gripper)
        response = gripper(limb,mode)
        if response.isError == 0:
            rospy.loginfo("Open/Close correctly!")
        else:
            rospy.logwarn("Error during opening/closing gripper")
        
    except rospy.ServiceException, e:
        rospy.logerr("Service call failed: %s"%e)


def call_reach_goal(limb, pos_x, pos_y, pos_z, orient_x, orient_y, orient_z, orient_w):
    rospy.wait_for_service('reach_goal')
    try:
        reach_goal = rospy.ServiceProxy('reach_goal', ReachGoal)
        pos = [pos_x, pos_y, pos_z]
        orient = [orient_x, orient_y, orient_z, orient_w]
        
        #posture = mirror_end_effector()
        #posture.position = pos
        #posture.quaternion = orient
        response = reach_goal(limb, pos, orient)
        if response.isError == 0:
            rospy.loginfo("Position Reached !")
        else:
            rospy.logwarn("Cannot reach the position")
        
    except rospy.ServiceException, e:
        rospy.logerr("Service call failed: %s"%e)


if __name__ == "__main__":
    """Acquire paramater specified in the command line and based on them ask for the specified service."""
    type_service = int(sys.argv[1])
    if type_service == 1: #Playback
       filename = sys.argv[2]
       loops = int(sys.argv[3])
       scale_vel = int(sys.argv[4])
       rospy.loginfo("Client: Calling Service Playback")
       call_playback(filename,loops,scale_vel)
       rospy.loginfo("Client: Called!")
    elif type_service == 2: #Record Start
       filename = sys.argv[2]
       record_rate = int(sys.argv[3])
       rospy.loginfo("Client: Calling Service Start Record")
       call_record(filename,record_rate,1)
       rospy.loginfo("Client: Called!")
    elif type_service == 3: #Record Stop
       rospy.loginfo("Client: Calling Service Stop Record")
       call_record("",100,0)
       rospy.loginfo("Client: Called!")
    elif type_service == 4: #List Files
       call_list_files()
    elif type_service == 5: #Remove file
        filename = sys.argv[2]
        call_delete_file(filename)
    elif type_service == 6: #Rename file
        old_filename = sys.argv[2]
        new_filename = sys.argv[3]
        call_rename_file(old_filename,new_filename)
    elif type_service == 7: #Gripper
        call_gripper(sys.argv[2],int(sys.argv[3]))
    elif type_service == 8: #Reach Goal
        call_reach_goal(sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]), float(sys.argv[6]), float(sys.argv[7]), float(sys.argv[8]), float(sys.argv[9]))
	sys.exit(1)
