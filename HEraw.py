import digitalio
import busio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
#set up the adc
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D22)
mcp = MCP.MCP3008(spi, cs)
channel0 = AnalogIn(mcp, MCP.PO)

# get valuable form the adc
for i in range(1000):
	currentVal = channel0.value
	print(currentVal)