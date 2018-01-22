#/usr/bin/python

from __future__ import division
import numpy as np
import io
import os
import random
import cv2
import re
import sys, getopt
import errno
from matplotlib import pyplot as plt
from PIL import Image

# coordinates_x = []
# coordinates_y = []
coordinates = []
src_path = ''
# path_to_dst = ''
# path_to_src = ''

def argparse(argv):
	global path
	try:
		opts, args = getopt.getopt(argv,"hi:o:")
	except getopt.GetoptError:
		print 'Usage: python clicker.py -i [src_path]'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'Usage: python clicker.py -i [src_path]'
			sys.exit()
		elif opt in ("-i"):
			src_path = arg

	print 'Source Path: ', src_path

argparse(sys.argv[1:])

def mouse_handler(event, x, y, flags, data) :
    global coordinates
    if event == cv2.EVENT_LBUTTONDOWN :
    	if len(data['points']) < 4 :
	        img_copy = data['im'].copy()
	        cv2.circle(data['im'], (x,y),1, (0,0,255), 5, 16);
	        cv2.imshow("Image", data['im']);
	        ix,iy = x, y

	        while(1):
	        	k = cv2.waitKey(20) & 0xFF
	        	if k == ord('a'):
	        		data['im'] = img_copy.copy()
	        		cv2.circle(data['im'], (ix-1,iy),1, (0,0,255), 5, 16)
	        		ix = ix-1
	       			cv2.imshow("Image", data['im'])
	       			continue
	       		if k == ord('d'):
					data['im'] = img_copy.copy()
					cv2.circle(data['im'], (ix+1,iy),1, (0,0,255), 5, 16)
					ix = ix+1
					cv2.imshow("Image", data['im'])
					continue
	       		if k == ord('w'):
	       			data['im'] = img_copy.copy()
	        		cv2.circle(data['im'], (ix,iy-1),1, (0,0,255), 5, 16)
	        		iy = iy-1
	       			cv2.imshow("Image", data['im'])
	       			continue
	       		if k == ord('s'):
	       			data['im'] = img_copy.copy()
	        		cv2.circle(data['im'], (ix,iy+1),1, (0,0,255), 5, 16)
	        		iy = iy+1
	       			cv2.imshow("Image", data['im'])
	       			continue
	       		if k == ord('z'):
					data['im'] = img_copy.copy()
					cv2.imshow("Image", data['im'])
					continue
	       		if k == ord('x'):
	       			if len(data['points']) < 4 :
						#coordinates.append([x,y])
						data['points'].append([x,y])
					# coordinates_x.append(x)
					# coordinates_y.append(y)
	       			break
	       		# if k == ord('r'):
	       		# 	print coordinates
        # if len(data['points']) < 4 :
        #     data['points'].append([x,y])

def get_four_points(im):
    
    # Set up data to send to mouse handler
    data = {}
    data['im'] = im.copy()
    data['points'] = []
    
    #Set the callback function for any mouse event
    cv2.imshow("Image",im)
    cv2.setMouseCallback("Image", mouse_handler, data)
    cv2.waitKey(0)
    
    # Convert array to np.array
    #points = np.vstack(data['points']).astype(float)
    
    return data['points']

filename = 'photo_templates_front/'
if not os.path.exists(os.path.dirname(filename)):
	try:
	    os.makedirs(os.path.dirname(filename))
	except OSError as exc: # Guard against race condition
	    if exc.errno != errno.EEXIST:
	        raise


# Read destination image
for root, dirs, files in os.walk('/home/svoren258/Dokumenty/FIT_VUT/3_BIT/IBP/IBP/photo_templates_front/'):
	for file_name in files:
		if file_name.endswith('.txt'):
			continue
		im_dst = cv2.imread('photo_templates_front/'+file_name,1)
		im_dst = cv2.resize(im_dst, (0,0), fx=0.25, fy=0.25) 

		#im_dst = cv2.imread('/home/svoren258/Dokumenty/FIT_VUT/3_BIT/IBP/IBP/templates/001.jpg',1)
		#im_dst = cv2.imread(path_to_dst,1)

		#im_dst = cv2.resize(im_dst, (0,0), fx=0.25, fy=0.25) 

		# im_bef = im_dst.copy()
		# Get four corners of the billboard
		# print 'Click on four corners and then press ENTER'
		pts_dst = get_four_points(im_dst)

		#print pts_dst
		file = open('photo_templates_front/'+file_name+'.txt','w')
		file.write(str(pts_dst)+"\n")
		file.close()
		
		# Display image.
		while(1):
			cv2.imshow("Image", im_dst)
			#cv2.imshow("Before", im_bef)
			k = cv2.waitKey(20) & 0xFF
			if k == 27:
				break
		# cv2.waitKey(0);
		cv2.destroyAllWindows()