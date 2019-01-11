#!/usr/bin/env python
import serial
import time

ser = serial.Serial(
  port='/dev/serial0',
  baudrate = 9600,
  parity=serial.PARITY_NONE,
  stopbits=serial.STOPBITS_ONE,
  bytesize=serial.EIGHTBITS,
  timeout=1
)

print ("Serial is open: ");

print ("Now Writing");
for i in range(1,100000):
    serOut = ("HelloWorld \n")
    ser.write(serOut.encode())
    time.sleep(1)

print ("Did write, done");


ser.close()

