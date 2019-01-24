#
#   TestMode 016
#   Read Pressure and Temp
#
#
import time
import IMUTempPress
import Comm

#setup reference pressure and altitude
cTemp, pressure, altitudeM = IMUTempPress.fnc_IMUTempPress(1007)
refAlt = altitudeM


print ("Setup Done...")

while True:
    cTemp, pressure, altitudeM = IMUTempPress.fnc_IMUTempPress(1007)
    actAlt = int(altitudeM)
    print ("Tmp: " + str(cTemp))
    print ("Alt: " + str(pressure))
    print("Altitude: " + str(actAlt))
    Comm.fnc_CommTransmit("ALT " + str(pressure))
    time.sleep(0.5)
    