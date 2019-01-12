#
#   TestMode 011
#   Comm Receiving and logging Data using new modules
#
#


import time
import Comm
import datetime

int_failed = 0
int_total = 0

while True:
    data = str(Comm.fnc_CommRecieve())
    print("Serial Read: " + data )
    if data == "None":
        print("Error_NoData")
        
        ###LOG ERROR###
        
        #get current time
        timestamp = str(datetime.datetime.now())
        #print("Timestamp", timestamp)
        cmdlog = open("output.txt", "a")
        #print("Opening file")
        int_failed = int_failed + 1
        int_total = int_total + 1
        str_failed = str(int_failed)
        str_total = str(int_total)
        str_cmdlog=(timestamp + " " + str_failed + " Failed, " + str_total + " Total; ")
        cmdlog.write(str_cmdlog)
        #print("Writing to file")
        
        
time.sleep(0.5)