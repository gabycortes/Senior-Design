import digitalio
import busio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
from datetime import datetime

spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D22)
mcp = MCP.MCP3008(spi, cs)
channel0 = AnalogIn(mcp, MCP.PO)

file = open("HEDATA.csv", "w+")

for i in range(3000):
	currentVal = channel0.value
	# save data to external file with timestamp
	# method 1: use a threshhold to find rev's 
	# method 2: use a maximums to find ver's 
	print(currentVal)
	print("\t"+str(datetime.now().time()))
	file.write("\n"+str(currentVal))

file.close()