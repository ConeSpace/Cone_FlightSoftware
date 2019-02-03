import Comm

while True:
    print("Send:")
    x = raw_input()
    print("Transmitted: " + x)
    Comm.fnc_CommTransmit(str(x))