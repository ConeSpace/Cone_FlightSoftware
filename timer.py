import time
import datetime
from threading import Thread

def startTimer():
    
    global Timer
    Timer = 0
    print("Starting Timer")
    
    #time.sleep(100)
        
def RunTimer():
    #print("Trying")
    global Timer
    Timer = 0
    print("Starting Timer")
    while True:
        #print("Timer running")
        Timer = Timer + 1
        time.sleep(1)
        #print(Timer)
        
def getTimer():
    return Timer
        
#startTimer()
Thread(target = RunTimer).start()
