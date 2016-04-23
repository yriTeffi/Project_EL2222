#This script serves as a test to see how LED works 
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)

GPIO.setwarnings(False)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)

print("Lights are on")
GPIO.output(17, GPIO.LOW)
GPIO.output(27, GPIO.LOW)
