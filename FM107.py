#
#   Flight Mode 107
#   Low Descend
#
print("---FM107 setup---")
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

Comm.fnc_CommTransmit("CFM FM107")
print ("---FM107 setup done---")

#Deploy main Chute
servo.fnc_moveServo(45)
time.sleep(1)

#Get Sensor Data
def getData():
    while continueFM("FM107"):
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
    while continueFM("FM107"):
        
        try:
            global vSpeed
        
            #set altitude1
            altitude1 = altitudeM
            time.sleep(1)
            vSpeed = altitudeM - altitude1
            #print(round(vSpeed, 1))
        except:
            pass
        
#checkData
def checkData():
    global INF
    INF = 1
    
    while continueFM("FM107"):
        try:
            
            #check for Main Chute opening
            if -3 > vSpeed > -10:
                print("Main Chute deployed!")
                Comm.fnc_CommTransmit("MSG FM107_MainChuteDeployed")
                
            #check for 30m above ground
            if (GLA + 30) > altitudeM:
                if INF == 1:
                    with open('config.txt', 'r') as file:
                        data = file.readlines()
                    for x in range(len(data)):
                        dataSplit = data[x].split(" ")
                        if dataSplit[0] == "INF":
                            data[x] = "INF 2 \n"
                            with open('config.txt', 'w') as file:
                                file.writelines( data )
                                break
                    print("Bracing for Impact")
                    Comm.fnc_CommTransmit("MSG FM107_ChangingINF2")
                    INF = 2
                    
            #check for impact
            if ACCx > 1:
                print("IMPACT")
                #change to FM110
                changeFM("FM110")
                
            if ACCx < -1:
                print("IMPACT")
                #change to FM110
                changeFM("FM110")    
                    
            
        except:
            pass
        
#Transmit Sensor Data
def transmitData():
    while continueFM("FM107"):
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
        
#Log Sensor Data
def logData():
    while continueFM("FM107"):
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
    
#Get and Transmit GPS Data
def GPS():
    while continueFM("FM107"):
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