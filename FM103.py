#
#   Flight Mode 103
#   Pre-Launch
#

print("---FM103 setup---")
from threading import Thread
import time
import IMUTempPress
import IMUGps
import IMUAccComGyro
import Comm
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

#ORR = "downwards"
print(" ")
print("Config:")
print("QNH: " + str(QnH))
print("Orientation: " + str(ORR))
print("GLA: " + str(GLA))

Comm.fnc_CommTransmit("CFM FM103")
print ("---FM103 setup done---")

#Get Sensor Data
def getData():
    while continueFM("FM103"):
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
        

Thread(target = getData).start()

#Evaluate Sensor Data
def checkData():
    while continueFM("FM103"):
        #Checking orientation
        #print(gyroYangle)
        time.sleep(0.2)
        if ORR == "upwards":
            #print("Checking smth")
            if -45 > gyroYangle > -125:
                #Check Acceleration
                if ACCx > 1.5:
                    print("---LIFTOFF---")
                print("")
                #print("Orientation normal")
            else:
                print("Orientation abnormal!!")
        if ORR == "downwards":
            #print("Checking smth")
            if 45 < gyroYangle < 125:
                #Check Acceleration
                if ACCx > -0.5:
                    print("---LIFTOFF---")
                print("")
            else:
                print("Orientation abnormal!!")
        
        
            
            
Thread(target = checkData).start()

#Transmit Sensor Data

#Get and Transmit GPS Data