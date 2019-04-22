#
#   Flight Mode 102
#   Post-Flight Hibernation
#

print("---FM101 setup---")
from threading import Thread
import time
import IMUGps
import Comm
from FCMS import changeFM
from FCMS import continueFM
###CONFIGURATION###
print(" ")
print("Config:")
Comm.fnc_CommTransmit("CFM FM102")
print ("---FM102 setup done---")

#Get and Transmit GPS Data
def GPS():
    while continueFM("FM102"):
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
            delay(5)
            #print("Logged GPS")
            
            
        except:
            pass

Thread(target = GPS).start()