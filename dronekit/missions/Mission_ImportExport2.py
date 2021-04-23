from __future__ import print_function
from dronekit import connect, VehicleMode, Command, LocationGlobalRelative, LocationGlobal
from connect import *
from arm_and_take_off import *
from Mission_Helper import *
from Guided_moded_Helper import *
from Guided_moded_1 import goto
import time
from pymavlink import mavutil

def main():
    vehicle = connect_to_vehicle()

    if(vehicle == None):
        print ("Error, unable to connect to vehicle")

    else:
        arm_and_takeoff(vehicle,10)

        print("Square path using standard Vehicle.simple_goto()")

        print("Set groundspeed to 1m/s.")
        vehicle.groundspeed=5

        print("Position North 10 m ")
        goto(vehicle,10, 0,vehicle.simple_goto)

        print("Position East 10 m")
        goto(vehicle,0, 10,vehicle.simple_goto)

        print("Position North -10 m ")
        goto(vehicle,-10, 0,vehicle.simple_goto)

        print("Position East -10 m")
        goto(vehicle,0, -10,vehicle.simple_goto)

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

    print("Saving mission")
    export_mission_filename = 'resources/test2.txt'
    #Download mission we just uploaded and save to a file
    save_mission(export_mission_filename, vehicle)

    # Do not forget so we can clean/flush vehicle
    # About to exit script
    print ("Closing Vehicle")
    vehicle.close()

    return

if __name__ == "__main__":
    main()