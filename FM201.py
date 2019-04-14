#
#   Flight Mode 201
#   Set time from GPS
#
print("---FM201 setup---")
import time
import IMUGps
import os
import datetime
import Comm
from FCMS import continueFM
Comm.fnc_CommTransmit("CFM FM201")
print ("---FM201 setup done---")

while continueFM("FM201"):
    #try to get GPS Data
    try:
        #Get GPS Data
        #print("Getting GPS")
        time, lat, dirLat, lon, dirLon = IMUGps.fnc_IMU_Gps()
        #print("Test")
        date = IMUGps.fnc_IMU_Gps_Date()
        splitDate = date.split("-")
        corrDate = "20" + splitDate[2] + "-" + splitDate[1] + "-" + splitDate[0]
        print(corrDate)
        
        if len(time) > 1:
            print(time)
            os.system("sudo date -s '" + corrDate + " " + time + "'")
            print("Changed to: " + str(datetime.datetime.now()))
            Comm.fnc_CommTransmit("MSG FM201_changedTime")
            break
            
        
        
    except:
        pass
        
    
