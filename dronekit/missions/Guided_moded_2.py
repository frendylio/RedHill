#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Fly a Square path using the SET_POSITION_TARGET_GLOBAL_INT command and specifying
a target position (rather than controlling movement using velocity vectors). The command is
called from goto_position_target_global_int() (via `goto`).

The goto_position_target_global_int method is called indirectly from a custom "goto" that allows 
the target position to be specified as a distance in metres (North/East) from the current position, 
and which reports the distance-to-target.

The code also sets the speed (MAV_CMD_DO_CHANGE_SPEED). In AC3.2.1 Copter will accelerate to this speed 
near the centre of its journey and then decelerate as it reaches the target. 
In AC3.3 the speed changes immediately.
"""	

from __future__ import print_function
from dronekit import connect, VehicleMode, Command, LocationGlobalRelative, LocationGlobal
from connect import *
from arm_and_take_off import *
from Guided_moded_Helper import *
import time
from pymavlink import mavutil

def goto_position_target_global_int(vehicle,aLocation):
    """
    Send SET_POSITION_TARGET_GLOBAL_INT command to request the vehicle fly to a specified LocationGlobal.

    For more information see: https://pixhawk.ethz.ch/mavlink/#SET_POSITION_TARGET_GLOBAL_INT

    See the above link for information on the type_mask (0=enable, 1=ignore). 
    At time of writing, acceleration and yaw bits are ignored.
    """
    msg = vehicle.message_factory.set_position_target_global_int_encode(
        0,       # time_boot_ms (not used)
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT, # frame
        0b0000111111111000, # type_mask (only speeds enabled)
        aLocation.lat*1e7, # lat_int - X Position in WGS84 frame in 1e7 * meters
        aLocation.lon*1e7, # lon_int - Y Position in WGS84 frame in 1e7 * meters
        aLocation.alt, # alt - Altitude in meters in AMSL altitude, not WGS84 if absolute or relative, above terrain if GLOBAL_TERRAIN_ALT_INT
        0, # X velocity in NED frame in m/s
        0, # Y velocity in NED frame in m/s
        0, # Z velocity in NED frame in m/s
        0, 0, 0, # afx, afy, afz acceleration (not supported yet, ignored in GCS_Mavlink)
        0, 0)    # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink) 
    # send command to vehicle
    vehicle.send_mavlink(msg)

def goto(vehicle, dNorth, dEast, gotoFunction):
    """
    Moves the vehicle to a position dNorth metres North and dEast metres East of the current position.

    The method takes a function pointer argument with a single `dronekit.lib.LocationGlobal` parameter for 
    the target position. This allows it to be called with different position-setting commands. 
    By default it uses the standard method: dronekit.lib.Vehicle.simple_goto().

    The method reports the distance to target every two seconds.
    """
    
    currentLocation = vehicle.location.global_relative_frame
    targetLocation = get_location_metres(currentLocation, dNorth, dEast)
    targetDistance = get_distance_metres(currentLocation, targetLocation)
    gotoFunction(vehicle,targetLocation)
    
    #print "DEBUG: targetLocation: %s" % targetLocation
    #print "DEBUG: targetLocation: %s" % targetDistance

    while vehicle.mode.name=="GUIDED": #Stop action if we are no longer in guided mode.
        #print "DEBUG: mode: %s" % vehicle.mode.name
        remainingDistance=get_distance_metres(vehicle.location.global_relative_frame, targetLocation)
        print("Distance to target: ", remainingDistance)
        # Update the distance .... 
        if remainingDistance<=targetDistance*0.1: #Just below target, in case of undershoot.
            print("Reached target")
            break
        time.sleep(2)

def main():
    vehicle = connect_to_vehicle()

    if(vehicle == None):
        print ("Error, unable to connect to vehicle")

    else:
        arm_and_takeoff(vehicle,10)

        print("Quare path using standard SET_POSITION_TARGET_GLOBAL_INT message and with varying speed.")
        print("Position South 100 West 130")

        print("Set groundspeed to 1m/s.")
        vehicle.groundspeed = 1
        goto(vehicle,10, 0, goto_position_target_global_int)

        print("Set groundspeed to 2m/s (max).")
        vehicle.groundspeed = 2
        goto(vehicle,0, 10, goto_position_target_global_int)

        print("Set airspeed to 3m/s (max).")
        vehicle.airspeed = 3
        goto(vehicle,-10, 0, goto_position_target_global_int)

        print("Set airspeed to 1m/s (max).")
        vehicle.airspeed = 1
        goto(vehicle,0, -10, goto_position_target_global_int)

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