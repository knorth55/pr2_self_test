#!/usr/bin/python 
# Software License Agreement (BSD License)
# 
# Copyright (c) 2008, Willow Garage, Inc. 
# All rights reserved. 
#                                                                               
# Redistribution and use in source and binary forms, with or without            
# modification, are permitted provided that the following conditions            
# are met:                                                                      
#                                                                               
#  * Redistributions of source code must retain the above copyright             
#    notice, this list of conditions and the following disclaimer.              
#  * Redistributions in binary form must reproduce the above                    
#    copyright notice, this list of conditions and the following                
#    disclaimer in the documentation and/or other materials provided            
#    with the distribution.                                                     
#  * Neither the name of the Willow Garage nor the names of its                 
#    contributors may be used to endorse or promote products derived            
#    from this software without specific prior written permission.              
#                                                                               
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS           
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT             
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS             
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE                
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,           
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,          
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;              
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER              
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT            
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN             
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE               
# POSSIBILITY OF SUCH DAMAGE.                                                   
#                                                                               

##\author Kevin Watts

##\brief Moves base side to side using velocity controller

import roslib
roslib.load_manifest('hot_box_test')

import traceback
import sys, os
from time import sleep

# Loads interface with the robot.

import rospy
from geometry_msgs.msg import Twist,Vector3


def main():
    usage = "base_shuffle.py <dist>;  Moves base in y dir side to side."

    if len(sys.argv) < 2:
        print usage
        sys.exit(1)
    distance = float(sys.argv[1])

    rospy.init_node('shuffle', anonymous=True)
    
    # Publishes velocity every 0.05s, calculates number of publishes
    num_publishes = int(distance * 20 * 2)
    
    cmd_vel = Twist()
    # Change to 0 for a controller with no bkwd bias
    cmd_vel.linear.x = float(-0.01) 
    cmd_vel.linear.y = float(0)
    cmd_vel.linear.z = float(0)
    cmd_vel.angular.x = float(0)
    cmd_vel.angular.y = float(0)
    cmd_vel.angular.z = float(0)

    base_vel = rospy.Publisher('cmd_vel', Twist)

    try:
        while not rospy.is_shutdown():
            # Set velocity 
            cmd_vel.linear.y = float(0.4)
            # Extra iteration adds a negative bias in controller
            for i in range(0, num_publishes - 1): 
                base_vel.publish(cmd_vel)
                if rospy.is_shutdown():
                    break 
                sleep(0.05)
                
            if rospy.is_shutdown():
                break

            cmd_vel.linear.y = float(-0.4)
            for i in range(0, num_publishes):
                if rospy.is_shutdown():
                    break            
                base_vel.publish(cmd_vel)
                sleep(0.05)
    except KeyboardInterrupt:
        pass
    except Exception, e:
        print "Caught exception!", traceback.print_exc()
        rospy.logerr(traceback.format_exc())

    finally:
        # Set velocity = 0
        cmd_vel.linear.y = float(0)
        base_vel.publish(cmd_vel)

        
if __name__ == '__main__':
    main()
