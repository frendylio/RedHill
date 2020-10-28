#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Fly the vehicle in a DIAMOND path using velocity vectors (the underlying code calls the 
SET_POSITION_TARGET_GLOBAL_INT command with the velocity parameters enabled).

The thread sleeps for a time (DURATION) which defines the distance that will be travelled.

The code sets the yaw (MAV_CMD_CONDITION_YAW) using the `set_yaw()` method using relative headings
so that the front of the vehicle points in the direction of travel.

At the end of the second segment the code sets a new home location to the current point.
"""

from __future__ import print_function
from dronekit import connect, VehicleMode, Command, LocationGlobalRelative, LocationGlobal
from connect import *
from arm_and_take_off import *
from Guided_moded_Helper import *
import time
from pymavlink import mavutil

def send_global_velocity(vehicle,velocity_x, velocity_y, velocity_z, duration):
    """
    Move vehicle in direction based on specified velocity vectors.

    This uses the SET_POSITION_TARGET_GLOBAL_INT command with type mask enabling only 
    velocity components 
    (http://dev.ardupilot.com/wiki/copter-commands-in-guided-mode/#set_position_target_global_int).
    
    Note that from AC3.3 the message should be re-sent every second (after about 3 seconds
    with no message the velocity will drop back to zero). In AC3.2.1 and earlier the specified
    velocity persists until it is canceled. The code below should work on either version 
    (sending the message multiple times does not cause problems).
    
    See the above link for information on the type_mask (0=enable, 1=ignore). 
    At time of writing, acceleration and yaw bits are ignored.
    """
    msg = vehicle.message_factory.set_position_target_global_int_encode(
        0,       # time_boot_ms (not used)
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT, # frame
        0b0000111111000111, # type_mask (only speeds enabled)
        0, # lat_int - X Position in WGS84 frame in 1e7 * meters
        0, # lon_int - Y Position in WGS84 frame in 1e7 * meters
        0, # alt - Altitude in meters in AMSL altitude(not WGS84 if absolute or relative)
        # altitude above terrain if GLOBAL_TERRAIN_ALT_INT
        velocity_x, # X velocity in NED frame in m/s
        velocity_y, # Y velocity in NED frame in m/s
        velocity_z, # Z velocity in NED frame in m/s
        0, 0, 0, # afx, afy, afz acceleration (not supported yet, ignored in GCS_Mavlink)
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
        mavutil.mavlink.MAV_CMD_CONDITION_YAW, #command
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

        print("DIAMOND path using SET_POSITION_TARGET_GLOBAL_INT and velocity parameters")
        # vx, vy are parallel to North and East (independent of the vehicle orientation)
        DURATION = 5 #Set duration for each segment.

        print("Yaw 225 absolute")
        condition_yaw(vehicle,225)

        print("Velocity South, West and Up")
        send_global_velocity(vehicle,SOUTH,WEST,UP,DURATION)
        send_global_velocity(vehicle,0,0,0,1)


        print("Yaw 90 relative (to previous yaw heading)")
        condition_yaw(vehicle,90,relative=True)

        print("Velocity North, West and Down")
        send_global_velocity(vehicle,NORTH,WEST,DOWN,DURATION)
        send_global_velocity(vehicle,0,0,0,1)

        print("Set new home location to current location")
        vehicle.home_location=vehicle.location.global_frame
        print("Get new home location")
        #This reloads the home location in DroneKit and GCSs
        cmds = vehicle.commands
        cmds.download()
        cmds.wait_ready()
        print(" Home Location: %s" % vehicle.home_location)


        print("Yaw 90 relative (to previous yaw heading)")
        condition_yaw(vehicle,90,relative=True)

        print("Velocity North and East")
        send_global_velocity(vehicle,NORTH,EAST,0,DURATION)
        send_global_velocity(vehicle,0,0,0,1)


        print("Yaw 90 relative (to previous yaw heading)")
        condition_yaw(vehicle,90,relative=True)

        print("Velocity South and East")
        send_global_velocity(vehicle,SOUTH,EAST,0,DURATION)
        send_global_velocity(vehicle,0,0,0,1)


        """
        The example is completing. LAND at current location.
        """

        while True:
            user_input = raw_input('LAND vehicle?: ')
            break

        print("Setting LAND mode...")
        vehicle.mode = VehicleMode("LAND")
        while vehicle.mode != 'LAND':
            print("Waiting for drone to enter LAND flight mode")
            time.sleep(1)
        print ("Vehicle now in LAND MODE")

        while True:
            user_input = raw_input('Close vehicle?: ')
            break

    # Do not forget so we can clean/flush vehicle
    # About to exit script
    print ("Closing Vehicle")
    vehicle.close()

    return

main()