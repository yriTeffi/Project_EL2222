import numpy as np
import cv2
import RPi.GPIO as GPIO


def main():    
    #See that LEDs are turned off, no passage
    control_lights(0)

    #Min number of matches for match to be validated
    MIN_MATCH_COUNT = 10


    #Read a training image and a test image
    tr = cv2.imread('key.jpg',0)
    test = cv2.imread('key2.jpg',0)

    #Create ORB algorithm to detect something
    orb = cv2.ORB_create()

    #Detect keypoints and compute its descriptors
    kp1, desc1 = orb.detectAndCompute(tr, None)
    kp2, desc2 = orb.detectAndCompute(test, None)

    #Create Brute Force matcher to match 2 things
    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    matches = bf.knnMatch(desc1, desc2, k=2)

    # Apply ratio test
    # So 2 matches are alike distant
    good = []
    for m,n in matches:
        if m.distance < 0.75*n.distance:
            good.append(m)

    #If good match is greater than 10
    if len(good)>MIN_MATCH_COUNT:
        src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
        dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
        
        if mask != None:
            matchesMask = mask.ravel().tolist()
            
            h,w = tr.shape
            pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
            dst = cv2.perspectiveTransform(pts,M)

            test = cv2.polylines(test,[np.int32(dst)],True,255,3, cv2.LINE_AA)

            draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                       singlePointColor = None,
                       matchesMask = matchesMask, # draw only inliers
                       flags = 2)
            #draw matches
            resImg = cv2.drawMatches(tr,kp1,test,kp2,good,None,**draw_params)
            control_lights(1)
            cv2.imshow("card",resImg)
            cv2.waitKey(0)
        else:
            print("Not enough matches are found")
            control_lights(2)

    else:    
        print("Not enough matches are found - %d/%d") % (len(good),MIN_MATCH_COUNT)
        #matchesMask = None
        control_lights(2)

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


#Main function which runs the whole door system.
main()
nr = int(raw_input("To turn off lights, press 0: "))
control_lights(nr)
    
    




