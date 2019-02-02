#
#   Flight State Check
#   Quickly Check Sensors and find out where we are
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
try:
    f = open("config.txt", "r")
    for x in f:
        if x[0:3] == "QNH":
            xSplit = x.split(" ")
            QnH = int(xSplit[1])
except:
    QnH = 1013

print(" ")
print("Config:")
print("QNH: " + str(QnH))

print ("-----INITIALIZATION COMPLETE-----")

while True:
    try:
        #---Reading---
        
        ACCx, ACCy, ACCz, gyroXangle, gyroYangle, gyroZangle, tiltCompensatedHeading = IMUAccComGyro.fnc_IMU_AxxComGry()
        heading1 = int(tiltCompensatedHeading)
        ACCx1 = ACCx
        ACCy1 = ACCy
        gryX1 = gyroXangle
        gryY1 = gyroYangle
        gryZ1 = gyroZangle
        #print(heading1)
        time.sleep(0.7)
        ACCx, ACCy, ACCz, gyroXangle, gyroYangle, gyroZangle, tiltCompensatedHeading = IMUAccComGyro.fnc_IMU_AxxComGry()
        heading2 = int(tiltCompensatedHeading)
        ACCx2 = ACCx
        ACCy2 = ACCy
        gryX2 = gyroXangle
        gryY2 = gyroYangle
        gryZ2 = gyroZangle
        #print(heading2)
        
        
        print("Checking...")
        
        #Heading
        if heading1 > (heading2 + 2):
            #print(" heading TURNING!")
            heading_state = "turning"
        elif heading2 > (heading1 + 2):
            #print(" heading TURNING!")
            heading_state = "turning"
        else:
            #print("heading not turning")
            heading_state = "still"
            
        
        #Gyro X
        if gryX1 > (gryX2 + 3):
            gryX_state = "turning"
            #print("Gyro X Turning!")
        elif gryX2 > (gryX1 + 3):
            #print("Gyro X Turning!")
            gryX_state = "turning"
        else:
            #print("Gyro X not turning")
            gryX_state = "still"
            
        #Gyro Y
        if gryY1 > (gryY2 + 3):
            #print("Gyro Y Turning!")
            gryY_state = "turning"
        elif gryY2 > (gryY1 + 3):
            #print("Gyro Y Turning!")
            gryY_state = "turning"
        else:
            #print("Gyro Y not turning")
            gryY_state = "still"
            
        #Gyro Z
        if gryZ1 > (gryZ2 + 0.5):
            #print("Gyro Z Turning!")
            gryZ_state = "turning"
        elif gryZ2 > (gryZ1 + 0.5):
            #print("Gyro Z Turning!")
            gryZ_state = "turning"
        else:
            #print("Gyro Z not turning")
            gryZ_state = "still"
            
        #find out if satellite is moving or not
        turning = 0
        still = 0
        if heading_state == "turning":
            turning = turning + 1
        if gryX_state == "turning":
            turning = turning + 1
        if gryY_state == "turning":
            turning = turning + 1
        if gryZ_state == "turning":
            turning = turning + 1
        
        if heading_state == "still":
            still = still + 1
        if gryX_state == "still":
            still = still + 1
        if gryY_state == "still":
            still = still + 1
        if gryZ_state == "still":
            still = still + 1
            
        if turning > 1:
            print("Satellite moving!")
            satellite_state = "moving"
            break
        
        elif still > 3:
            print("Satellite still!")
            satellite_state = "still"
            break
    
    except:
         pass

if satellite_state == "still":
    cTemp, pressure, altitudeM = IMUTempPress.fnc_IMUTempPress(QnH)
    altitudeM1 = altitudeM
    pressure1 = pressure
    time.sleep(0.7)
    cTemp, pressure, altitudeM = IMUTempPress.fnc_IMUTempPress(QnH)
    altitudeM2 = altitudeM
    pressure2 = pressure
    
    #Check if both measurements are within boundaries (not decending or ascending)
    if ((altitudeM1 - 2) < altitudeM2 < (altitudeM1 + 2)):
        print("Altitude level")
        import FM100
    else:
        print("Checking state of flight...")
        #Check if both measurements are within boundaries (not decending or ascending)
        if ((altitudeM1 - 2) < altitudeM2 < (altitudeM1 + 2)):
            print("Altitude level")
    
        elif altitudeM1 < altitudeM2:
            print("Alt Climbing!")
    
        elif altitudeM2 < altitudeM1:
            print("Alt Descending!")
        
        if ((pressure1 - 2) < pressure2 < (pressure1 + 2)):
            print("Pressure level")
    
        elif pressure1 < pressure2:
            print("Pressure Climbing!")
    
        elif pressure2 > pressure1:
            print("pressure Descending!")
        
else:
    print("Checking state of flight...")
    cTemp, pressure, altitudeM = IMUTempPress.fnc_IMUTempPress(QnH)
    altitudeM1 = altitudeM
    pressure1 = pressure
    time.sleep(0.7)
    cTemp, pressure, altitudeM = IMUTempPress.fnc_IMUTempPress(QnH)
    altitudeM2 = altitudeM
    pressure2 = pressure
    
    #Check if both measurements are within boundaries (not decending or ascending)
    if ((altitudeM1 - 2) < altitudeM2 < (altitudeM1 + 2)):
        print("Altitude level")
    
    elif altitudeM1 < altitudeM2:
        print("Alt Climbing!")
    
    elif altitudeM2 < altitudeM1:
        print("Alt Descending!")
        
    if ((pressure1 - 2) < pressure2 < (pressure1 + 2)):
        print("Pressure level")
    
    elif pressure1 < pressure2:
        print("Pressure Climbing!")
    
    elif pressure2 > pressure1:
        print("pressure Descending!")
        
    
    