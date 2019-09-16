import Adafruit_GPIO as SPI
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

spi = busio.SPI(clock = board.SCK, MISO = board.MISO, MOSI = board.MOSI)