#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import print_function
from dronekit import VehicleMode
from connect import *
import time
from send_gps import *

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
    delay1 = 7 # From the start of command to the start of transmission
    delay2 = 65 # From the start of transmission to the take off
    path = "/home/redhill/Desktop/RedHill/SDR-Attacks-on-Sensors-master"

#    send_gps(path, drive)
#    time.sleep(delay1 + delay2)
    
    vehicle = connect_to_vehicle()

    if(vehicle == None):
        print ("Error, unable to connect to vehicle")

    else:    
        send_gps(path)
        time.sleep(delay1 + delay2)
        arm_and_takeoff(vehicle, 4)

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
