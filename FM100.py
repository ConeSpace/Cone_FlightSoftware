#
#   Flight Mode 100
#   Hibernation
#

print("---FM100 setup---")
from threading import Thread
import time
import IMUTempPress
import IMUGps
import IMUAccComGyro
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

Comm.fnc_CommTransmit("CFM FM100")
print ("---FM100 setup done---")

def checkComm():
    while True:
        time.sleep(1)
        #print("Checking for new Comm msg")
        msg = str(Comm.fnc_CommRecieve())
        
        if msg[0:3] == "CMD":
            #decrypt command
            msgSplit = msg.split(" ")
            if msgSplit[1] == "changeFM":
                fm = msgSplit[2]
                if fm == "FM101":
                    import FM101

checkComm()
    
def checkMovement():
    print("Checking if satellite moved")
    