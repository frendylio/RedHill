from dronekit import connect, VehicleMode

import argparse
"""
=============================
	Connecthing to drone
=============================
"""
print "Start simulator (SITL)"

# Capture the IP Address that the script will connect to:

# parser object	
parser = argparse.ArgumentParser(description='commands')
# Option would be called --connect -> specify IP address and catch and save in variable called args
parser.add_argument('--connect', 
                   help="vehicle connection target string. If not specified, SITL automatically started and used.")
args = parser.parse_args()

# capture the specific value by typing this
connection_string = args.connect
#connection_string = "127.0.0.1:14550" # Static for SITL
sitl = None

# If not IP address no especified
if not connection_string:
	import dronekit_sitl
	sitl = dronekit_sitl.start_default()
	connection_string = sitl.connection_string()

# connect to a vehicle and return a vehicle option
# wait_ready = True means to wait till we connect successfuly to the drone

# Connect to the Vehicle
print('Connecting to vehicle on: %s' % connection_string)
vehicle = connect(connection_string, wait_ready=True)

"""
=============================
	Printing vehicle attributes
=============================
"""

# Get some vehicle attributes (state)
print "Get some vehicle attribute values:"
print " GPS: %s" % vehicle.gps_0
print " Battery: %s" % vehicle.battery
print " Last Heartbeat: %s" % vehicle.last_heartbeat
print " Is Armable?: %s" % vehicle.is_armable
print " System status: %s" % vehicle.system_status.state
print " Mode: %s" % vehicle.mode.name    # settable


"""
=============================
	Closing
=============================
"""

# Close vehicle object before exiting script
print("Close vehicle object")
vehicle.close()

# Shut down simulator if it was started.
if sitl is not None:
    sitl.stop()

print("Completed")
