#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import print_function
from dronekit import connect, VehicleMode, Command, LocationGlobalRelative, LocationGlobal
from connect import *
from arm_and_take_off import *
import time
from pymavlink import mavutil

def main():
    vehicle = connect_to_vehicle()

    if(vehicle == None):
        print ("Error, unable to connect to vehicle")

    else:
        # Need to arm and takeoff in order to put a simple_goto
        arm_and_takeoff(vehicle,10)
        # Set mode to guided - this is optional as the goto method will change the mode if needed.
        vehicle.mode = VehicleMode("GUIDED")

        # # Set the target location in global-relative frame
        a_location = LocationGlobalRelative(-34.364114, 149.166022, 30)
        # vehicle.simple_goto(a_location)

        # Set airspeed using attribute
        vehicle.airspeed = 5 #m/s

        # Set groundspeed using attribute
        vehicle.groundspeed = 7.5 #m/s

        # Set groundspeed using `simple_goto()` parameter
        vehicle.simple_goto(a_location, groundspeed=10)

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