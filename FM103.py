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
        
        
            
            


#Transmit Sensor Data
def transmitData():
    while continueFM("FM103"):
        try:
            #Generate messages
            #Generate Temp Press and Altitude Message
            msgAlt = "ALT " + str(altitudeM) + " " + str(pressure) + " " + str(cTemp)
        
            #Generate Accelerometer Message
            msgAcc = "ACC " + str(ACCx) + " " + str(ACCy) + " " + str(ACCz)
        
            #Generate Gyroscope and Heading Message
            msgGry = "GRY " + str(gyroXangle) + " " + str(gyroYangle) + " " + str(gyroZangle) + " " + str(tiltCompensatedHeading)
        
            #Transmit Messages
            #Transmit msgs
            print("Transmitting...")
            Comm.fnc_CommTransmit(msgAlt)
            #Comm.fnc_CommTransmit(msgGps)
            Comm.fnc_CommTransmit(msgAcc)
            Comm.fnc_CommTransmit(msgGry)
            print("Transmission complete...")
        
            #Log Data
            #f = open("/home/pi/Desktop/InFlightSoftware/Logs/datalog.txt", "a")
            #f.write("\n" + str(msgAlt))
            #f.write("\n" + str(msgAcc))
            #f.write("\n" + str(msgGry))
            #f.write("\n" + str(datetime.datetime.now()))
        except:
            pass
        
#Log Sensor Data
def logData():
    while continueFM("FM103"):
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
            delay(0.1)
        except:
            pass

Thread(target = getData).start()
Thread(target = checkData).start()
Thread(target = transmitData).start()
#Thread(target = logData).start()

#Get and Transmit GPS Data