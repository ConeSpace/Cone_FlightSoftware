import Comm

while True:
    try:
        x = input('Send: ')
        Comm.fnc_CommTransmit(str(x))
    except:
        pass