#
#   TestMode 012
#   Comm Transmitting Data using new modules
#
#


import time
import Comm
import datetime


while True:
    print("Transmitting...")
    Comm.fnc_CommTransmit("Hello World")
    time.sleep(1)
