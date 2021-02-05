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
#K_00: 9.842439e+02 0.000000e+00 6.900000e+02 0.000000e+00 9.808141e+02 2.331966e+02 0.000000e+00 0.000000e+00 1.000000e+00
# this is calibration matrix diagonal values are focal length w.r.t. x y z axis   
    k =np.array([[9.842439e+02, 0.000000e+00, 6.900000e+02], 
             [0.000000e+00, 9.808141e+02, 2.331966e+02], 
             [0.000000e+00, 0.000000e+00, 1.000000e+00]])
    proj = np.array([[7.215377e+02,0.000000e+00,6.095593e+02, 0.000000e+00],
		     [0.000000e+00, 7.215377e+02, 1.728540e+02, 0.000000e+00],
		     [0.000000e+00, 0.000000e+00, 1.000000e+00, 0.000000e+00,]])
    temp1 = "/home/neha/Downloads/2011_09_26/2011_09_26_drive_0001_sync/image_00/data/0000000000.png"
    cv_image1 = cv2.imread(temp1,cv2.IMREAD_GRAYSCALE)
    try:
	for i in range(1,107):
		print("now i is",i)
		if i<=9:
			temp = "/home/neha/Downloads/2011_09_26/2011_09_26_drive_0001_sync/image_00/data/000000000"+str(i)+".png"
		elif (i<=99):
			temp = "/home/neha/Downloads/2011_09_26/2011_09_26_drive_0001_sync/image_00/data/00000000"+str(i)+".png"
		else:
			temp = "/home/neha/Downloads/2011_09_26/2011_09_26_drive_0001_sync/image_00/data/0000000"+str(i)+".png"
		cv_image2 = cv2.imread(temp,cv2.IMREAD_GRAYSCALE)
        	sift = cv2.xfeatures2d.SIFT_create()
	        kp1, ds1 = sift.detectAndCompute(cv_image1, None)
		kp2, ds2 = sift.detectAndCompute(cv_image2, None)
		ds1=np.float32(ds1)
    		ds2=np.float32(ds2)
		cv_image1 = cv2.drawKeypoints(cv_image1, kp1, None)
		cv_image2 = cv2.drawKeypoints(cv_image2, kp2, None)
		cv2.imshow("img2", cv_image2)
		bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)
		matches = bf.match(ds1, ds2)
		# queryIdx corresponds to index for 1st img trainIdx corresponds from 2nd img
		kep1=np.float32([kp1[m.queryIdx].pt for m in matches])
		kep2=np.float32([kp2[m.trainIdx].pt for m in matches])
		matching_result = cv2.drawMatches(cv_image1,kp1,cv_image2,kp2,matches,None)
		#cv2.imshow("matching_result", matching_result)
		#finds Essential Matrix 
            	E,mask=cv2.findEssentialMat(kep2,kep1,k,cv2.RANSAC,prob=0.999,threshold=0.1, mask=None)
		retval,rmat,trans,mask=cv2.recoverPose(E,kep1,kep2,k)
#this is ore like correction 
		new_cloud=triangulation(rmat,trans,kep1,kep2,k)
		new_cloud = new_cloud/new_cloud[3]
		cv_image1 = cv_image2
		print("m here")
		print(kep1)
		print(kep2)
		print(len(kep1))
		print(len(kep2))
		print(E)
		print(rmat)
		print(trans)
		print(new_cloud)
		print(len(new_cloud))
		print("m out")
		cv2.waitKey(10)	
    except KeyboardInterrupt:
        print("Shutting Down")
    cv2.destroyAllWindows()

def triangulation(R, t, kp0, kp1, K):
    P0 = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]])
    P0 = K.dot(P0)
    P1 = np.hstack((R, t))
    P1 = K.dot(P1)
    kp0_3d=np.ones((3,kp0.shape[0]))
    kp1_3d=np.ones((3,kp1.shape[0]))
    kp0_3d[0], kp0_3d[1] = kp0[:, 0].copy(), kp0[:, 1].copy()
    kp1_3d[0], kp1_3d[1] = kp1[:, 0].copy(), kp1[:, 1].copy()
    cloud = cv2.triangulatePoints(P0, P1, kp0_3d[:2],kp1_3d[:2])
#     cloud/=cloud[3]
    cloud=cloud.T
    return cloud[:,:3]

if __name__ == '__main__':
    main(sys.argv)
