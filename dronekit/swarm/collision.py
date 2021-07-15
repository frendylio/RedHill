from dronekit import connect, VehicleMode, Command, LocationGlobalRelative, LocationGlobal
import argparse
import socket
import exceptions

import time
from pymavlink import mavutil
import thread
import math
import sys
#===========
# Connect
#===========
def connect_to_vehicle(ipAddress):

    if ipAddress is None: 
        print ("No IP address")
        return None

    # capture the specific value by typing this
    connection_string = ipAddress

    # Connect to the Vehicle
    print('Connecting to vehicle on: %s' % connection_string)
    try:
        vehicle = connect(connection_string, wait_ready=True)
        return vehicle
    # Bad TCP connection
    except socket.error:
        print ('No server exists!')
    # Bad TTY connection
    except exceptions.OSError as e:
        print ('No serial exists!')
    # API Error
    except APIException:
        print ('Timeout!')
    # Other error
    except ValueError:
        print ('Some other error!')

    return None

#===========
# Takeoff
#===========

def arm_and_takeoff(vehicle,aTargetAltitude, ipAddressList):
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
        print (") Altitude: ", vehicle.location.global_relative_frame.alt, ":::", ipAddressList)
        #Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt>= aTargetAltitude*0.95 and vehicle.location.global_relative_frame.alt<= aTargetAltitude*0.95 +2:
            print ("Reached target altitude")
            break
        time.sleep(1)

    print ("Reached target altitude")
    return


# meters
def get_location_metres(lat1, lon1, lat2, lon2, alt1):
    dx = (lon1-lon2)*40000*math.cos((lat1+lat2)*math.pi/360)/360
    dy = (lat1-lat2)*40000/360
        
    return dx*1000, dy*1000, alt1


# Define a function for the thread
def mission( vehicle, ipAddressList, locationGlobal):

    lat = locationGlobal.lat
    lon = locationGlobal.lon
    alt = locationGlobal.alt

    # Check if you connected
    if (vehicle == None):
        print ("Error, unable to connect to vehicle with ip:" + ipAddressList)
    else:
        print("==========" + "Connected to vehicle with ip:" + ipAddressList + "==========")
            # Need to arm and takeoff in order to put a simple_goto
        arm_and_takeoff(vehicle,5, ipAddressList)
        # Set mode to guided - this is optional as the goto method will change the mode if needed.
        vehicle.mode = VehicleMode("GUIDED")

        # # Set the target location in global-relative frame
        a_location = LocationGlobalRelative(21.297751261928763,-157.81677706889198,10)
        # vehicle.simple_goto(a_location)

        # Set airspeed using attribute
        vehicle.airspeed = 1 #m/s

        # Set groundspeed using attribute
        vehicle.groundspeed = 2 #m/s

        # Set groundspeed using `simple_goto()` parameter
        vehicle.simple_goto(a_location, groundspeed=10)      

    return

def collision(listOfVehicles):
    vehicleCurrentLocation = []

    #=======
    # Get vehicle locations
    #=======
    for vehicle in listOfVehicles:
        vehicleCurrentLocation.append(vehicle.location.global_frame)
    
    #======
    # Get Center
    #========
    currentCenter = [0,0,0]
    for i in vehicleCurrentLocation:
        print(i)
        currentCenter[0] = currentCenter[0] + i.lat/2
        currentCenter[1] = currentCenter[1] + i.lon/2
        currentCenter[2] = currentCenter[2] + i.alt/2

    # ========
    # Gets meters
    # ========
    allLats = []
    allLongs = []
    allAlt = []
    allRad = []
    for i in vehicleCurrentLocation:
        lat, long, alt = get_location_metres(i.lat, i.lon,currentCenter[0], currentCenter[1], i.alt)
        allLats.append(lat)
        allLongs.append(long)
        allAlt.append(alt)

        radius = math.sqrt(lat**2 + long**2 + alt**2)

        allRad.append(radius)

    #======
    # get radius
    #======
    temp = 0
    for i in allRad:
        temp = temp + i
    
    print(temp)
    if (abs(temp) <= 21):
        #return True 
        print("Collision")
    else:
        #return False
        print("No collision")




def main():

    print ('Number of arguments:', len(sys.argv), 'arguments.')
    print ('Argument List:', str(sys.argv))

    print("===========Connecting===========")
    ipAddressList = []
    for i in range(len(sys.argv)):
        if i == 0:
            continue
        ipAddressList.append(sys.argv[i])
    
    listOfVehicles = []
    for i in ipAddressList:
        listOfVehicles.append(connect_to_vehicle(i))

    print("Finished connecting")

    print("===========Mission===========")

    for i, vehicle in enumerate(listOfVehicles):
        try:
            thread.start_new_thread( mission, (vehicle, ipAddressList[i], listOfVehicles[(i+1)%2].location.global_frame) )
        except:
            print("Error: unable to start thread")

    print("===========Check for Collision=============")
    didItCollide = False
    try:
        while True:
            collision(listOfVehicles)
            time.sleep(5)
    except KeyboardInterrupt:
        pass    

    print("===========RTL===========")
    while True:
        user_input = raw_input('RTL vehicle?: ')
        break

    for i, vehicle in enumerate(listOfVehicles):
        print('Return to launch')
        vehicle.mode = VehicleMode("RTL")
        while vehicle.mode != 'RTL':
            print("Waiting for drone to enter RTL flight mode")
            time.sleep(1)
        print ("Vehicle now in RTL MODE with ip Address: "  + ipAddressList[i])

    print("===========Closing Vehicles===========")
    while True:
        user_input = raw_input('Close vehicle?: ')
        break
  
    for i, vehicle in enumerate(listOfVehicles):
        print("Closing Vehicle with ip address:" + ipAddressList[i])
        vehicle.close()

    while True:
        user_input = raw_input('Exit: ')
        break

    return 
    
if __name__ == "__main__":
    main()
