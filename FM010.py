import IMUAccComGyro
import time

while True:
    ACCx, ACCy, ACCz, gyroXangle, gyroYangle, gyroZangle, tiltCompensatedHeading = IMUAccComGyro.fnc_IMU_AxxComGry()
    
    print ("AccZ = " + str(ACCx))
    time.sleep(0.1)
