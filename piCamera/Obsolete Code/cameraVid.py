#import filetype
from picamera import PiCamera
import picamera
from time import sleep
import datetime as dt
#now = datetime.datetime.now()

camera = PiCamera()

camera.start_preview(alpha=180)
camera.annotate_text_size = 80
camera.annotate_background = picamera.Color('black')
camera.annotate_text=dt.datetime.now().strftime("%H:%M:%S")
camera.start_recording('/home/pi/Desktop/testvid2.h264')
start = dt.datetime.now()
while (dt.datetime.now() - start).seconds < 3:
        camera.annotate_text = dt.datetime.now().strftime("%H:%M:%S")
        camera.wait_recording(0.2)
#sleep(5)
camera.stop_recording()
camera.stop_preview()
