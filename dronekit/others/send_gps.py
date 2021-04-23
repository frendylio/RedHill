# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import subprocess
import threading
import time
import os

    
def send_gps_thread(cmd):  
    os.system(cmd)
        
def send_gps(path = '', drive = ''):
    cmd = ''
    if path != '':
        cmd += "cd " + path + " && " 
    if drive != '':
        cmd += drive + " && " 
    cmd += "bladeRF-cli -s bladerf2.0.script"
#    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    

    print('Sending GPS bitstream')

    t = threading.Thread(target=send_gps_thread, args=(cmd,))
    t.start()

#    t.join()

#    for line in iter(p.stdout.readline, b''):
#        print(">>> " + line.rstrip())
    

#start_time = time.time()
#send_gps("\"E:\\My Documents\\Virtual Machines\\share_folder\\SDR-Attacks\\SDR-Attacks-on-Sensors\\\"", "e:")
#print("--- %s seconds ---" % (time.time() - start_time))
