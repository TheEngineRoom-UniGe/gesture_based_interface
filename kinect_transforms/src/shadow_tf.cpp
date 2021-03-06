#include <ros/ros.h>
#include "std_msgs/Float64.h"
#include <tf/transform_broadcaster.h>
#include <cmath>
#include <nav_msgs/Odometry.h>
#include <tf/transform_listener.h>
#include <geometry_msgs/Vector3.h>
#include <tf/transform_datatypes.h>
#include <iostream>
#include <unistd.h>
#include <sys/types.h>
#include <string>
/**
 * @file
 */
 
ros::Publisher pub;  /**< Publisher to /odometry/shadow/<passed frame> */
/**
 * Main function: 
 * - create a TF broadcaster in order to fix the transformation from the frame attached in correspondence of the computed center of mass and the joint frame, passed as parameter (right hand frame, useful for the shadow motion of the Baxter). 
 * - publish odometry of the joint frame, passed as parameter, with respect to the center of mass.
 * @param[in]  frame    string that identifies the joint frame 
 */
int main(int argc, char** argv)
{
    ros::init(argc, argv, "shadow_tf", ros::init_options::AnonymousName);
	ros::NodeHandle n("~");    
	
	static tf::TransformBroadcaster br;
	tf::TransformListener listener;
	
	std::string frame;
	n.param<std::string>("frame", frame, "kinect_right_hand");
	
	std::stringstream pub_path;
	pub_path << "/shadow/" << frame;
	
	ros::NodeHandle nh;  
	// Initilize Publishers for the odometry wrt center of mass
	pub = nh.advertise<nav_msgs::Odometry>(pub_path.str(), 1);
    
	tf::StampedTransform t_com_to_frame;
	
	tf::Transform transform;
	
	ros::Rate r(10);

	while(ros::ok()){
		try{    
			listener.waitForTransform("position_com_frame", frame, ros::Time::now(), ros::Duration(10.0) );
			listener.lookupTransform("position_com_frame", frame, ros::Time(0), t_com_to_frame);
			
			// Update tranformation from position_com_frame (center of mass) to joint frame
			transform = t_com_to_frame;
			
			// Inizialize odometry message (wrt position of the center of mass)
			nav_msgs::Odometry odom_msg;
			odom_msg.header.stamp = ros::Time::now();
			odom_msg.header.frame_id = "position_com_frame";
			odom_msg.child_frame_id = frame;
			tf::poseTFToMsg(transform, odom_msg.pose.pose);
			
			// publish message
			pub.publish(odom_msg);
		}
		catch (tf::TransformException ex){
			
		}
		
		ros::spinOnce();
		r.sleep();
	}

    return 0;
}
