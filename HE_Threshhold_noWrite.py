import spidev
import time
import os
from datetime import datetime
 
# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=1000000
#setup channel
he_channel = 0
magnet = False
hasChanged = False
#setup time trackers
t_lastRev = datetime.now().time()
t_currentRev = datetime.now().time()
 

def ReadChannel(channel):
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data
 
#while True:
for i in range(50000): 
	currentVal = ReadChannel(he_channel)
	#print(currentVal)
	
	if (currentVal <20):
		magnet = True
	else:
		magnet = False
		
	if (magnet and not(magnet == hasChanged)):
		t_currentRev = time.now().time()
		RPM = 60/(t_currentRev-t_lastRev)
		print("magnet detected\t"+str(round(RPM,2))+"\t"+str(datetime.now().time()))
	
	hasChanged = magnet
	t_lastRev = t_currentRev	