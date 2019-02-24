#
#   Flight Computer Management System
#
#

print("----FCMS setup----")
from threading import Thread
import time
import Comm
import sys
print(sys.version_info)
Comm.fnc_CommTransmit("MSG FCMS_setupDone")

fm_states = {
    "FM010": "disabled",
    "FM011": "disabled",
    "FM012": "disabled",
    "FM013": "disabled",
    "FM014": "disabled",
    "FM015": "disabled",
    "FM016": "disabled",
    "FM017": "disabled",
    "FM018": "disabled",
    "FM019": "disabled",
    "FM020": "disabled",
    "FM021": "disabled",
    "FM100": "disabled",
    "FM101": "disabled",
    "FM102": "disabled",
    "FM103": "disabled",
    }
    
activeFM = "FM000"

print ("----FCMS setup done----")

def changeFM(fm):
    #Currently available: FM010-021 FM 100-103
    
    global fm_states
    global activeFM
    fm_states = {
    "FM010": "disabled",
    "FM011": "disabled",
    "FM012": "disabled",
    "FM013": "disabled",
    "FM014": "disabled",
    "FM015": "disabled",
    "FM016": "disabled",
    "FM017": "disabled",
    "FM018": "disabled",
    "FM019": "disabled",
    "FM020": "disabled",
    "FM021": "disabled",
    "FM100": "disabled",
    "FM101": "disabled",
    "FM102": "disabled",
    "FM103": "disabled",
    }
    
    if fm == "FM010":
        fm_states = {x:"disabled" for x in fm_states}
        fm_states["FM010"] = "active"
        import FM010
    if fm == "FM011":
        fm_states = {x:"disabled" for x in fm_states}
        fm_states["FM011"] = "active"
        import FM011
    if fm == "FM012":
        fm_states = {x:"disabled" for x in fm_states}
        fm_states["FM012"] = "active"
        import FM012
    if fm == "FM013":
        fm_states = {x:"disabled" for x in fm_states}
        fm_states["FM013"] = "active"
        import FM013
    if fm == "FM014":
        fm_states = {x:"disabled" for x in fm_states}
        fm_states["FM014"] = "active"
        import FM014
    if fm == "FM015":
        fm_states = {x:"disabled" for x in fm_states}
        fm_states["FM015"] = "active"
        import FM015
    if fm == "FM016":
        fm_states = {x:"disabled" for x in fm_states}
        fm_states["FM016"] = "active"
        import FM016
    if fm == "FM017":
        fm_states = {x:"disabled" for x in fm_states}
        fm_states["FM017"] = "active"
        import FM017
    if fm == "FM018":
        fm_states = {x:"disabled" for x in fm_states}
        fm_states["FM018"] = "active"
        import FM019
    if fm == "FM020":
        fm_states = {x:"disabled" for x in fm_states}
        fm_states["FM019"] = "active"
        import FM020
    if fm == "FM021":
        fm_states = {x:"disabled" for x in fm_states}
        fm_states["FM021"] = "active"
        import FM021
        
    if fm == "FM100":
        fm_states = {x:"disabled" for x in fm_states}
        fm_states["FM100"] = "active"
        #print("shitty 100 stuff")
        activeFM = "FM100"
        import FM100
    if fm == "FM101":
        fm_states = {x:"disabled" for x in fm_states}
        fm_states["FM101"] = "active"
        activeFM = "FM101"
        import FM101
    if fm == "FM102":
        fm_states = {x:"disabled" for x in fm_states}
        fm_states["FM102"] = "active"
        activeFM = "FM102"
        import FM102
    if fm == "FM103":
        fm_states = {x:"disabled" for x in fm_states}
        fm_states["FM103"] = "active"
        activeFM = "FM103"
        import FM103
    return
        
def continueFM(fm):
   #Currently available: FM010-021 FM 100-103
    global activeFM
    #print (activeFM)
    curr_state = fm_states[fm]
    #print(curr_state)
    if curr_state == "active":
        return True
    elif curr_state == "disabled":
        return False
        
    
    
    
def checkComm():
    while True:
        try:
            time.sleep(1)
            msg = str(Comm.fnc_CommRecieve())
        
            #print(msg)
            if msg[0:3] == "CMD":
                #print("receivec CMD")
                #decrypt command
                msgSplit = msg.split(" ")
                if msgSplit[1] == "changeFM":
                    fm = msgSplit[2]
                    print("Changing FM")
                    Comm.fnc_CommTransmit("MSG FCMS_ChangingFM")
                    changeFM(fm)
                    pass
                if msgSplit[1] == "changeQnH":
                    QnH = msgSplit[2]
                    print("Changing QnH")
                    Comm.fnc_CommTransmit("MSG FCMS_ChangingQnH")
                    #Get contents of config.txt
                    with open('config.txt', 'r') as file:
                        data = file.readlines()
                    #Find QnH
                    for x in range((len(data)-1)):
                        dataSplit = data[x].split(" ")
                        if dataSplit[0] == "QNH":
                            data[x] = "QNH " + str(QnH) + " \n"
                            with open('config.txt', 'w') as file:
                                file.writelines( data )
                                break
                    pass
                if msgSplit[1] == "changeOrientation":
                    Orientation = msgSplit[2]
                    print("Changing orientation")
                    Comm.fnc_CommTransmit("MSG FCMS_ChangingOrientation")
                    #Get contents of config.txt
                    with open('config.txt', 'r') as file:
                        data = file.readlines()
                    #Find ORR
                    for x in range((len(data))):
                        dataSplit = data[x].split(" ")
                        if dataSplit[0] == "ORR":
                            data[x] = "ORR " + str(Orientation) + " \n"
                            with open('config.txt', 'w') as file:
                                file.writelines( data )
                                break
                    pass
                        
        except:
            pass
Thread(target = checkComm).start()