import spidev
import time
import os
from datetime import datetime

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 1000000


he_channel1 = 0
he_channel2 = 1

t_lastRev1 = time.time()
t_currentRev1 = time.time()

t_lastRev2 = time.time()
t_currentRev2 = time.time()

def ReadChannel(channel):
    adc = spi.xfer2([1,(8+channel)<<4,0])
    data = ((adc[1]&3) << 8) + adc[2]
    return data

for i in range(50000):

    currentVal1 = ReadChannel(he_channel1)
    currentVal2 = ReadChannel(he_channel2)    
        
    t_currentRev1 = time.time()
    RPM1 = 60/(t_currentRev1-t_lastRev1)
    print("magnet ----1---- detected\t"+str(round(RPM1,2)) + "\t"+ str(datetime.now().time()))
    t_lastRev1 = t_currentRev1

	t_currentRev2 = time.time()
    RPM2 = 60/(t_currentRev2-t_lastRev2)
    print("magnet ----2---- detected\t"+str(round(RPM2,2)) + "\t"+ str(datetime.now().time()))    
    t_lastRev2 = t_currentRev2
