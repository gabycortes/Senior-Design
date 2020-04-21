import multiprocessing
from random import random
from datetime import datetime, date
#from time import time
import spidev
import time
import queue
import os
import board
import busio
import adafruit_vl6180x

today = date.today()
today = today.strftime("%m-%d-%y")
QUEUE_SIZE = 6000

# time_for_now = datetime.now()
current_time = datetime.now().strftime("%H-%M-%S")
file_name = "/media/pi/BajaSSD1/BajaTest_" + today + "_" + str(current_time)
file = open(file_name + ".csv", "a")

# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=1000000

# Create I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_vl6180x.VL6180X(i2c)

he_channel1 = 0
he_channel2 = 1
magnet1 = False
hasChanged1 = False
magnet2 = False
hasChanged2 = False


t_lastRev1 = time.time()
t_currentRev1 = time.time()

t_lastRev2 = time.time()
t_currentRev2 = time.time()

def ReadChannel(channel):
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data

def consumer(q):
    file = open(file_name + ".csv", "a")
    while q.qsize() > 0 :       
        obj = q.get()
        file.write(str(obj[0])+','+ str(obj[1])+','+str(obj[2])+'\n')
        print(str(obj[0])+','+ str(obj[1])+','+str(obj[2])+'\n')
    file.close()

if __name__ == '__main__':
    
    
    print("READING SENSORS")
    
    file = open(file_name + ".csv", "a")
    file.write(str(QUEUE_SIZE)+"\n")
    file.close()
    
    while True:    
        # print("BEGINNING OF LOOP")
        my_queue = multiprocessing.Queue()
        while my_queue.qsize() < QUEUE_SIZE:
            
            currentVal1 = ReadChannel(he_channel1)
            currentVal2 = ReadChannel(he_channel2)
            
            if (currentVal1 > 980):
                magnet1 = True
            else:
                magnet1 = False

            # start of HE1 RPM Threshold ---------------------
            if (magnet1 and not(magnet1 == hasChanged1)):
                t_currentRev1 = time.time()
                RPM1 = 60/(t_currentRev1-t_lastRev1)
                print("magnet ----1---- detected\t"+str(round(RPM1,2)) + "\t"+ str(datetime.now().time()))
                x = ("HE1", RPM1, datetime.now().time())
                my_queue.put(x)

                distance = sensor.range
                distance /= 25.4
                y = ("Dist", distance, datetime.now().time())
                my_queue.put(y)

            hasChanged1 = magnet1
            t_lastRev1 = t_currentRev1

            # start of HE2 RPM Threshold ---------------------
            if (currentVal2 < 20):
                magnet2 = True
            else:
                magnet2 = False

            if (magnet2 and not(magnet2 == hasChanged2)):
                t_currentRev2 = time.time()
                RPM2 = 60/(t_currentRev2-t_lastRev2)
                print("magnet ----2---- detected\t"+str(round(RPM2,2)) + "\t"+ str(datetime.now().time()))
                x = ("HE2", RPM2, datetime.now().time())
                my_queue.put(x)

                distance = sensor.range
                distance /= 25.4
                y = ("Dist", distance, datetime.now().time())
                my_queue.put(y)

            hasChanged2 = magnet2
            t_lastRev2 = t_currentRev2

        print("SAVING DATA")    
        p = multiprocessing.Process(target=consumer, args=(my_queue,))
         
        p.start()   
        # Wait for the worker to finish
        my_queue.close()
        my_queue.join_thread()
        p.join()
        # print(my_queue.qsize())
    print("FINISHED SAVING DATA")
