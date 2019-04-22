#
#   Ground View
#   Read data from Comm and Display it
#
#

import os
clear = lambda: os.system('clear')

clear()

groundOUT = """
   _____                   ______ _ _       _     _          _____           _                 
  / ____|                 |  ____| (_)     | |   | |        / ____|         | |                
 | |     ___  _ __   ___  | |__  | |_  __ _| |__ | |_ _____| (___  _   _ ___| |_ ___ _ __ ___  
 | |    / _ \| '_ \ / _ \ |  __| | | |/ _` | '_ \| __|______\___ \| | | / __| __/ _ \  _ ` _ \ 
 | |___| (_) | | | |  __/ | |    | | | (_| | | | | |_       ____) | |_| \__ \ ||  __/ | | | | |
  \_____\___/|_| |_|\___| |_|    |_|_|\__, |_| |_|\__|     |_____/ \__, |___/\__\___|_| |_| |_|
                                       __/ |                        __/ |                      
                                      |___/                        |___/

Setup...
"""
print (groundOUT)

import time
import datetime
import Comm

###CONFIGURATION###

print(" ")
print("Config:")

print ("-----INITIALIZATION COMPLETE-----")
time.sleep(1)

altitudeM = "XXX.X"
pressure = "XXXX.XX"
cTemp = "XX.X"

time = "XXXX"
latDeg = "XX"
latMin = "XX.XXXX"
latDir = "X"
lonDeg = "XX"
lonMin = "XX.XXXX"
lonDir = "X"

accX = "XX.XXX"
accY = "XX.XXX"
accZ = "XX.XXX"

gyroX = "XX.XX"
gyroY = "XX.XX"
gyroZ = "XX.XX"
heading = "XX.X"

apogee = "XXX"

vSpeed = "XX.XX"

msg1 = " "
msg2 = " "
msg3 = " "

rawComm1 = " "
rawComm2 = " "
rawComm3 = " "

flightMode = "XXX"

servo = "XX"

status = "0"

def getData():
    
    global altitudeM
    global pressure
    global cTemp
    
    global time
    global latDeg
    global latMin
    global latDir
    global lonDeg
    global lonMin
    global lonDir
    
    global accX
    global accY
    global accZ
    
    global gyroX
    global gyroY
    global gyroZ
    global heading
    
    global apogee
    
    global vSpeed
    
    global msg1
    global msg2
    global msg3
    
    global rawComm1
    global rawComm2
    global rawComm3
    
    global flightMode
    
    global servo
    
    global status
    
    while True:
    
        try:
            msg = Comm.fnc_CommRecieve()
        
            newComm(msg)
        
            #decode
            if msg[0:3] == "MSG":
                msgSplit = msg.split(" ")
                newMSG(msgSplit[1])
            elif msg[0:3] == "CFM":
                msgSplit = msg.split(" ")
                flightMode = msgSplit[1]
            elif msg[0:3] == "SRV":
                msgSplit = msg.split(" ")
                servo = msgSplit[1]
        
            elif msg[0:3] == "ALM":
                msgSplit = msg.split(" ")
                altitudeM = msgSplit[1]
            elif msg[0:3] == "PRS":
                msgSplit = msg.split(" ")
                pressure = msgSplit[1]
            elif msg[0:3] == "CTM":
                msgSplit = msg.split(" ")
                cTemp = msgSplit[1]
            
            elif msg[0:3] == "ACX":
                msgSplit = msg.split(" ")
                accX = msgSplit[1]
            elif msg[0:3] == "ACY":
                msgSplit = msg.split(" ")
                accY = msgSplit[1]
            elif msg[0:3] == "ACZ":
                msgSplit = msg.split(" ")
                accZ = msgSplit[1]
            
            elif msg[0:3] == "GRX":
                msgSplit = msg.split(" ")
                gyroX = msgSplit[1]
            elif msg[0:3] == "GRY":
                msgSplit = msg.split(" ")
                gyroY = msgSplit[1]
            elif msg[0:3] == "GRZ":
                msgSplit = msg.split(" ")
                gyroZ = msgSplit[1]
            elif msg[0:3] == "HDN":
                msgSplit = msg.split(" ")
                heading = msgSplit[1]
        
            elif msg[0:3] == "APG":
                msgSplit = msg.split(" ")
                apogee = msgSplit[1]
            elif msg[0:3] == "VSP":
                msgSplit = msg.split(" ")
                vSpeed = msgSplit[1]
            
            elif msg[0:3] == "GPS":
                #decrypt GPS data
                msgSplit = msg.split(" ")
                time = msgSplit[1]
                latDeg = msgSplit[2]
                latMin = msgSplit[4]
                latDir = msgSplit[6]
                lonDeg = msgSplit[7]
                lonMin = msgSplit[9]
                lonDir = msgSplit[11]
            
        except:
            pass
    
def newMSG(msg0):
    msg3 = msg2
    msg2 = msg1
    msg1 = msg0
    
def newComm(rawComm0):
    rawComm3 = rawComm2
    rawComm2 = rawComm1
    rawComm1 = rawComm0
    
    #Log Data
    f = open("/home/pi/Cone_FlightSoftware/Logs/commlog.txt", "a")
    f.write("\n" + str(rawComm0))
    f.write("\n" + str(datetime.datetime.now()))
    
def display():
    while True:
        try:
            
            if status == "0":
                dsp = ("""
$$$ $  $       ##  ##  #   # ###
$ $ $ $       #   #  # ##  # #
$ $ $$    ### #   #  # # # # ###
$ $ $ $       #   #  # #  ## #
$$$ $  $       ##  ##  #   # ###

Flight Mode: %s

Servo: %s | Apogee: %s | Time: %s

Heading: %s | Altitude: %s | Vertical Speed: %s
Temp: %s | Pressure: %s

Accelerometer:
    X: %s
    Y: %s
    Z: %s
    
Gyroscope:
    X: %s
    Y: %s
    Z: %s
    
GPS:
    Lat %s DEG %s MIN %s
    Lon %s DEG %s MIN %s
    
Messages:
1: %s
2: %s
3: %s

Communications:
1: %s
2: %s
3: %s

""" %  (flightMode, servo, apogee, time, heading, altitudeM, vSpeed, cTemp,))
            
        except:
            pass