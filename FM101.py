#
#   Flight Mode 101
#   Hibernation
#

print("---FM101 setup---")
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

print(" ")
print("Config:")
print("QNH: " + str(QnH))

Comm.fnc_CommTransmit("CFM FM101")
print ("---FM101 setup done---")

#PRE LAUNCH CHECK AND PROCEDURES
print ("Pre-Launch check and procedures")




def checkMovement():
    print("Checking if satellite moved")
    #print FCMS.continueFM("FM100")
    while continueFM("FM101"):
        print("Checking")
        time.sleep(1)
        
        #See if Altitude is climbing or descending, if not set the current altitude as Ground Level Altitude (GLA)
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
            
            GLA = altitudeM2
            print(GLA)
            
            #Change GLA in the config file
            #Get contents of config.txt
            with open('config.txt', 'r') as file:
                data = file.readlines()
            #Find GLA
            for x in range(len(data)):
                #print("Trying to find GLA at " + str(x))
                dataSplit = data[x].split(" ")
                #print("Gla?" + str(dataSplit[0]))
                if dataSplit[0] == "GLA":
                    #print("FOUND GLA!")
                    data[x] = "GLA " + str(GLA) + " \n"
                    with open('config.txt', 'w') as file:
                        #print(data)
                        file.writelines( data )
                        break
            
    
        elif altitudeM1 < altitudeM2:
            print("Alt Climbing!")
    
        elif altitudeM2 < altitudeM1:
            print("Alt Descending!")
        
        
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
            time.sleep(2)
            ACCx, ACCy, ACCz, gyroXangle, gyroYangle, gyroZangle, tiltCompensatedHeading = IMUAccComGyro.fnc_IMU_AxxComGry()
            heading2 = int(tiltCompensatedHeading)
            ACCx2 = ACCx
            ACCy2 = ACCy
            gryX2 = gyroXangle
            gryY2 = gyroYangle
            gryZ2 = gyroZangle
            #print(heading2)
        
        
            #print("Checking...")
        
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
                Comm.fnc_CommTransmit("MSG FM101_SatelliteMoving")
                return
                break
        
            elif still > 3:
                print("Satellite still!")
                satellite_state = "still"
                Comm.fnc_CommTransmit("MSG FM101_SatelliteStill")
    
        except:
             pass
Thread(target = checkMovement).start()