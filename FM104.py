#
#   Flight Mode 104
#   Burn&Climb
#

print("---FM104 setup---")
from threading import Thread
import time
import IMUTempPress
import IMUGps
import IMUAccComGyro
import Comm
import datetime
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

Comm.fnc_CommTransmit("CFM FM104")
print ("---FM104 setup done---")

#Get Sensor Data
def getData():
    while continueFM("FM104"):
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
    while continueFM("FM104"):
        global vSpeed
        
        #set altitude1
        altitude1 = altitudeM
        time.sleep(1)
        vSpeed = altitudeM - altitude1
        print(round(vSpeed, 1))
        
#Check Data
def checkData():
    global Burn
    global Apogee
    Burn = True
    Apogee = 0
    while continueFM("FM104"):
        time.sleep(0.1)
        try:
            
            
            
            #print("Burn " + str(Burn))
            
        
            #check Orientation
            if ORR == "upwards":
            
                #check if Burning
                if ACCx > 1.5:
                    #Burn ongoing
                    Burn = True
                else:
                    #Burn ended
                    if Burn == True:
                        print("---BURN ENDED---")
                    Burn = False
                    Comm.fnc_CommTransmit("MSG FM104_BurnEnded")
        
            if ORR == "downwards":
            
                #check if Burning
                if ACCx > -0.5:
                    #Burn ongoing
                    Burn = True
                else:
                    #Burn ended
                    if Burn == True:
                        print("---BURN ENDED---")
                    Burn = False
                    Comm.fnc_CommTransmit("MSG FM104_BurnEnded")
                    
            #check for Apogee
            if altitudeM > Apogee:
                #new Apogee!
                Apogee = round(altitudeM)
                with open('config.txt', 'r') as file:
                    data = file.readlines()
                for x in range(len(data)):
                    dataSplit = data[x].split(" ")
                    if dataSplit[0] == "APG":
                        data[x] = "APG " + str(Apogee) + " \n"
                        with open('config.txt', 'w') as file:
                            file.writelines( data )
                            break
                
            Comm.fnc_CommTransmit("APG " + str(Apogee))
            
            #check for deployment
            if ORR == "upwards":
                #print("Checking smth")
                if -45 > gyroYangle > -125:
                print("")
                
                else:
                    print("Deployment detected!!")
                    Comm.fnc_CommTransmit("MSG FM104_Deployment")
            if ORR == "downwards":
                #print("Checking smth")
                if 45 < gyroYangle < 125:            
                    print("")
                    
                else:
                    print("Deployment detected!!")
                    Comm.fnc_CommTransmit("MSG FM104_Deployment")
            
        except:
            pass

Thread(target = getData).start()
Thread(target = checkData).start()
Thread(target = getVspeed).start()