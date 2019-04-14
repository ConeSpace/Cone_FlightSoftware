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
                    #GOTO Burn&Climb
                    changeFM("FM104")
                    
                print("")
                #print("Orientation normal")
            else:
                print("Orientation abnormal!!")
                Comm.fnc_CommTransmit("MSG FM103_OrrAbnormal!")
        if ORR == "downwards":
            #print("Checking smth")
            if 45 < gyroYangle < 125:
                #Check Acceleration
                if ACCx > -0.5:
                    print("---LIFTOFF---")
                    #GOTO Burn&Climb
                    FCMS.changeFM("FM104")
                    
                print("")
            else:
                print("Orientation abnormal!!")
                Comm.fnc_CommTransmit("MSG FM103_OrrAbnormal!")
        
        
            
            


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
            #print("Transmitting...")
            #Comm.fnc_CommTransmit(msgAlt)
            #Comm.fnc_CommTransmit(msgGps)
            #Comm.fnc_CommTransmit(msgAcc)
            #Comm.fnc_CommTransmit(msgGry)
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
            #print("Transmission complete...")
        
            #Log Data
            #f = open("/home/pi/Desktop/InFlightSoftware/Logs/datalog.txt", "a")
            #f.write("\n" + str(msgAlt))
            #f.write("\n" + str(msgAcc))
            #f.write("\n" + str(msgGry))
            #f.write("\n" + str(datetime.datetime.now()))
            time.sleep(0.25)
            
            try:
                
                print(" ")
                #Get GPS Data
                #print("Getting GPS")
                #time, lat, dirLat, lon, dirLon = IMUGps.fnc_IMU_Gps()
            
                #Generate GPS Message
                #msgGps = "GPS " + str(time) + " " + str(lat) + " " + str(dirLat) + " " + str(lon)+ " " + str(dirLon)
                #print(msgGps)
            
                #Comm.fnc_CommTransmit(msgGps)
                #Log Data
                #f = open("/home/pi/Cone_FlightSoftware/gpslog.txt", "a")
                #f.write("\n" + str(magGps))
                #f.write("\n" + str(datetime.datetime.now()))
            
            
            except:
                pass
            
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
Thread(target = logData).start()

#Get and Transmit GPS Data
def GPS():
    while continueFM("FM103"):
        try:
            
            #Get GPS Data
            #print("Getting GPS")
            time, lat, dirLat, lon, dirLon = IMUGps.fnc_IMU_Gps()
            
            #Generate GPS Message
            msgGps = "GPS " + str(time) + " " + str(lat) + " " + str(dirLat) + " " + str(lon)+ " " + str(dirLon)
            #print(msgGps)
            
            Comm.fnc_CommTransmit(msgGps)
            #Log Data
            f = open("/home/pi/Cone_FlightSoftware/gpslog.txt", "a")
            f.write("\n" + str(magGps))
            f.write("\n" + str(datetime.datetime.now()))
            delay(1)
            
            
        except:
            pass

Thread(target = GPS).start()