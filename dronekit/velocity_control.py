#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import print_function
from dronekit import connect, VehicleMode, Command, LocationGlobalRelative, LocationGlobal
from connect import *
from arm_and_take_off import *
import time
from pymavlink import mavutil

def send_ned_velocity(vehicle,velocity_x, velocity_y, velocity_z, duration):
    """
    Move vehicle in direction based on specified velocity vectors.
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

def main():
    vehicle = connect_to_vehicle()

    if(vehicle == None):
        print ("Error, unable to connect to vehicle")

    else:
        # Need to arm and takeoff in order to put a simple_goto
        arm_and_takeoff(vehicle,10)

        # Set up velocity mappings
        # velocity_x > 0 => fly North
        # velocity_x < 0 => fly South
        # velocity_y > 0 => fly East
        # velocity_y < 0 => fly West
        # velocity_z < 0 => ascend
        # velocity_z > 0 => descend
        SOUTH=-2
        UP=-0.5   #NOTE: up is negative!

        #Fly south and up.
        send_ned_velocity(vehicle,SOUTH,0,UP,30)



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

main()