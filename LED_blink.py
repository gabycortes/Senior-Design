import RPi.GPIO as GPIO

from time import sleep
import datetime

LED_PIN = 16

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT, initial=GPIO.LOW)

while True:
	GPIO.output(LED_PIN, GPIO.HIGH)
	print("LED on")
	sleep(0.25)
	GPIO.output(LED_PIN, GPIO.LOW)
	print("LED off")
	sleep(0.25)
	print(datetime.datetime.now().time())
	