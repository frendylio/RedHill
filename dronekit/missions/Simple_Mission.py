#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import print_function
from dronekit import connect, VehicleMode, Command, LocationGlobalRelative, LocationGlobal
from learning.connect import *
from learning.arm_and_take_off import *
import time
from pymavlink import mavutil

def create_circle_mission(vehicle):
	cmds = vehicle.commands

	print("Clear any existing commands")
	cmds.clear() 

    #Add MAV_CMD_NAV_TAKEOFF command. This is ignored if the vehicle is already in the air.
	# For some reason, if I don't have this, it breaks....
	cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 0, 0, 10))


	print(" Define/add new commands.")
	cmds.add(
		Command(
			0,
			0,
			0,
			mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, 
			mavutil.mavlink.MAV_CMD_NAV_LOITER_TURNS,
			0, 
			0, 
			# Paremeteres
			5, # Number of turns
			0, # Nothing
			100, # RAdius in m
			0, 
			# Altitude
			# Target latitude. If zero, the vehicle will loiter at the current latitude.
			0, 0, 0

		)
	)

	print(" Upload new commands to vehicle")
	cmds.upload()

	return


def main():
    vehicle = connect_to_vehicle()

    if(vehicle == None):
        print ("Error, unable to connect to vehicle")

    else:
		print('Create Mission')
		create_circle_mission(vehicle)

		arm_and_takeoff(vehicle,10)
		
		print("Starting mission")
		# Reset mission set to first (0) waypoint
		vehicle.commands.next=0

		# Set mode to AUTO to start mission
		vehicle.mode = VehicleMode("AUTO")
		while vehicle.mode != 'AUTO':
			print("Waiting for drone to enter AUTO flight mode")
			time.sleep(1)
		print ("Vehicle now in AUTO MODE")


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