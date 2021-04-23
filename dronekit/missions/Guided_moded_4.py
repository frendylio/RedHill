#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Fly the vehicle in a SQUARE path using velocity vectors (the underlying code calls the 
SET_POSITION_TARGET_LOCAL_NED command with the velocity parameters enabled).

The thread sleeps for a time (DURATION) which defines the distance that will be travelled.

The code also sets the yaw (MAV_CMD_CONDITION_YAW) using the `set_yaw()` method in each segment
so that the front of the vehicle points in the direction of travel
"""

from __future__ import print_function
from dronekit import connect, VehicleMode, Command, LocationGlobalRelative, LocationGlobal
from connect import *
from arm_and_take_off import *
from Guided_moded_Helper import *
import time
from pymavlink import mavutil

def send_ned_velocity(vehicle,velocity_x, velocity_y, velocity_z, duration):
    """
    Move vehicle in direction based on specified velocity vectors and
    for the specified duration.

    This uses the SET_POSITION_TARGET_LOCAL_NED command with a type mask enabling only 
    velocity components 
    (http://dev.ardupilot.com/wiki/copter-commands-in-guided-mode/#set_position_target_local_ned).
    
    Note that from AC3.3 the message should be re-sent every second (after about 3 seconds
    with no message the velocity will drop back to zero). In AC3.2.1 and earlier the specified
    velocity persists until it is canceled. The code below should work on either version 
    (sending the message multiple times does not cause problems).
    
    See the above link for information on the type_mask (0=enable, 1=ignore). 
    At time of writing, acceleration and yaw bits are ignored.
    """
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,       # time_boot_ms (not used)
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_FRAME_LOCAL_NED, # frame
        0b0000111111000111, # type_mask (only speeds enabled)
        0, 0, 0, # x, y, z positions (not used)
        velocity_x, velocity_y, velocity_z, # x, y, z velocity in m/s
        0, 0, 0, # x, y, z acceleration (not supported yet, ignored in GCS_Mavlink)
        0, 0)    # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink) 

    # send command to vehicle on 1 Hz cycle
    for x in range(0,duration):
        vehicle.send_mavlink(msg)
        time.sleep(1)

def condition_yaw(vehicle,heading, relative=False):
    """
    Send MAV_CMD_CONDITION_YAW message to point vehicle at a specified heading (in degrees).

    This method sets an absolute heading by default, but you can set the `relative` parameter
    to `True` to set yaw relative to the current yaw heading.

    By default the yaw of the vehicle will follow the direction of travel. After setting 
    the yaw using this function there is no way to return to the default yaw "follow direction 
    of travel" behaviour (https://github.com/diydrones/ardupilot/issues/2427)

    For more information see: 
    http://copter.ardupilot.com/wiki/common-mavlink-mission-command-messages-mav_cmd/#mav_cmd_condition_yaw
    """
    if relative:
        is_relative = 1 #yaw relative to direction of travel
    else:
        is_relative = 0 #yaw is an absolute angle
    # create the CONDITION_YAW command using command_long_encode()
    msg = vehicle.message_factory.command_long_encode(
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_CMD_CONDITION_ROI, #command
        0, #confirmation
        heading,    # param 1, yaw in degrees
        0,          # param 2, yaw speed deg/s
        1,          # param 3, direction -1 ccw, 1 cw
        is_relative, # param 4, relative offset 1, absolute angle 0
        0, 0, 0)    # param 5 ~ 7 not used
    # send command to vehicle
    vehicle.send_mavlink(msg)


def main():
    vehicle = connect_to_vehicle()

    if(vehicle == None):
        print ("Error, unable to connect to vehicle")

    else:
        arm_and_takeoff(vehicle,10)

        #Set up velocity vector to map to each direction.
        # vx > 0 => fly North
        # vx < 0 => fly South
        NORTH = 2
        SOUTH = -2

        # Note for vy:
        # vy > 0 => fly East
        # vy < 0 => fly West
        EAST = 2
        WEST = -2

        # Note for vz: 
        # vz < 0 => ascend
        # vz > 0 => descend
        UP = -0.5
        DOWN = 0.5


        # Square path using velocity
        print("SQUARE path using SET_POSITION_TARGET_LOCAL_NED and velocity parameters")
        DURATION = 5 #Set duration for each segment.

        print("Yaw 180 absolute (South)")
        condition_yaw(vehicle,180)

        print("Velocity South & up")
        send_ned_velocity(vehicle,SOUTH,0,UP,DURATION)


        send_ned_velocity(vehicle,0,0,0,1)


        print("Yaw 270 absolute (West)")
        condition_yaw(vehicle,270)

        print("Velocity West & down")
        send_ned_velocity(vehicle,0,WEST,DOWN,DURATION)
        send_ned_velocity(vehicle,0,0,0,1)

        print("Yaw 0 absolute (North)")
        condition_yaw(vehicle,0)

        print("Velocity North")
        send_ned_velocity(vehicle,NORTH,0,0,DURATION)
        send_ned_velocity(vehicle,0,0,0,1)


        print("Yaw 90 absolute (East)")
        condition_yaw(vehicle,90)

        print("Velocity East")
        send_ned_velocity(vehicle,0,EAST,0,DURATION)
        send_ned_velocity(vehicle,0,0,0,1)

        while True:
            user_input = raw_input('RTL vehicle?: ')
            break

        print('Return to launch')
        vehicle.mode = VehicleMode("RTL")
        while vehicle.mode != 'RTL':
            print("Waiting for drone to enter RTL flight mode")
            time.sleep(1)
        print ("Vehicle now in RTL MODE")

        while True:
            user_input = raw_input('Close vehicle?: ')
            break

    # Do not forget so we can clean/flush vehicle
    # About to exit script
    print ("Closing Vehicle")
    vehicle.close()

    return

if __name__ == "__main__":
    main()