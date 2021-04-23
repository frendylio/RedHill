#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import print_function
from dronekit import VehicleMode
from connect import *
import time

def get_homeLocation(vehicle):
    # Get Vehicle Home location - will be `None` until first set by autopilot
    while not vehicle.home_location:
        cmds = vehicle.commands
        cmds.download()
        cmds.wait_ready()
        if not vehicle.home_location:
            print (" Waiting for home location ...")

    # We have a home location.
    print ("\n Home location: %s" % vehicle.home_location)

    return

def main():
    vehicle = connect_to_vehicle()

    if(vehicle == None):
        print ("Error, unable to connect to vehicle")

    else:
        get_homeLocation(vehicle)

    # Do not forget so we can clean/flush vehicle
    # About to exit script
    print ("Closing Vehicle")
    vehicle.close()

    return

if __name__ == "__main__":
    main()