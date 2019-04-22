import Comm
from threading import Thread
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def manualTransmit():

    while True:
        print("Send:")
        x = raw_input()
        print("Transmitted: " + x)
        Comm.fnc_CommTransmit(str(x))
    #Con = True
    #while Con:
        #Comm.fnc_CommTransmit(str(x))
        #data = Comm.fnc_CommRecieve()
        #print(data)
        #if data == "ACKNOWLEDGE":
            #Con = False

def switchTransmit():
    
    while True:
        state = GPIO.input(18)
        if state == False:
            print("pressed!")
        time.sleep(0.2)
        
Thread(target = switchTransmit).start()