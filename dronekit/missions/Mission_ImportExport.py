from __future__ import print_function
from dronekit import connect, VehicleMode, Command, LocationGlobalRelative, LocationGlobal
from connect import *
from arm_and_take_off import *
from Mission_Helper import *
import time
from pymavlink import mavutil

def main():
    vehicle = connect_to_vehicle()

    if(vehicle == None):
        print ("Error, unable to connect to vehicle")

    else:
        # Arm vehicle first, this is so wecanensure hoome_Location is set
        # (To save WayPoint files)
        while not vehicle.is_armable:
            print(" Waiting for vehicle to initialise...")
            time.sleep(1)

        # Imporitingor exporting
        import_mission_filename = 'resources/mpmission.txt'
        export_mission_filename = 'resources/exportedmission.txt'

        #Upload mission from file
        upload_mission(import_mission_filename,vehicle,import_mission_filename)

        #Download mission we just uploaded and save to a file
        save_mission(export_mission_filename, vehicle)

        while True:
            user_input = raw_input('Close vehicle?: ')
            break

    # Do not forget so we can clean/flush vehicle
    # About to exit script
    print ("Closing Vehicle")
    vehicle.close()

    print("\nShow original and uploaded/downloaded files:")
    #Print original file (for demo purposes only)
    printfile(import_mission_filename)
    #Print exported file (for demo purposes only)
    printfile(export_mission_filename)

    return

if __name__ == "__main__":
    main()