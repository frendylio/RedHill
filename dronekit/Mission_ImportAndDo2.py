from __future__ import print_function
from dronekit import connect, VehicleMode, Command, LocationGlobalRelative, LocationGlobal
from connect import *
from arm_and_take_off import *
from Mission_Helper import *
import time
from pymavlink import mavutil

# QGC WPL <VERSION>
#  <INDEX> <CURRENT WP> <COORD FRAME> <COMMAND> <PARAM1> <PARAM2> <PARAM3> <PARAM4> <PARAM5/X/LATITUDE> <PARAM6/Y/LONGITUDE> <PARAM7/Z/ALTITUDE> <AUTOCONTINUE>

def main():
    vehicle = connect_to_vehicle()

    if(vehicle == None):
        print ("Error, unable to connect to vehicle")

    else:
        # Arm vehicle first, this is so wecanensure hoome_Location is set
        # (To save WayPoint files)
        # while not vehicle.is_armable:
        #     print(" Waiting for vehicle to initialise...")
        #     time.sleep(1)
        arm_and_takeoff(vehicle, 10)

        # Imporitingor exporting
        import_mission_filename = 'resources/test2.txt'

        #Upload mission from file
        upload_mission(import_mission_filename,vehicle,import_mission_filename)

        # Modify 
        # Save the vehicle commands to a list
        missionlist=[]
        cmds = vehicle.commands
        for cmd in cmds:
            missionlist.append(cmd)    
        for cmd in cmds:
            missionlist.append(cmd)
            
        # Clear the current mission (command is sent when we call upload())
        cmds.clear()

        #Write the modified mission and flush to the vehicle
        for cmd in missionlist:
            cmds.add(cmd)
        cmds.upload()


        # missionlist = vehicle.commands
        # for x in missionlist:
        #     print(x)

        print("Setting AUTO mode...")
        vehicle.mode = VehicleMode("AUTO")
        while vehicle.mode != 'AUTO':
            print("Waiting for drone to enter AUTO flight mode")
            time.sleep(1)
        print ("Vehicle now in AUTO MODE")        

        while True:
            user_input = raw_input('Close vehicle?: ')
            break

    # Do not forget so we can clean/flush vehicle
    # About to exit script
    print ("Closing Vehicle")
    vehicle.close()

    return

main()