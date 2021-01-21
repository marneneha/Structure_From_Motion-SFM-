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
	cv_image = cv2.imread("/home/neha/Downloads/turtlebot/src/maps/playground1.pgm",cv2.IMREAD_UNCHANGED)
        sift = cv2.xfeatures2d.SIFT_create()
        #kp = sift.detect(cv_image, None)
        #cv_image = cv2.drawKeypoints(cv_image, kp, None)
	cv2.imshow("neha", cv_image)
	cv2.waitKey()
	print("m out")
    except KeyboardInterrupt:
        print("Shutting Down")
    cv2.destroyAllWindows()
if __name__ == '__main__':
    main(sys.argv)
