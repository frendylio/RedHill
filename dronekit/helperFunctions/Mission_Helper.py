from __future__ import print_function
from dronekit import connect, VehicleMode, Command, LocationGlobalRelative, LocationGlobal
from connect import *
from arm_and_take_off import *
import time
from pymavlink import mavutil

def download_cmd(vehicle):
    cmds = vehicle.commands
    cmds.download()
    cmds.wait_ready

    return cmds

def clear_cmd(vehicle):
    cmds = vehicle.commands
    cmds.clear()
    cmds.upload()

    return cmds

def create_cmds(cmds):
    cmd1=Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 0, 0, 10)
    cmd2=Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, 10, 10, 10)
    cmds.add(cmd1)
    cmds.add(cmd2)
    cmds.upload() # Send commands

    return cmds

def modify_cmds(cmds):
    # Save the vehicle commands to a list
    missionlist=[]
    for cmd in cmds:
        missionlist.append(cmd)    

    # Modify the mission as needed. For example, here we change the
    # first waypoint into a MAV_CMD_NAV_TAKEOFF command.
    missionlist[0].command=mavutil.mavlink.MAV_CMD_NAV_TAKEOFF

    # Clear the current mission (command is sent when we call upload())
    cmds.clear()

    #Write the modified mission and flush to the vehicle
    for cmd in missionlist:
        cmds.add(cmd)
    cmds.upload()

def upload_mission(aFileName, vehicle, import_mission_filename):
        """
        Upload a mission from a file.
        """
        #Read mission from file
        missionlist = readmission(aFileName,vehicle)

        print ("\nUpload mission from a file: %s" % import_mission_filename)
        #Clear existing mission from vehicle
        print (' Clear mission')
        cmds = vehicle.commands
        cmds.clear()
        #Add new mission to vehicle
        for command in missionlist:
            cmds.add(command)
        print (' Upload mission')
        vehicle.commands.upload()

def readmission(aFileName, vehicle):
    """
    Load a mission from a file into a list.

    This function is used by upload_mission().
    """
    print ("Reading mission from file: %s\n" % aFileName)
    cmds = vehicle.commands
    missionlist=[]
    with open(aFileName) as f:
        for i, line in enumerate(f):
            if i==0:
                if not line.startswith('QGC WPL 110'):
                    raise Exception('File is not supported WP version')
            else:
                linearray=line.split('\t')
                ln_index=int(linearray[0])
                ln_currentwp=int(linearray[1])
                ln_frame=int(linearray[2])
                ln_command=int(linearray[3])
                ln_param1=float(linearray[4])
                ln_param2=float(linearray[5])
                ln_param3=float(linearray[6])
                ln_param4=float(linearray[7])
                ln_param5=float(linearray[8])
                ln_param6=float(linearray[9])
                ln_param7=float(linearray[10])
                ln_autocontinue=int(linearray[11].strip())
                cmd = Command( 0, 0, 0, ln_frame, ln_command, ln_currentwp, ln_autocontinue, ln_param1, ln_param2, ln_param3, ln_param4, ln_param5, ln_param6, ln_param7)
                missionlist.append(cmd)
    return missionlist

def save_mission(aFileName, vehicle):
    """
    Save a mission in the Waypoint file format (http://qgroundcontrol.org/mavlink/waypoint_protocol#waypoint_file_format).
    """
    missionlist = download_mission(vehicle)
    output='QGC WPL 110\n'
    for cmd in missionlist:
        commandline="%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (cmd.seq,cmd.current,cmd.frame,cmd.command,cmd.param1,cmd.param2,cmd.param3,cmd.param4,cmd.x,cmd.y,cmd.z,cmd.autocontinue)
        output+=commandline
    with open(aFileName, 'w') as file_:
        file_.write(output)

def download_mission(vehicle):
    """
    Downloads the current mission and returns it in a list.
    It is used in save_mission() to get the file information to save.
    """
    missionlist=[]
    cmds = vehicle.commands
    cmds.download()
    cmds.wait_ready()
    for cmd in cmds:
        missionlist.append(cmd)
    return missionlist

def distance_to_current_waypoint():
    """
    Gets distance in metres to the current waypoint.
    It returns None for the first waypoint (Home location).
    """
    nextwaypoint=vehicle.commands.next
    if nextwaypoint ==0:
        return None
    missionitem=vehicle.commands[nextwaypoint-1] #commands are zero indexed
    lat=missionitem.x
    lon=missionitem.y
    alt=missionitem.z
    targetWaypointLocation=LocationGlobalRelative(lat,lon,alt)
    distancetopoint = get_distance_metres(vehicle.location.global_frame, targetWaypointLocation)
    return distancetopoint

def printfile(aFileName):
    """
    Print a mission file to demonstrate "round trip"
    """
    print("\nMission file: %s" % aFileName)
    with open(aFileName) as f:
        for line in f:
            print(' %s' % line.strip())   

