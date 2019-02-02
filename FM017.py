#
#   TestMode 017
#   Read data and send it to Comm
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
import IMUTempPress
import IMUGps
import IMUAccComGyro
import datetime
import Comm

###CONFIGURATION###
f = open("config.txt", "r")
for x in f:
    if x[0:3] == "QNH":
        xSplit = x.split(" ")
        QnH = int(xSplit[1])

print(" ")
print("Config:")
print("QNH: " + str(QnH))

print ("-----INITIALIZATION COMPLETE-----")
time.sleep(1)

while True:
    
    #Get Temperature Pressure and Altitude
    print("Getting Pressure, Temp and Altitute")
    cTemp, pressure, altitudeM = IMUTempPress.fnc_IMUTempPress(QnH)
    
    #Get GPS Data
    #print("Getting GPS")
    #time, lat, dirLat, lon, dirLon = IMUGps.fnc_IMU_Gps()
    
    #Get everything else from the IMU
    print("Getting Accelerometer, Gyroscope and Heading")
    ACCx, ACCy, ACCz, gyroXangle, gyroYangle, gyroZangle, tiltCompensatedHeading = IMUAccComGyro.fnc_IMU_AxxComGry()
    
    #Generate Temp Press and Altitude Message
    msgAlt = "ALT " + str(altitudeM) + " " + str(pressure) + " " + str(cTemp)
    print(msgAlt)
    
    #Generate GPS Message
    #msgGps = "GPS " + str(time) + " " + str(lat) + " " + str(dirLat) + " " + str(lon)+ " " + str(dirLon)
    #print(msgGps)
    
    #Generate Accelerometer Message
    msgAcc = "ACC " + str(ACCx) + " " + str(ACCy) + " " + str(ACCz)
    print(msgAcc)
    
    #Generate Gyroscope and Heading Message
    msgGry = "GRY " + str(gyroXangle) + " " + str(gyroYangle) + " " + str(gyroZangle) + " " + str(tiltCompensatedHeading)
    print(msgGry)
    
    #Transmit msgs
    print("Transmitting...")
    Comm.fnc_CommTransmit(msgAlt)
    #Comm.fnc_CommTransmit(msgGps)
    Comm.fnc_CommTransmit(msgAcc)
    Comm.fnc_CommTransmit(msgGry)
    print("Transmission complete...")
    
    #Log Data
    f = open("/home/pi/Desktop/InFlightSoftware/Logs/datalog.txt", "a")
    f.write("\n" + str(msgAlt))
    f.write("\n" + str(msgAcc))
    f.write("\n" + str(msgGry))
    
    
    
    
    
    




