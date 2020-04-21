from picamera import PiCamera
from time import sleep

camera = PiCamera()

camera.start_preview(alpha=180)
camera.annotate_text="Hello World!"
sleep(2)
camera.capture('/home/pi/Desktop/text.png')
camera.stop_preview()
