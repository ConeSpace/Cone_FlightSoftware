#
#     TestMode 020
#     Testing multithreading
#

print("Initializing FM020")

from threading import Thread
import time
import datetime
import Comm

def func1():
    while True:
        print("1 Working")
        time.sleep(1)

def func2():
    while True:
        print("2 Working")
        time.sleep(1)
        
Thread(target = func1).start()
Thread(target = func2).start()
        