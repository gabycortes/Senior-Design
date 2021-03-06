import time
import serial
import gmplot 

file = open("gps6.csv", "w+")


lat_list = []
lng_list = []
gmap1 = gmplot.GoogleMapPlotter(34.1119131, -118.2075095, 13 ) 
gmap1.apikey = "AIzaSyCwwzLYbIDnY0G_7DmqtsH1CmKltblaaA8"

def readString():
    while 1:
            while ser.read().decode("utf-8") != '$':
                pass
            line = ser.readline().decode("utf-8")
            return line
        
def getTime(string, format, returnFormat):
    return time.strftime(returnFormat, time.strptime(string, format))
    
def getLatLng(latString, lngString):
    try:
        lat = latString[:2].lstrip('0') + "." + "%.7s" % str(float(latString[2:]) * 1 / 60).lstrip("0.")
        lng = lngString[:3].lstrip('0') + "." + "%.7s" % str(float(lngString[3:]) * 1 / 60).lstrip("0.")
        return lat, lng
    except:
        print("")
    
def printGLL(lines):
    try:
        print("========================================GLL========================================")
        latlng = getLatLng(lines[1], lines[3])
        print("Lat,Long: ", latlng[0], lines[2], ", ", "-", latlng[1], lines[4], sep='')
        print("Fix taken at:", getTime(lines[5], "%H%M%S.%f", "%H:%M:%S"), "UTC")
        return
    except:
        print("")
                
def checksum(line): 

    checkString = line.partition("*") 
    checksum = 0 
    for c in checkString[0]: 
        checksum ^= ord(c) 

    try:  # Just to make sure 
        inputChecksum = int(checkString[2].rstrip(), 16) 

    except: 
        print("Error in string") 
        return False 

    if checksum == inputChecksum: 
        return True 

    else: 
        print("=====================================================================================") 
        print("===================================Checksum error!===================================") 
        print("=====================================================================================") 
        print(hex(checksum), "!=", hex(inputChecksum)) 
        return False 

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    try: 
        while True: 
        
            line = readString() 
            lines = line.split(",")
        
            if checksum(line):
        
                if lines[0] == "GPGLL": 
    	    
                    try:
                        printGLL(lines)
                        latlng = getLatLng(lines[1], lines[3])
                        newLat = float(latlng[0])
                        newLng = float(latlng[1])
                        newLat *= -1 if lines[2] == 'S' else 1
                        newLng *= -1 if lines[4] == 'W' else 1
                        file.write("\n" + str(getTime(lines[5], "%H%M%S.%f", "%H:%M:%S"))+ "," + str(newLat) + "," + str(newLng))
                        lat_list.append(newLat)
                        lng_list.append(newLng)
                    except:
                        print("")
                else:
                   print("")

    except KeyboardInterrupt: 
        print('Exiting Script')
   
gmap1.scatter(lat_list, lng_list, '#FF0000',size = 1, marker = False)
gmap1.plot(lat_list, lng_list, 'cornflowerblue', edge_width = 1)
gmap1.draw("newTest6.html")

file.close() 


