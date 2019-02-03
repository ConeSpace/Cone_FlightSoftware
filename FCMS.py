#
#   Flight Computer Management System
#
#

print("----FCMS setup----")
from threading import Thread
import time
import Comm
Comm.fnc_CommTransmit("MSG FCMS_setupDone")
print ("----FCMS setup done----")

def changeFM(fm):
    #Currently available: FM010-021 FM 100-101
    if fm == "FM010":
        import FM010
    if fm == "FM011":
        import FM011
    if fm == "FM012":
        import FM012
    if fm == "FM013":
        import FM013
    if fm == "FM014":
        import FM014
    if fm == "FM015":
        import FM015
    if fm == "FM016":
        import FM016
    if fm == "FM017":
        import FM017
    if fm == "FM018":
        import FM019
    if fm == "FM020":
        import FM020
    if fm == "FM021":
        import FM021
        
    if fm == "FM100":
        import FM100
    if fm == "FM101":
        import FM101
    
def checkComm():
    while True:
        try:
            time.sleep(1)
            msg = str(Comm.fnc_CommRecieve())
        
            if msg[0:3] == "CMD":
                #decrypt command
                msgSplit = msg.split(" ")
                if msgSplit[1] == "changeFM":
                    fm = msgSplit[2]
                    changeFM(fm)
        except:
            pass
Thread(target = checkComm).start()