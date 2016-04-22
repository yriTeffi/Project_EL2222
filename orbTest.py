import numpy as np
import cv2

#Min number of matches for match to be validated
MIN_MATCH_COUNT = 10


#Read a training image and a test image
tr = cv2.imread('key.jpg',0)
test = cv2.imread('nokey.jpg',0)

#Create ORB algorithm
orb = cv2.ORB_create()

#Detect keypoints and compute its descriptors
kp1, desc1 = orb.detectAndCompute(tr, None)
kp2, desc2 = orb.detectAndCompute(test, None)

#Create BF matcher
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

        cv2.imshow("card",resImg)
        cv2.waitKey(0)
    else:
        print("Not enough matches are found")

else:    
    print("Not enough matches are found - %d/%d") % (len(good),MIN_MATCH_COUNT)
    #matchesMask = None





