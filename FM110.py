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
                changeFM("FM102")
                
        except:
            pass
        

#Log Sensor Data
def logData():
    while continueFM("FM110"):
        try:
            #Generate messages
            #Generate Temp Press and Altitude Message
            msgAlt = "ALT " + str(altitudeM) + " " + str(pressure) + " " + str(cTemp)
        
            #Generate Accelerometer Message
            msgAcc = "ACC " + str(ACCx) + " " + str(ACCy) + " " + str(ACCz)
        
            #Generate Gyroscope and Heading Message
            msgGry = "GRY " + str(gyroXangle) + " " + str(gyroYangle) + " " + str(gyroZangle) + " " + str(tiltCompensatedHeading)
        
            #Log Data
            f = open("/home/pi/Cone_FlightSoftware/Logs/datalog.txt", "a")
            f.write("\n" + str(msgAlt))
            f.write("\n" + str(msgAcc))
            f.write("\n" + str(msgGry))
            f.write("\n" + str(datetime.datetime.now()))
            time.sleep(0.11)
            
        except:
            pass
        
#Transmit Sensor Data
def transmitData():
    while continueFM("FM110"):
        try:
            #Generate messages
            #Generate Temp Press and Altitude Message
            msgAlt = "ALT " + str(altitudeM) + " " + str(pressure) + " " + str(cTemp)
        
            #Generate Accelerometer Message
            msgAcc = "ACC " + str(ACCx) + " " + str(ACCy) + " " + str(ACCz)
        
            #Generate Gyroscope and Heading Message
            msgGry = "GRY " + str(gyroXangle) + " " + str(gyroYangle) + " " + str(gyroZangle) + " " + str(tiltCompensatedHeading)
        
            #Transmit stuff
            Comm.fnc_CommTransmit("ALM  " + str(altitudeM))
            Comm.fnc_CommTransmit("PRS " + str(pressure))
            Comm.fnc_CommTransmit("CTM " + str(cTemp))
            Comm.fnc_CommTransmit("ACX "+ str(ACCx))
            Comm.fnc_CommTransmit("ACY "+ str(ACCy))
            Comm.fnc_CommTransmit("ACZ "+ str(ACCz))
            Comm.fnc_CommTransmit("GRX "+ str(gyroXangle))
            Comm.fnc_CommTransmit("GRY "+ str(gyroYangle))
            Comm.fnc_CommTransmit("GRZ "+ str(gyroZangle))
            Comm.fnc_CommTransmit("HDN "+ str(tiltCompensatedHeading))
            Comm.fnc_CommTransmit("VSP " + str(vSpeed))
            #print("Transmission complete...")
        
            
        except:
            pass
        
#Get and Transmit GPS Data
def GPS():
    while continueFM("FM110"):
        try:
        #if True: 
            #Get GPS Data
            #print("Getting GPS")
            time, lat, dirLat, lon, dirLon = IMUGps.fnc_IMU_Gps()
            
            #Generate GPS Message
            msgGps = "GPS " + str(time) + " " + str(lat) + " " + str(dirLat) + " " + str(lon)+ " " + str(dirLon)
            #print(msgGps)
            
            Comm.fnc_CommTransmit(msgGps)
            #Log Data
            f = open("/home/pi/Cone_FlightSoftware/Logs/gpslog.txt", "a")
            f.write("\n" + str(msgGps))
            f.write("\n" + str(datetime.datetime.now()))
            delay(1)
            #print("Logged GPS")
            
            
        except:
            pass
                
Thread(target = getData).start()
Thread(target = getVspeed).start()
Thread(target = checkData).start()
Thread(target = transmitData).start()
Thread(target = logData).start()
Thread(target = GPS).start()