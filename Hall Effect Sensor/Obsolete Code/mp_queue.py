import multiprocessing
from random import random
from datetime import datetime
#from time import time
import spidev
import time
import queue
import os
import board
import busio
import adafruit_vl6180x

# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=1000000

# Create I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_vl6180x.VL6180X(i2c)

file = open("HEDATA_10-28.csv", "w+")

he_channel1 = 0
magnet1 = False
hasChanged1 = False


t_lastRev1 = time.time()
t_currentRev1 = time.time()

def ReadChannel(channel):
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data

def consumer(q):
    file = open("HEDATA_10-28.csv", "w+")
    while q.qsize() > 0 :       
        obj = q.get()
        file.write(str(obj[0])+','+ str(obj[1])+','+str(obj[2])+'\n')
        print(str(obj[0])+','+ str(obj[1])+','+str(obj[2])+'\n')
    file.close()

if __name__ == '__main__':
    
    my_queue = multiprocessing.Queue()

#while True:    
    print("BEGINNING OF LOOP")
    
    while my_queue.qsize() < 100:
        print("READING SENSORS")
        currentVal1 = ReadChannel(he_channel1)
        
        if (currentVal1 < 20):
            magnet1 = True
        else:
            magnet1 = False
        
        # start of HE1 RPM Threshold ---------------------
        if (magnet1 and not(magnet1 == hasChanged1)):
            t_currentRev1 = time.time()
            RPM1 = 60/(t_currentRev1-t_lastRev1)
            print("magnet ---- detected\t"+str(round(RPM1,2)) + "\t"+ str(datetime.now().time()))
            x = ("HE1", RPM1, datetime.now().time())
            my_queue.put(x)
        hasChanged1 = magnet1
        t_lastRev1 = t_currentRev1
        
        distance = sensor.range
        distance /= 25.4
        
        # start of HE1 RPM Threshold ---------------------
        # x = ("Dist", distance, datetime.now().time())
        # my_queue.put(x)
        
    p = multiprocessing.Process(target=consumer, args=(my_queue,))
     
    p.start()   
    # Wait for the worker to finish
    my_queue.close()
    my_queue.join_thread()
    p.join()
    print(my_queue.qsize())
