#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import print_function
from dronekit import VehicleMode
from connect import *
import time

def arm_and_takeoff(vehicle,aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print ("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print (" Waiting for vehicle to initialise...")
        time.sleep(1)
    print ("Vehicle is now armable")

    print ("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode    = VehicleMode("GUIDED")

    while vehicle.mode != 'GUIDED':
		print("Waiting for drone to enter GUIDED flight mode")
		time.sleep(1)
    print ("Vehicle now in GUIDED MODE")

    vehicle.armed   = True

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        if vehicle.mode.name == "INITIALISING":
            print ("Waiting for vehicle to initialise")
            time.sleep(1)
        while vehicle.gps_0.fix_type < 2:
            print ("Waiting for GPS...:", vehicle.gps_0.fix_type)
            time.sleep(1)

    print ("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command
    #  after Vehicle.simple_takeoff will execute immediately).
    while True:
        print (") Altitude: ", vehicle.location.global_relative_frame.alt)
        #Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt>= aTargetAltitude*0.95 and vehicle.location.global_relative_frame.alt<= aTargetAltitude*0.95 +2:
            print ("Reached target altitude")
            break
        time.sleep(1)

    print ("Reached target altitude")
    return

def main():
    vehicle = connect_to_vehicle()

    if(vehicle == None):
        print ("Error, unable to connect to vehicle")

    else:
        arm_and_takeoff(vehicle, 1)

    # Do not forget so we can clean/flush vehicle
    # About to exit script
    print ("Closing Vehicle")
    vehicle.close()

    return

main()