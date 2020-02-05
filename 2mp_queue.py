import multiprocessing
from random import random
from datetime import datetime
import queue
import os
import spidev
import time
 
# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=1000000

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

myFile = open("MPpiTest_10-21.csv", "w+")

def producer1(conn, queue):
    for i in range(queue.qsize()):
        msgs = queue.get()
        conn.send(msgs)
        print("\nP1 produced the data: {}".format(msgs))
    conn.close()
    
    
def producer2(conn, queue):
    for i in range(queue.qsize()):
        msgs = queue.get()
        conn.send(msgs)
        print("\nP2 produced the data: {}".format(msgs))
    conn.close()

def producer3(conn, queue):
    for i in range(queue.qsize()):
        msgs = queue.get()
        conn.send(msgs)
        print("\nP3 produced the data: {}".format(msgs))
    conn.close()

def consumer(conn):
    while conn.poll():
        msg = conn.recv()
        print("\nReceived the data: {}".format(msg))
        myFile.write("\n"+str(msg))
    myFile.close()

if __name__ == "__main__":
    #beautify data and check data saving efficiency (delta t avg)
    
    # messages to be sent
    my_queue = queue.Queue()
    
    # creating a pipe
    producer_conn, consumer_conn = multiprocessing.Pipe()
    
        
    # sensor name, data value, timestamp
    #while True:    
    print("BEGINNING OF LOOP")
    
    while my_queue.qsize() < 10:
        print("READING SENSORS")
        currentVal1 = ReadChannel(he_channel1)
        currentVal2 = ReadChannel(he_channel2)
        
        
        if (currentVal1 < 20):
            magnet1 = True
        else:
            magnet1 = False
            
        if (magnet1 and not(magnet1 == hasChanged1)):
            t_currentRev1 = time.time()
            RPM1 = 60/(t_currentRev1-t_lastRev1)
            print("magnet ----1---- detected\t"+str(round(RPM1,2)) + "\t"+ str(datetime.now().time()))
            x = ("HE1", RPM1, datetime.now().time())
            my_queue.put(x)
        hasChanged1 = magnet1
        t_lastRev1 = t_currentRev1

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
        
        hasChanged2 = magnet2
        t_lastRev2 = t_currentRev2
        
        # x = ("Dist", (int(random()*100)), datetime.now().time())
        # my_queue.put(x)
                

    
    # creating new processes
    p1 = multiprocessing.Process(target=producer1, args=(producer_conn, my_queue))
    # p2 = multiprocessing.Process(target=producer2, args=(producer_conn, my_queue))
    # p3 = multiprocessing.Process(target=producer3, args=(producer_conn, my_queue))
    p4 = multiprocessing.Process(target=consumer, args=(consumer_conn,))

    print("PROCESSES STARTING")
    # running processes
    p1.start()
    #p2.start()
    #p3.start()
    p4.start()

    # wait until processes finish
    p1.join()
    #p2.join()
    #p3.join()
    p4.join()
    print("PROCESSES HAVE JOINED, END OF LOOP")
    print(my_queue.qsize())

