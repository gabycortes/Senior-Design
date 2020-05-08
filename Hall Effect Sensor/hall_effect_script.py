import multiprocessing
from random import random
from datetime import datetime, date
import spidev
import time
import queue
import os
import board
import busio
import adafruit_vl6180x

# Get the current date and set the size of the queue.
today = date.today()
today = today.strftime("%m-%d-%y")
QUEUE_SIZE = 6000

# Get the current time and initialize the file where the data will be saved.
current_time = datetime.now().strftime("%H-%M-%S")
file_name = "/media/pi/BajaSSD1/BajaTest_" + today + "_" + str(current_time)
file = open(file_name + ".csv", "a")

# Open SPI bus.
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=1000000

# Create I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)
# Create an instance of the distance sensor.
sensor = adafruit_vl6180x.VL6180X(i2c)

# Initialize instance variables.
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
  # Gets information from hall effect sensors.
  # Turns it into usable digital data.
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data

def consumer(q):
    # Once the queue is full, take data from queue and write it into .csv file.
    # Continues until the queue is empty.
    file = open(file_name + ".csv", "a")
    while q.qsize() > 0 :       
        obj = q.get()
        file.write(str(obj[0])+','+ str(obj[1])+','+str(obj[2])+'\n')
        print(str(obj[0])+','+ str(obj[1])+','+str(obj[2])+'\n')
    file.close()

if __name__ == '__main__':
    
    print("READING SENSORS")
    
    # Write the size of the queue into the first line of the .csv file.
    file = open(file_name + ".csv", "a")
    file.write(str(QUEUE_SIZE)+"\n")
    file.close()
    
    while True:    
        # Initialize the queue.
        my_queue = multiprocessing.Queue()
        
        # Add to the queue until the specified size has been reached.
        while my_queue.qsize() < QUEUE_SIZE:
            
            # Get the raw digital data from the hall effect sensors.
            currentVal1 = ReadChannel(he_channel1)
            currentVal2 = ReadChannel(he_channel2)
            
            # start of HE1 RPM Threshold ---------------------
            
            # Determine if the hall effect sensor is over a magnet.
            # 980 was the most optimal value to serve as the threshold.
            if (currentVal1 > 980):
                magnet1 = True
            else:
                magnet1 = False
           
            # If the magnet is over the hall effect sensor, a full revolution happened.
            if (magnet1 and not(magnet1 == hasChanged1)):
              
                # Set the time of the current revolution.
                t_currentRev1 = time.time()
                
                # Calculate the RPM and put it into the queue.
                RPM1 = 60/(t_currentRev1-t_lastRev1)
                print("magnet ----1---- detected\t"+str(round(RPM1,2)) + "\t"+ str(datetime.now().time()))
                x = ("HE1", RPM1, datetime.now().time())
                my_queue.put(x)
                
                # Get the current range of the distance sensor and put it into the queue.
                distance = sensor.range
                distance /= 25.4
                y = ("Dist", distance, datetime.now().time())
                my_queue.put(y)
            
            hasChanged1 = magnet1
            t_lastRev1 = t_currentRev1

            
            # start of HE2 RPM Threshold ---------------------
            
            # The HE2 RPM Threshold is largely the same as HE1 RPM Threshold
            # 20 was chosen instead of 980 as the magnet was flipped. 
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

        # Once the queue is full, call the consumer() to extract the data.
        print("SAVING DATA")    
        p = multiprocessing.Process(target=consumer, args=(my_queue,))
         
        p.start()   
        
        # Wait for the worker to finish
        my_queue.close()
        my_queue.join_thread()
        p.join()

    print("FINISHED SAVING DATA")
