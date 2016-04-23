import numpy as np
import os
import cv2
import RPi.GPIO as GPIO

def main():
    #See that LEDs are turned off, no passage
    control_lights(0)
    take_picture()
    cascade_path = '/home/pi/opencv-3.1.0/data/haarcascades/haarcascade_frontalface_default.xml'
    face_cascade = cv2.CascadeClassifier(cascade_path)

    
    img = cv2.imread("picture.jpg", 0)


    faces = face_cascade.detectMultiScale(img, 1.3, 5)
    for (x,y,w,h) in faces:
        person = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
       
       
    #If one or more faces are detected   
    if len(faces)> 0:
        control_lights(1)
        cv2.imshow('Detected Face',img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        control_lights(2)
        cv2.imshow('No Face Detected',img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    nr = int(raw_input("To turn off lights, press 0: "))
    control_lights(nr)
    

def control_lights(led_nr):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(17, GPIO.OUT)
    GPIO.setup(27, GPIO.OUT)
    #Close door
    if led_nr == 0:
        GPIO.output(17, GPIO.LOW)
        GPIO.output(27, GPIO.LOW)
        print("Both lights are off \n")
    #Person recognized, permission allowed turn Green LED on
    elif led_nr == 1:
        GPIO.output(17, GPIO.HIGH)
        GPIO.output(27, GPIO.LOW)
        print("LED 1 is on \n")
    #Person recognized, but not in database turn Red LED on
    elif led_nr == 2:
        GPIO.output(27, GPIO.HIGH)
        GPIO.output(17, GPIO.LOW)
        print("LED 2 is on \n")
    #No person recognized
    else:    
        print("Unrecognize control number " + str(led_nr) + "\n")

def take_picture():
    os.system("fswebcam picture.jpg")

main()
