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
 | |    / _ \| '_ \ / _ \ |  __| | | |/ _` | '_ \| __|______\___ \| | | / __| __/ _ \  _ ` _ \ 
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

time = "XXXX"
latDeg = "XX"
latMin = "XX.XXXX"
latDir = "X"
lonDeg = "XX"
lonMin = "XX.XXXX"
lonDir = "X"

accX = "XX.XXX"
accY = "XX.XXX"
accZ = "XX.XXX"

gyroX = "XX.XX"
gyroY = "XX.XX"
gyroZ = "XX.XX"
heading = "XX.X"

status = "X"

while True:
    try:
        
        #recieve from Comm
        msg = Comm.fnc_CommRecieve()
        print(msg)
        
        if msg[0:3] == "ALT":
            #decrypt altitude, temp and pressure data
            #print("ALT detected")
            msgSplit = msg.split(" ")
            #print(msgSplit)
            altitudeM = msgSplit[1]
            pressure = msgSplit[2]
            cTemp = msgSplit[3]
            #print(msgSplit[3])
            status = "OK"
            
        elif msg[0:3] == "GPS":
            #decrypt GPS data
            msgSplit = msg.split(" ")
            time = msgSplit[1]
            latDeg = msgSplit[2]
            latMin = msgSplit[4]
            latDir = msgSplit[6]
            lonDeg = msgSplit[7]
            lonMin = msgSplit[9]
            lonDir = msgSplit[11]
        elif msg[0:3] == "GRY":
            #decrypt Gyroscope and Heading data
            msgSplit = msg.split(" ")
            gyroX = msgSplit[1]
            gyroY = msgSplit[2]
            gyroZ = msgSplit[3]
            heading = msgSplit[4]
        elif msg[0:3] == "ACC":
            #decrypt Accelerometer data
            msgSplit = msg.split(" ")
            accX = msgSplit[1]
            accY = msgSplit[2]
            accZ = msgSplit[3]
        else:
            status = "XX"
        
        ###GENERATING OUTPUT###
            
        #Check Status
        if status == "OK":
            #Display
            dsp = ("""
$$$ $  $
$ $ $ $
$ $ $$
$ $ $ $
$$$ $  $

    Heading %s # Altitude %s m # Flight-Mode 001
    
    Gyroscope # GPS
    X %s        Lat %s DEG %s MIN %s
    Y %s        Lon %s DEG %s MIN %s
    Z %s
    
    Accelerometer
    X %s
    Y %s
    Z %s
    
    Temperature %s C # Barometer %s HpA
            """ %  (heading, altitudeM, gyroX, latDeg, latMin, latDir, gyroY, lonDeg, lonMin, lonDir, gyroZ, accX, accY, accZ, cTemp, pressure))
            clear()
            print (dsp)
            
            #Write data to file
            #f = open("datalog.txt", "a")
    
            
            
            
        
    except:
        pass



'''
def fnc_display(altitudeM, pressure, cTemp, status):
    
    print("Generating output...")
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
        print
        '''