from dronekit import connect, VehicleMode, LocationGlobalRelative,APIException
import time
import csv
import socket
import exceptions
import subprocess
import math
import os
import argparse
from pymavlink import mavutil

def connectMyCopter():
	parser = argparse.ArgumentParser(description='commands')
	parser.add_argument('--connect')
	args = parser.parse_args()
	
	connection_string = "127.0.0.1:14550" # Static for SITL

	if not connection_string:
		import dronekit_sitl
		sitl = dronekit_sitl.start_default()
		connection_string = sitl.connection_string()
	
	vehicle = connect(connection_string,wait_ready=True)
	
	return vehicle

def arm_and_takeoff(aTargetAltitude):
	print ("Basic pre-arm checks")
	while not vehicle.is_armable:
		print ("Waiting for vehicle to initialize...")
		time.sleep(1)

	print ("Arming motors")
	vehicle.mode = VehicleMode("GUIDED")
	vehicle.armed = True
	
	while not vehicle.armed:
		print ("Waiting for arming...")
		time.sleep(1)

	print ("Taking Off!")
	vehicle.simple_takeoff(aTargetAltitude)

	while True:
		print ("Altitude: ", vehicle.location.global_relative_frame.alt)
		if vehicle.location.global_relative_frame.alt >= aTargetAltitude*0.95:
			print ("Reached target altitude")
			break
		time.sleep(1)

### Manual MavLink Message Creation ###
def send_local_ned_velocity(vx, vy, vz):
	msg = vehicle.message_factory.set_position_target_local_ned_encode(
		0, # time_boot_ms
		0, # target_system
		0, #target_component
		mavutil.mavlink.MAV_FRAME_BODY_OFFSET_NED, # Frame of reference
		0b0000111111000111, # type_mask
		0, 0, 0, # Position (x,y,z)
		vx, vy, vz, # Velocities (x,y,z)
		0, 0, 0, # Accelerations (N/A)
		0, #yaw in radians
		0) #yaw_rate in rad/s
	vehicle.send_mavlink(msg)
	vehicle.flush()

def send_global_ned_velocity(vx, vy, vz):
	msg = vehicle.message_factory.set_position_target_local_ned_encode(
		0,
		0, 0,
		mavutil.mavlink.MAV_FRAME_LOCAL_NED,
		0b0000111111000111,
		0, 0, 0,
		vx, vy, vz,
		0, 0, 0,
		0, 0)
	vehicle.send_mavlink(msg)
	vehicle.flush()
	
### Only creates subprocess if the file is located within the ArduPilot directory ###
sim = subprocess.Popen(["sim_vehicle.py --map --location UH -v ArduCopter"], shell=True)
time.sleep(5)

vehicle = connectMyCopter()
arm_and_takeoff(30)

point1 = LocationGlobalRelative(21.29860114, -157.81681053, 30)
point2 = LocationGlobalRelative(21.29860114, -157.81612828, 30)
point3 = LocationGlobalRelative(21.29670604, -157.81612828, 30)
point4 = LocationGlobalRelative(21.29670604, -157.81544603, 30)
point5 = LocationGlobalRelative(21.29860114, -157.81544603, 30)
point6 = LocationGlobalRelative(21.29860114, -157.81476378, 30)
point7 = LocationGlobalRelative(21.29670604, -157.81476378, 30)


print ("Flying to point1")
vehicle.simple_goto(point1, groundspeed = 10)

time.sleep(35)

print ("Flying to point2")
vehicle.simple_goto(point2, groundspeed = 10)

time.sleep(15)

print ("Flying to point3")
vehicle.simple_goto(point3, groundspeed = 10)

time.sleep(35)

print ("Flying to point4")
vehicle.simple_goto(point4, groundspeed = 10)

time.sleep(15)

print ("Flying to point5")
vehicle.simple_goto(point5, groundspeed = 10)

time.sleep(35)

print ("Flying to point6")
vehicle.simple_goto(point6, groundspeed = 10)

time.sleep(15)

print ("Flying to point7")
vehicle.simple_goto(point7, groundspeed = 10)

time.sleep(35)

vehicle.mode = VehicleMode("RTL")

print("Landing...")

vehicle.close()
sim.kill()

#Non-elegant way to kill program
os.system('pkill mavproxy')
os.system('pkill mavproxy')        
os.system('pkill mavproxy')  
os.system('pkill mavproxy') 
os.system('pkill arducopter')
os.system('pkill xterm')
