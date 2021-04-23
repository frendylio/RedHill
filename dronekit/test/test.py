# -*- coding: utf-8 -*-
"""
Spyder Editor
This is a temporary script file.
"""
# Refer to https://mavlink.io/en/mavgen_pytlshon/ for the MAVLink lib
# Refer to https://mavlink.io/en/messages/common.html for MAVLink messages

#import time
import csv
from pymavlink import mavutil
import keyboard
# import matplotlib.pyplot as plt
from read_plot import plot_gps

# Start a connection listening to a UDP port
the_connection = mavutil.mavlink_connection('udpin:192.168.99.2:14550')

# Wait for the first heartbeat 
#   This sets the system and component ID of remote system for the link
the_connection.wait_heartbeat()
print("Heartbeat from system (system %u component %u)" % (the_connection.target_system, the_connection.target_system))

# Once connected, use 'the_connection' to get and send messages

csv_filename = 'drone_status.csv'
with open(csv_filename, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    field = ['time', 'fix_type', 'EKF_status','lat', 'lon', 'alt', 'vel_acc', 'h_acc', 'v_acc', 
             'vel', 'global_lat', 'global_lon', 'global_alt', 'global_vx', 'global_vy', 'global_vz', 
             'HUD_airspeed', 'HUD_groundspeed']
    csvwriter.writerow(field);
    print(field)
    
    lat_list = []
    lon_list = []

    while not keyboard.is_pressed('c'):
        the_connection.wait_heartbeat()
        time_usec = the_connection.messages['GPS_RAW_INT'].time_usec # time since system boot in us
        fix_type = the_connection.messages['GPS_RAW_INT'].fix_type # 1: No fix, 3: 3D fix
        ekf_status = the_connection.messages['EKF_STATUS_REPORT'].flags
        lat = the_connection.messages['GPS_RAW_INT'].lat # degE7
        lon = the_connection.messages['GPS_RAW_INT'].lon
        alt = the_connection.messages['GPS_RAW_INT'].alt # mm
        vel_acc = the_connection.messages['GPS_RAW_INT'].vel_acc # Speed uncertainty in mm
        h_acc = the_connection.messages['GPS_RAW_INT'].h_acc # Position uncertainty in mm
        v_acc = the_connection.messages['GPS_RAW_INT'].v_acc # Altitude uncertainty in mm
        
        # New variables
        vel = the_connection.messages['GPS_RAW_INT'].vel # GPS ground speed in cm/s
        global_lat = the_connection.messages['GLOBAL_POSITION_INT'].lat # Fused global position in degE7
        global_lon = the_connection.messages['GLOBAL_POSITION_INT'].lon
        global_alt = the_connection.messages['GLOBAL_POSITION_INT'].alt
        global_vx = the_connection.messages['GLOBAL_POSITION_INT'].vx # Ground Speed in cm/s
        global_vy = the_connection.messages['GLOBAL_POSITION_INT'].vy
        global_vz = the_connection.messages['GLOBAL_POSITION_INT'].vz
        HUD_airspeed = the_connection.messages['VFR_HUD'].airspeed # m/s
        HUD_groundspeed = the_connection.messages['VFR_HUD'].groundspeed
        # x_vel = the_connection.messages['CONTROL_SYSTEM_STATE'].x_vel # velocity in body frame
        # y_vel = the_connection.messages['CONTROL_SYSTEM_STATE'].y_vel
        # z_vel = the_connection.messages['CONTROL_SYSTEM_STATE'].z_vel
        # x_pos = the_connection.messages['CONTROL_SYSTEM_STATE'].x_pos
        # y_pos = the_connection.messages['CONTROL_SYSTEM_STATE'].y_pos
        # z_pos = the_connection.messages['CONTROL_SYSTEM_STATE'].z_pos
        # airspeed = the_connection.messages['CONTROL_SYSTEM_STATE'].airspeed
        
        time_s = time_usec / 1000000
        lat_deg = lat / 10000000
        lon_deg = lon / 10000000
        alt_deg = alt / 1000
        vel_acc_m = vel_acc / 1000
        h_acc_m = h_acc / 1000
        v_acc_m = v_acc / 1000
        
        # New variables
        vel_m_s = vel / 100
        global_lat_deg = global_lat / 10000000
        global_lon_deg = global_lon / 10000000
        global_alt_deg = global_alt / 1000
        global_vx_m_s = global_vx / 100
        global_vy_m_s = global_vy / 100
        global_vz_m_s = global_vz / 100
        
        lat_list.append(lat_deg)
        lon_list.append(lon_deg)
        
        row = [time_s, fix_type, ekf_status, lat_deg, lon_deg, alt_deg, vel_acc_m, h_acc_m, v_acc_m,
               vel_m_s, global_lat_deg, global_lon_deg, global_alt_deg, global_vx_m_s, global_vy_m_s, global_vz_m_s, 
               HUD_airspeed, HUD_groundspeed]
        csvwriter.writerow(row);
        print(row)
    
        # time.sleep(0.25)
        
plot_gps(csv_filename, 'lowercampus.txt')