from dronekit import connect, APIException
import argparse
import socket
import exceptions
#mavproxy.py --master=udp:0.0.0.0:14550 --map --console
def connect_to_vehicle():
    parser = argparse.ArgumentParser(description='commands')
    # Option would be called --connect -> specify IP address and catch and save in variable called args
    parser.add_argument('--connect', 
                    help="vehicle connection target string. If not specified, SITL automatically started and used.")
    args = parser.parse_args()

    # capture the specific value by typing this
    connection_string = args.connect

    connection_string = "0.0.0.0:14550"

    #connection_string = "127.0.0.1:14550" # Static for SITL
    sitl = None

    # If not IP address no especified
    if not connection_string:
        import dronekit_sitl
        sitl = dronekit_sitl.start_default()
        connection_string = sitl.connection_string()


    # Connect to the Vehicle
    print('Connecting to vehicle on: %s' % connection_string)
    try:
        vehicle = connect(connection_string, wait_ready=True)
        return vehicle
    # Bad TCP connection
    except socket.error:
        print 'No server exists!'
    # Bad TTY connection
    except exceptions.OSError as e:
        print 'No serial exists!'
    # API Error
    except APIException:
        print 'Timeout!'
    # Other error
    except ValueError:
        print 'Some other error!'

    return None

def main():
    vehicle = connect_to_vehicle()

    if(vehicle == None):
        print "Error, unable to connect to vehicle"
        return

    else:
        # Get some vehicle attributes (state)
        print "Get some vehicle attribute values:"
        print " GPS: %s" % vehicle.gps_0
        print " Battery: %s" % vehicle.battery
        print " Last Heartbeat: %s" % vehicle.last_heartbeat
        print " Is Armable?: %s" % vehicle.is_armable
        print " System status: %s" % vehicle.system_status.state
        print " Mode: %s" % vehicle.mode.name    # settable

    # Do not forget so we can clean/flush vehicle
    # About to exit script
    print "Closing Vehicle"
    vehicle.close()

    return 
    
if __name__ == "__main__":
    main()