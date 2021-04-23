#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Fly a Square path using the standard Vehicle.simple_goto() method.

The method is called indirectly via a custom "goto" that allows the target position to be
specified as a distance in metres (North/East) from the current position, and which reports
the distance-to-target.
"""	

from __future__ import print_function
from dronekit import connect, VehicleMode, Command, LocationGlobalRelative, LocationGlobal
from connect import *
from arm_and_take_off import *
from Guided_moded_Helper import *
import time
from pymavlink import mavutil

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
    gotoFunction(targetLocation)
    
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
        delay1 = 7 # From the start of command to the start of transmission
        delay2 = 65 # From the start of transmission to the take off
    	path = "/home/redhill/Desktop/RedHill/SDR-Attacks-on-Sensors-master"
        drive = ""
        send_gps(path, drive)
        time.sleep(delay1 + delay2)
    
        arm_and_takeoff(vehicle,4)

        print("Square path using standard Vehicle.simple_goto()")

        print("Set groundspeed to 1m/s.")
        vehicle.groundspeed=1

        # print("Position North 10 m ")
        # goto(vehicle,10, 0,vehicle.simple_goto)

        print("Position East 30 m")
        goto(vehicle,0, 30 ,vehicle.simple_goto)

        # print("Position North -10 m ")
        # goto(vehicle,-10, 0,vehicle.simple_goto)

        # print("Position East -10 m")
        # goto(vehicle,0, -10,vehicle.simple_goto)

        while True:
            user_input = raw_input('LAND vehicle?: ')
            break

        print('Return to launch')
        vehicle.mode = VehicleMode("LAND")
        while vehicle.mode != 'LAND':
            print("Waiting for drone to enter RTL flight mode")
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


if __name__ == "__main__":
    main()
