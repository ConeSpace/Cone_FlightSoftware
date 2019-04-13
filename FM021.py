import Comm

while True:
    print("Send:")
    x = raw_input()
    print("Transmitted: " + x)
    Comm.fnc_CommTransmit(str(x))
    Con = True
    while Con:
        Comm.fnc_CommTransmit(str(x))
        data = Comm.fnc_CommRecieve()
        print(data)
        if data == "ACKNOWLEDGE":
            Con = False