import digitalio
import busio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
from datetime import datetime
import time

spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D22)
mcp = MCP.MCP3008(spi, cs)
channel0 = AnalogIn(mcp, MCP.PO)

magnet = False
hasChanged = False

t_lastRev = datetime.now().time()
t_currentRev = datetime.now().time()


#file = open("HEDATA.csv", "w+")

#for i in range(1000):
while True:
	currentVal = channel0.value
	if (currentVal <450):
		magnet = True
	else:
		magnet = False
		
	if (magnet and not(magnet == hasChanged)):
		t_currentRev = datetime.now().time()
		RPM = (t_currentRev-t_lastRev)
		print("magnet detected\t"+str(RPM)+"\t"+str(datetime.now().time()))
	
	# save data to external file with timestamp
	# method 1: use a threshhold to find rev's 
	# method 2: use a maximums to find ver's 
	hasChanged = magnet
	t_lastRev = t_currentRev	
	#print(str(magnet)"\t"+str(datetime.now().time()))
	#file.write("\n"+str(currentVal))
	#time.sleep(0.1)

#file.close()