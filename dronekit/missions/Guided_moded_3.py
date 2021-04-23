#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Fly the vehicle in a square path, using the SET_POSITION_TARGET_LOCAL_NED command 
and specifying a target position (rather than controlling movement using velocity vectors). 
The command is called from goto_position_target_local_ned() (via `goto`).

The position is specified in terms of the NED (North East Down) relative to the Home location.

WARNING: The "D" in NED means "Down". Using a positive D value will drive the vehicle into the ground!

The code sleeps for a time (DURATION) to give the vehicle time to reach each position (rather than 
sending commands based on proximity).

The code also sets the region of interest (MAV_CMD_DO_SET_ROI) via the `set_roi()` method. This points the 
camera gimbal at the the selected location (in this case it aligns the whole vehicle to point at the ROI).
"""	

from __future__ import print_function
from dronekit import connect, VehicleMode, Command, LocationGlobalRelative, LocationGlobal
from connect import *
from arm_and_take_off import *
from Guided_moded_Helper import *
import time
from pymavlink import mavutil

def goto_position_target_local_ned(vehicle,north, east, down):
    """	
    Send SET_POSITION_TARGET_LOCAL_NED command to request the vehicle fly to a specified 
    location in the North, East, Down frame.

    It is important to remember that in this frame, positive altitudes are entered as negative 
    "Down" values. So if down is "10", this will be 10 metres below the home altitude.

    Starting from AC3.3 the method respects the frame setting. Prior to that the frame was
    ignored. For more information see: 
    http://dev.ardupilot.com/wiki/copter-commands-in-guided-mode/#set_position_target_local_ned

    See the above link for information on the type_mask (0=enable, 1=ignore). 
    At time of writing, acceleration and yaw bits are ignored.

    """
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,       # time_boot_ms (not used)
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_FRAME_LOCAL_NED, # frame
        0b0000111111111000, # type_mask (only positions enabled)
        north, east, down, # x, y, z positions (or North, East, Down in the MAV_FRAME_BODY_NED frame
        0, 0, 0, # x, y, z velocity in m/s  (not used)
        0, 0, 0, # x, y, z acceleration (not supported yet, ignored in GCS_Mavlink)
        0, 0)    # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink) 
    # send command to vehicle
    vehicle.send_mavlink(msg)

def set_roi(vehicle,location):
    """
    Send MAV_CMD_DO_SET_ROI message to point camera gimbal at a 
    specified region of interest (LocationGlobal).
    The vehicle may also turn to face the ROI.

    For more information see: 
    http://copter.ardupilot.com/common-mavlink-mission-command-messages-mav_cmd/#mav_cmd_do_set_roi
    """
    # create the MAV_CMD_DO_SET_ROI command
    msg = vehicle.message_factory.command_long_encode(
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_CMD_DO_SET_ROI, #command
        0, #confirmation
        0, 0, 0, 0, #params 1-4
        location.lat,
        location.lon,
        location.alt
        )
    # send command to vehicle
    vehicle.send_mavlink(msg)

def main():
    vehicle = connect_to_vehicle()

    if(vehicle == None):
        print ("Error, unable to connect to vehicle")

    else:
        arm_and_takeoff(vehicle,10)

        print("SQUARE path using SET_POSITION_TARGET_LOCAL_NED and position parameters")
        DURATION = 5 #Set duration for each segment.

        ###############
        # NORTH
        ###############
        print("North 10m, East 0m, 10m altitude for %s seconds" % DURATION)
        goto_position_target_local_ned(vehicle,10,0,-10)
        print("Point ROI at current location (home position)") 
        # NOTE that this has to be called after the goto command as first "move" command of a particular type
        # "resets" ROI/YAW commands
        set_roi(vehicle,vehicle.location.global_relative_frame)
        time.sleep(DURATION)

        ###############
        # EAST
        ###############
        print("North 10m, East 10m, 10m altitude")
        goto_position_target_local_ned(vehicle,10,10,-10)
        time.sleep(DURATION)

        print("Point ROI at current location")
        set_roi(vehicle,vehicle.location.global_relative_frame)

        ###############
        # SOUTH
        ###############
        print("North 0m, East 10m, 10m altitude")
        goto_position_target_local_ned(vehicle,0,10,-10)
        time.sleep(DURATION)

        print("Point ROI at current location")
        set_roi(vehicle,vehicle.location.global_relative_frame)

        ###############
        # WEST
        ###############
        print("North 0m, East 0m, 10m altitude")
        goto_position_target_local_ned(vehicle,0,0,-10)
        time.sleep(DURATION)

        while True:
            user_input = raw_input('RTL vehicle?: ')
            break

        print('Return to launch')
        vehicle.mode = VehicleMode("RTL")
        while vehicle.mode != 'RTL':
            print("Waiting for drone to enter RTLAUTO flight mode")
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