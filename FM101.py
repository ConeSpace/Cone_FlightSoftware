#
#   Flight Mode 101
#   Pre-Launch Hibernation
#

print("---FM101 setup---")
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

print(" ")
print("Config:")
print("QNH: " + str(QnH))

GLA_set = False
GPS_available = False
Orientation = "upwards"
Orientation_stable = False
Temperature_stable = False
QnH_set = False
GroundConfirmation = False
PreFlightCheck = False

Comm.fnc_CommTransmit("CFM FM101")
print ("---FM101 setup done---")

#PRE LAUNCH CHECK AND PROCEDURES
print ("Pre-Launch check and procedures")




def checkMovement():
    global GLA_set
    global QnH
    global GPS_available
    global Orientation
    global Orientation_stable
    global Temperature_stable
    global QnH_set
    global GroundConfirmation
    global PreFlightCheck
    
    print("Checking if satellite moved")
    #print FCMS.continueFM("FM100")
    while continueFM("FM101"):
        print("Checking")
        time.sleep(1)
        
        #See if Altitude is climbing or descending, if not set the current altitude as Ground Level Altitude (GLA)
        print("Checking state of flight...")
        cTemp, pressure, altitudeM = IMUTempPress.fnc_IMUTempPress(QnH)
        altitudeM1 = altitudeM
        pressure1 = pressure
        cTemp1 = cTemp
        time.sleep(0.7)
        cTemp, pressure, altitudeM = IMUTempPress.fnc_IMUTempPress(QnH)
        altitudeM2 = altitudeM
        pressure2 = pressure
        cTemp2 = cTemp
        
        #Check if Temperature is stable
        if ((cTemp1 - 1) < cTemp2 < (cTemp1 + 1)):
            Temperature_stable = True
            print("#Temperature Stable")
            Comm.fnc_CommTransmit("MSG PreFlightCheck_Temp_stable")
            
        #Check if QnH is set
        if QnH_set == False:
            try:
                f = open("config.txt", "r")
                for x in f:
                    if x[0:3] == "QNH":
                        xSplit = x.split(" ")
                        QnH = int(xSplit[1])
                f.close()
                QnH_set = True
                print("#QnH Set")
                Comm.fnc_CommTransmit("MSG PreFlightCheck_QnH_Set")
            except:
                print("QnH not yet set")
                Comm.fnc_CommTransmit("MSG WARNING_PreFlightCheck_QnH_NotSet")
                
        #Check if all PreFlight-Checks are completed and get Ground Confirmation
        if GLA_set == True and GPS_available == True and Orientation_stable == True and Temperature_stable == True and QnH_set == True:
            print(" ")
            print("-PRE FLIGHT CHECKLIST-")
            print("#GLA                Set")
            print("#GPS                Available")
            print("#Orientation        Stable")
            print("#Temperature        Stable")
            print("#QnH                Set")
            print("#GroundConfirmation ...")
            
            Comm.fnc_CommTransmit("MSG PreFlightCheck_ConfirmationPending")
            
            while continueFM("FM101"):
                data = Comm.fnc_CommRecieve()
                if str(data) == "MSG ChecklistConfirmed":
                    print("                    received")
                    print("-CHECKLIST COMPLETE-")
                    Comm.fnc_CommTransmit("MSG PreFlightCheck_Completed")
                    #FCMS.changeFM("FM103")
        

        #Check if both measurements are within boundaries (not decending or ascending)
        if ((altitudeM1 - 2) < altitudeM2 < (altitudeM1 + 2)):
            print("Altitude level")
            
            
            
            if GLA_set == False:
            
                GLA = round(altitudeM2)
                GLA = int(GLA)
                print(GLA)
            
                #Change GLA in the config file
                #Get contents of config.txt
                with open('config.txt', 'r') as file:
                    data = file.readlines()
                #Find GLA
                for x in range(len(data)):
                    #print("Trying to find GLA at " + str(x))
                    dataSplit = data[x].split(" ")
                    #print("Gla?" + str(dataSplit[0]))                
                    if dataSplit[0] == "GLA":
                        print("FOUND GLA!")
                        data[x] = "GLA " + str(GLA) + " \n"
                        with open('config.txt', 'w') as file:
                            #print(data)
                            file.writelines( data )
                            GLA_set = True
                            print("#Setting GLA")
                            Comm.fnc_CommTransmit("MSG PreFlightCheck_GLA_set")
                            
                            break
                with open('config.txt', 'r') as file:
                    data = file.readlines()
                for x in range(len(data)):
                    dataSplit = data[x].split(" ")
                    if dataSplit[0] == "APG":
                        data[x] = "APG 0 \n"
                        with open('config.txt', 'w') as file:
                            file.writelines( data )
                            break
            
    
        elif altitudeM1 < altitudeM2:
            print("Alt Climbing!")
    
        elif altitudeM2 < altitudeM1:
            print("Alt Descending!")
        
        
        try:
            #---Reading---
        
            ACCx, ACCy, ACCz, gyroXangle, gyroYangle, gyroZangle, tiltCompensatedHeading = IMUAccComGyro.fnc_IMU_AxxComGry()
            heading1 = int(tiltCompensatedHeading)
            ACCx1 = ACCx
            ACCy1 = ACCy
            gryX1 = gyroXangle
            gryY1 = gyroYangle
            gryZ1 = gyroZangle
            #print(heading1)
            time.sleep(2)
            ACCx, ACCy, ACCz, gyroXangle, gyroYangle, gyroZangle, tiltCompensatedHeading = IMUAccComGyro.fnc_IMU_AxxComGry()
            heading2 = int(tiltCompensatedHeading)
            ACCx2 = ACCx
            ACCy2 = ACCy
            gryX2 = gyroXangle
            gryY2 = gyroYangle
            gryZ2 = gyroZangle
            #print(heading2)
        
        
            #print("Checking...")
        
            #Heading
            if heading1 > (heading2 + 2):
                #print(" heading TURNING!")
                heading_state = "turning"
            elif heading2 > (heading1 + 2):
                #print(" heading TURNING!")
                heading_state = "turning"
            else:
                #print("heading not turning")
                heading_state = "still"
            
        
            #Gyro X
            if gryX1 > (gryX2 + 3):
                gryX_state = "turning"
                #print("Gyro X Turning!")
            elif gryX2 > (gryX1 + 3):
                #print("Gyro X Turning!")
                gryX_state = "turning"
            else:
                #print("Gyro X not turning")
                gryX_state = "still"
            
            #Gyro Y
            if gryY1 > (gryY2 + 3):
                #print("Gyro Y Turning!")
                gryY_state = "turning"
            elif gryY2 > (gryY1 + 3):
                #print("Gyro Y Turning!")
                gryY_state = "turning"
            else:
                #print("Gyro Y not turning")
                gryY_state = "still"
            
            #Gyro Z
            if gryZ1 > (gryZ2 + 0.5):
                #print("Gyro Z Turning!")
                gryZ_state = "turning"
            elif gryZ2 > (gryZ1 + 0.5):
                #print("Gyro Z Turning!")
                gryZ_state = "turning"
            else:
                #print("Gyro Z not turning")
                gryZ_state = "still"
            
            #find out if satellite is moving or not
            turning = 0
            still = 0
            if heading_state == "turning":
                turning = turning + 1
            if gryX_state == "turning":
                turning = turning + 1
            if gryY_state == "turning":
                turning = turning + 1
            if gryZ_state == "turning":
                turning = turning + 1
        
            if heading_state == "still":
                still = still + 1
            if gryX_state == "still":
                still = still + 1
            if gryY_state == "still":
                still = still + 1
            if gryZ_state == "still":
                still = still + 1
                
            #Check pointing direction
            print(gryY2)
            if (-80 > gryY2 > -100):
                print("Pointing Upwards!")
                Orientation = "upwards"
                
                print("Changing orientation")
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
                        
                Orientation_stable = True
                Comm.fnc_CommTransmit("MSG PreFlightCheck_Orientation_Upwards")
                
            elif (80 < gryY2 < 100):
                print("Pointing Downwards!")
                Orientation = "downwards"
              
                print("Changing orientation")
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
                        
                Orientation_stable = True
                Comm.fnc_CommTransmit("MSG PreFlightCheck_Orientation_Downwards")
            
            if turning > 1:
                print("Satellite moving!")
                satellite_state = "moving"
                Comm.fnc_CommTransmit("MSG FM101_SatelliteMoving")
                #return
                #break
        
            elif still > 3:
                print("Satellite still!")
                satellite_state = "still"
                Comm.fnc_CommTransmit("MSG FM101_SatelliteStill")
                
                
    
        except:
             pass
            
def check_GPS():
    print("Checking for GPS")
    global GPS_available
    
    while continueFM("FM101"):
        
        #Get GPS Data
        #print("Getting GPS")
        time, lat, dirLat, lon, dirLon = IMUGps.fnc_IMU_Gps()
        print("#GPS available")
        GPS_available = True
        Comm.fnc_CommTransmit("MSG PreFlightCheck_GPS_available")
        break
    
Thread(target = checkMovement).start()
Thread(target = check_GPS).start()
