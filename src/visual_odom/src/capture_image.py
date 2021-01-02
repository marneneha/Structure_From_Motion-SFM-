#!/usr/bin/env python

import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import sys


def main(args):
    rospy.init_node('image_converter', anonymous=True)
    print("i m in")
    try:
	cv_image1 = cv2.imread("/home/neha/Downloads/neha.jpg",cv2.IMREAD_GRAYSCALE)
	cv_image2 = cv2.imread("/home/neha/Downloads/neha (1).jpg",cv2.IMREAD_GRAYSCALE)
        sift = cv2.xfeatures2d.SIFT_create()
        kp1, ds1 = sift.detectAndCompute(cv_image1, None)
        kp2, ds2 = sift.detectAndCompute(cv_image2, None)
        cv_image1 = cv2.drawKeypoints(cv_image1, kp1, None)
        cv_image2 = cv2.drawKeypoints(cv_image2, kp2, None)
	cv2.imshow("img1", cv_image1)
	cv2.imshow("img2", cv_image1)
	bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)
	matches = bf.match(ds1, ds2)
	matching_result = cv2.drawMatches(cv_image1,kp1,cv_image2,kp2,matches,None)
	cv2.imshow("matching_result", matching_result)
	cv2.waitKey()
	print("m out")
    except KeyboardInterrupt:
        print("Shutting Down")
    cv2.destroyAllWindows()
if __name__ == '__main__':
    main(sys.argv)
