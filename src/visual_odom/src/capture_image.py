#!/usr/bin/env python

import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import sys
import numpy as np

def main(args):
    rospy.init_node('image_converter', anonymous=True)
    print("i m in")
    try:
		temp1 = "/home/neha/Downloads/2011_09_26/2011_09_26_drive_0001_sync/image_00/data/0000000001.png"
		temp2 = "/home/neha/Downloads/2011_09_26/2011_09_26_drive_0001_sync/image_00/data/0000000002.png"
		cv_image1 = cv2.imread(temp1,cv2.IMREAD_GRAYSCALE)
		cv_image2 = cv2.imread(temp2,cv2.IMREAD_GRAYSCALE)
        	sift = cv2.xfeatures2d.SIFT_create()
	        kp1, ds1 = sift.detectAndCompute(cv_image1, None)
		kp2, ds2 = sift.detectAndCompute(cv_image2, None)
		ds1=np.float32(ds1)
    		ds2=np.float32(ds2)
		cv_image1 = cv2.drawKeypoints(cv_image1, kp1, None)
		cv_image2 = cv2.drawKeypoints(cv_image2, kp2, None)
		cv2.imshow("img1", cv_image1)
		cv2.imshow("img2", cv_image1)
		bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)
		matches = bf.match(ds1, ds2)
		kep1=np.float32([kp1[m.queryIdx].pt for m in matches])
		kep2=np.float32([kp2[m.trainIdx].pt for m in matches])
		matching_result = cv2.drawMatches(cv_image1,kp1,cv_image2,kp2,matches,None)
		cv2.imshow("matching_result", matching_result)
		print(kep1)
		print(kep2)
		print(len(kep1))
		print(len(kep2))

		cv2.waitKey()	
		print("m out")
    except KeyboardInterrupt:
        print("Shutting Down")
    cv2.destroyAllWindows()
if __name__ == '__main__':
    main(sys.argv)
