import serial


#---SETUP---
ser = serial.Serial(
    port='/dev/serial0' ,
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=0.5
    )
print ("GPS serial is open...");

print ("--- GPS SETUP DONE---");


def fnc_IMU_Gps():
    times = 0;
    #Use: time, lat, dirLat, lon, dirLon = fnc_IMU_Gps()
    while True:
        try:
            data = ser.readline()
            #print(data)
            
            time, lat, dirLat, lon, dirLon = parseGPS(data)
            
            #actLat = str(lat[0:2] + " deg " + lat[2:4] + "M " + str(int(lat[5:]) * 60) + "S")
            #actLon = str(lon[0:2] + " deg " + lon[2:4] + "M " + str(int(lon[5:]) * 60) + "S")
            return time, lat, dirLat, lon, dirLon
                
            
            if times > 100:
                return
                break
        except:
            #print ("Failed")
            pass
    


def parseGPS(data):
#    print "raw:", data #prints raw data
    if data[0:6] == "$GNRMC":
        sdata = data.split(",")
        if sdata[2] == 'V':
            print "no satellite data available GNRMC"
            return
        #print "---Parsing GNRMC---",
        time = sdata[1][0:2] + ":" + sdata[1][2:4] + ":" + sdata[1][4:6]
        lat = decode(sdata[3]) #latitude
        dirLat = sdata[4]      #latitude direction N/S
        lon = decode(sdata[5]) #longitute
        dirLon = sdata[6]      #longitude direction E/W
        speed = "N/A"#sdata[7]       #Speed in knots
        trCourse = "N/A"#sdata[8]    #True course
        date = "N/A"#sdata[9][0:2] + "/" + sdata[9][2:4] + "/" + sdata[9][4:6]#date
        
        #print("Houston...")
        
        #actLat = lat[0:2] + " deg " + lat[2:4] + "M " + str(int(lat[5:]) * 60) + "S"
        #actLon = lon[0:2] + " deg " + lon[2:4] + "M " + str(int(lon[5:]) * 60) + "S"
        
        #print(lat + " " + lon)
        
        return time, lat, dirLat, lon, dirLon
 
        #print "time : %s, latitude : %s(%s), longitude : %s(%s), speed : %s, True Course : %s, Date : %s" %  (time,lat,dirLat,lon,dirLon,speed,trCourse,date)
    elif data[0:6] == "$GPRMC":
        sdata = data.split(",")
        if sdata[2] == 'V':
            print "no satellite data available GPRMC"
            return
        #print "---Parsing GPRMC---",
        time = sdata[1][0:2] + ":" + sdata[1][2:4] + ":" + sdata[1][4:6]
        lat = decode(sdata[3]) #latitude
        dirLat = sdata[4]      #latitude direction N/S
        lon = decode(sdata[5]) #longitute
        dirLon = sdata[6]      #longitude direction E/W
        speed = "N/A"#sdata[7]       #Speed in knots
        trCourse = "N/A"#sdata[8]    #True course
        date = "N/A"#sdata[9][0:2] + "/" + sdata[9][2:4] + "/" + sdata[9][4:6]#date
        
        #actLat = lat[0:2] + " deg " + lat[2:4] + "' " + str(int(lat[5:]) * 60) + "''"
        #actLon = lon[0:2] + " deg " + lon[2:4] + "' " + str(int(lon[5:]) * 60) + "''"
        
        return time, lat, dirLat, lon, dirLon
 
        #print "time : %s, latitude : %s(%s), longitude : %s(%s), speed : %s, True Course : %s, Date : %s" %  (time,lat,dirLat,lon,dirLon,speed,trCourse,date)
 
def decode(coord):
    #Converts DDDMM.MMMMM > DD deg MM.MMMMM min
    x = coord.split(".")
    head = x[0]
    tail = x[1]
    deg = head[0:-2]
    min = head[-2:]
    return deg + " deg " + min + "." + tail + " min"