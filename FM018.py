#
#   TestMode 018
#   Read data from Comm and Display it
#
#

import os
clear = lambda: os.system('clear')

clear()

groundOUT = """
   _____                   ______ _ _       _     _          _____           _                 
  / ____|                 |  ____| (_)     | |   | |        / ____|         | |                
 | |     ___  _ __   ___  | |__  | |_  __ _| |__ | |_ _____| (___  _   _ ___| |_ ___ _ __ ___  
 | |    / _ \| '_ \ / _ \ |  __| | | |/ _` | '_ \| __|______\___ \| | | / __| __/ _ \ '_ ` _ \ 
 | |___| (_) | | | |  __/ | |    | | | (_| | | | | |_       ____) | |_| \__ \ ||  __/ | | | | |
  \_____\___/|_| |_|\___| |_|    |_|_|\__, |_| |_|\__|     |_____/ \__, |___/\__\___|_| |_| |_|
                                       __/ |                        __/ |                      
                                      |___/                        |___/

Setup...
"""
print (groundOUT)

import time
import datetime
import Comm

###CONFIGURATION###

print(" ")
print("Config:")

print ("-----INITIALIZATION COMPLETE-----")
time.sleep(1)

altitudeM = "XXX.X"
pressure = "XXXX.XX"
cTemp = "XX.X"
status = "X"

while True:
    try:
        
        #recieve from Comm
        msg = Comm.fnc_CommRecieve()
        
        if msg[0:3] == "ALT":
            #decrypt altitude, temp and pressure data
            msgSplit = msg.split(" ")
            altitudeM = msgSplit[1]
            pressure = msgSplit[2]
            cTemp = msg[3]
            status = "OK"
        
        fnc_display(altitudeM, pressure, cTemp, status)
        
    except:
        pass
    
def fnc_display(altitudeM, pressure, cTemp, status):
    
    #Check status
    if status == "OK":
        
        #Display
        dsp = ("""
$$$ $  $
$ $ $ $
$ $ $$
$ $ $ $
$$$ $  $

    Heading 090 # Altitude %s m # Flight-Mode 001
    
    Gyroscope # GPS
    X 000       Lat 04 23.12344
    Y 000
    Z 000
    
    Temperature %s C # Barometer %s HpA
        """ %  (altitudeM, cTemp, pressure))
        print (dsp)
    