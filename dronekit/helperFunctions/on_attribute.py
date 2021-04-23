#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import print_function
from connect import *
import time

def rangefinder_callback(self,attr_name):
    #attr_name not used here.
    global last_rangefinder_distance
    if last_rangefinder_distance == round(self.rangefinder.distance, 1):
        return
    last_rangefinder_distance = round(self.rangefinder.distance, 1)
    print (" Rangefinder (metres): %s" % last_rangefinder_distance)

# Demonstrate getting callback on any attribute change
def wildcard_callback(self, attr_name, value):
    print (" CALLBACK: (%s): %s" % (attr_name,value) )

def main():
    vehicle = connect_to_vehicle()

    if(vehicle == None):
        print ("Error, unable to connect to vehicle")

    else:


        print ("\nAdd attribute callback detecting any attribute change")
        vehicle.add_attribute_listener('*', wildcard_callback)


        print (" Wait 1s so callback invoked before observer removed")
        time.sleep(1)

        print (" Remove Vehicle attribute observer")
        # Remove observer added with `add_attribute_listener()`
        vehicle.remove_attribute_listener('*', wildcard_callback)


    # Do not forget so we can clean/flush vehicle
    # About to exit script
    print ("Closing Vehicle")
    vehicle.close()

    return

if __name__ == "__main__":
    main()