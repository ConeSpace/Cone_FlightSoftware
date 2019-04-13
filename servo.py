import time
import datetime
import Comm
import RPi.GPIO as GPIO

servoPIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50)
#p.start(2.5)


def fnc_moveServo(degrees):
    
    dgr = int(degrees)
    print(dgr)
    
    #check if within 0<=degrees<=180
    if (dgr == 0):
        #print("0")
        p.start(2.5)
        time.sleep(1)
        p.stop()
        Comm.fnc_CommTransmit("SRV 0")
    elif (dgr == 45):
        p.start(5)
        time.sleep(1)
        p.stop()
        Comm.fnc_CommTransmit("SRV 45")
    elif (dgr == 90):
        p.start(7.5)
        time.sleep(1)
        p.stop()
        Comm.fnc_CommTransmit("SRV 90")
    elif (dgr == 135):
        p.start(10)
        time.sleep(1)
        p.stop()
        Comm.fnc_CommTransmit("SRV 135")
    elif (dgr == 180):
        p.start(12.5)
        time.sleep(1)
        p.stop()
        Comm.fnc_CommTransmit("SRV 180")
    else:
        print("ERROR: Wrong servo parameter")
        Comm.fnc_CommTransmit("MSG Wrong servo parameter")
        
    
#fnc_moveServo(45)
#time.sleep(1)
    

