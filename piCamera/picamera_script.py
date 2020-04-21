import time
import os
import sys
from picamera import PiCamera
from datetime import datetime

file_name = sys.argv[1]
os.mkdir(file_name)

camera = PiCamera()
print(file_name)
print("Started taking pictures")

while True:
	time_taken = time.asctime(time.gmtime())
	ini_time_for_now = datetime.now()
	current_time = ini_time_for_now.strftime("%H-%M-%S")
	#camera.capture('%s/picamera_pictures/testpic%s.jpg' % file_name, current_time)
	img_name = file_name + "/testpic" + current_time + ".jpg"
	camera.capture(img_name)
	camera.stop_preview()
	time.sleep(3)
