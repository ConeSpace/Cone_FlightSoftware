#
#   TestMode 019
#   Testing Config reading
#
#
import os
clear = lambda: os.system('clear')

clear()

groundOUT = """
   _____                   ______ _ _       _     _          _____           _                 
  / ____|                 |  ____| (_)     | |   | |        / ____|         | |                
 | |     ___  _ __   ___  | |__  | |_  __ _| |__ | |_ _____| (___  _   _ ___| |_ ___ _ __ ___  
 | |    / _ \| '_ \ / _ \ |  __| | | |/ _` | '_ \| __|______\___ \| | | / __| __/ _ \ '_ ` _ \ 
 | |___| (_) | | | |  __/ | |    | | | (_| | | | | |_       ____) | |_| \__ \ ||  __/ | | | | |
  \_____\___/|_| |_|\___| |_|    |_|_|\__, |_| |_|\__|     |_____/ \__, |___/\__\___|_| |_| |_|
                                       __/ |                        __/ |                      
                                      |___/                        |___/

Setup...
"""
print (groundOUT)

import time
import IMUTempPress
import IMUGps
import IMUAccComGyro
import datetime
import Comm

###CONFIGURATION###
#QnH = 996

f = open("config.txt", "r")
for x in f:
    if x[0:3] == "QNH":
        xSplit = x.split(" ")
        QnH = int(xSplit[1])
    

print(" ")
print("Config:")
print("QNH: " + str(QnH))

print ("-----INITIALIZATION COMPLETE-----")
time.sleep(1)