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
	for i in range(107):
		if i<=9:
			temp = "/home/neha/Downloads/2011_09_26/2011_09_26_drive_0001_sync/image_00/data/000000000"+str(i)+".png"
		else:
			temp = "/home/neha/Downloads/2011_09_26/2011_09_26_drive_0001_sync/image_00/data/00000000"+str(i)+".png"
		cv_image1 = cv2.imread(temp,cv2.IMREAD_GRAYSCALE)
		cv2.imshow("img2", cv_image1)
		print("m here")
		cv2.waitKey(60)
	print("m out")
    except KeyboardInterrupt:
        print("Shutting Down")
    cv2.destroyAllWindows()
if __name__ == '__main__':
    main(sys.argv)
