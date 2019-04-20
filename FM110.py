#
#   Flight Mode 110
#   Touchdown
#
print("---FM110 setup---")
from threading import Thread
import time
import IMUTempPress
import IMUGps
import IMUAccComGyro
import Comm
import datetime
import servo
from FCMS import changeFM
from FCMS import continueFM
###CONFIGURATION###
try:
    f = open("config.txt", "r")
    for x in f:
        if x[0:3] == "QNH":
            xSplit = x.split(" ")
            QnH = int(xSplit[1])
    f.close()
except:
    QnH = 1013
try:
    f = open("config.txt", "r")
    for x in f:
        if x[0:3] == "ORR":
            xSplit = x.split(" ")
            ORR = str(xSplit[1])
    f.close()
except:
    ORR = "upwards"
try:
    f = open("config.txt", "r")
    for x in f:
        if x[0:3] == "GLA":
            xSplit = x.split(" ")
            GLA = int(xSplit[1])
    f.close()
except:
    GLA = 0
try:
    f = open("config.txt", "r")
    for x in f:
        if x[0:3] == "APG":
            xSplit = x.split(" ")
            #global APG
            APG = int(xSplit[1])
    f.close()
except:
    APG = 0
    


#ORR = "downwards"
print(" ")
print("Config:")
print("QNH: " + str(QnH))
print("Orientation: " + str(ORR))
print("GLA: " + str(GLA))
print("Apogee: " + str(APG))

Comm.fnc_CommTransmit("CFM FM110")
print ("---FM110 setup done---")

#Get Sensor Data
def getData():
    while continueFM("FM110"):
        global cTemp
        global pressure
        global altitudeM
        global ACCx
        global ACCy
        global ACCz
        global gyroXangle
        global gyroYangle
        global gyroZangle
        global tiltCompensatedHeading
        
        try:
            #get Temp Pressure and altitude
            cTemp, pressure, altitudeM = IMUTempPress.fnc_IMUTempPress(QnH)
            #Get everything else from the IMU
            ACCx, ACCy, ACCz, gyroXangle, gyroYangle, gyroZangle, tiltCompensatedHeading = IMUAccComGyro.fnc_IMU_AxxComGry()
            time.sleep(0.1)
        except:
            pass
        
#get Vertical Speed
def getVspeed():
    while continueFM("FM110"):
        
        try:
            global vSpeed
        
            #set altitude1
            altitude1 = altitudeM
            time.sleep(1)
            vSpeed = altitudeM - altitude1
            #print(round(vSpeed, 1))
        except:
            pass
        
def checkData():
    while continueFM("FM110"):
    
        try:
            
            #check for Movement
            gyroYangle1 = gyroYangle
            time.sleep(1)
            if (gyroYangle1 - 5) < gyroYangle < (gyroYangle + 5):
                print("Not moving")