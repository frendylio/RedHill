#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import print_function
from connect import *
import time

#Callback to print the location in global frames. 'value' is the updated value
def location_callback(self, attr_name, value):
    print ("Location (Global Latitude): ", value.lat)

def main():
    vehicle = connect_to_vehicle()

    if(vehicle == None):
        print ("Error, unable to connect to vehicle")

    else:
        # Add a callback `location_callback` for the `global_frame` attribute.
        vehicle.add_attribute_listener('location.global_frame', location_callback)

        # Wait 2s so callback can be notified before the observer is removed
        # if we don't have this, it will run too fast and not print anything
        time.sleep(2)

        # Remove observer - specifying the attribute and previously registered callback function
        vehicle.remove_message_listener('location.global_frame', location_callback)

        # vehicle.add_attribute_listener('location.global_frame', location_callback)
        # time.sleep(2)
        # vehicle.location.add_attribute_listener('global_frame', location_callback)
        # time.sleep(2)
    # Do not forget so we can clean/flush vehicle
    # About to exit script
    print ("Closing Vehicle")
    vehicle.close()

    return

main()