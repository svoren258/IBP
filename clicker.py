#!/usr/bin/python
# -*- coding: utf-8 -*-

# Author: Ondrej Svoreň, 3 BIT
# Subject: IBP - Bachelor Thesis
# Thesis Name: Synthetic Dataset Generator for Traffic Analysis
# Supervisor: prof. Ing. Adam Herout PhD.
# School Year: 2017/18

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

coordinates = []
src_path = 'photo_templates_front/'

# Input arguments parser
def argparse(argv):
	global src_path
	try:
		opts, args = getopt.getopt(argv,"hi:o:")
	except getopt.GetoptError:
		print 'Usage: python clicker.py -i [src_path]'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print (
				'Usage: python clicker.py -i [src_path]\n'
				'	Click on the corners of license number to get 4 corner coordinates of it.\n'
				'	After clicking, you can move red point on the picture (indicates position) in following way:\n'
				'	key W - UP\n'
				'	key A - LEFT\n'
				'	key S - DOWN\n'
				'	key D - RIGHT\n'
				'	key X - ENTER\n'
				'	key Z - BACK\n'
				)

			sys.exit()
		elif opt in ("-i"):
			src_path = arg

	print 'Source Path: ', src_path

argparse(sys.argv[1:])

# Function handles mouse and keyboard events
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
	        	# Key A => LEFT
	        	if k == ord('a'):
	        		data['im'] = img_copy.copy()
	        		cv2.circle(data['im'], (ix-1,iy),1, (0,0,255), 5, 16)
	        		ix = ix-1
	       			cv2.imshow("Image", data['im'])
	       			continue
	       		# Key D => RIGHT
	       		if k == ord('d'):
					data['im'] = img_copy.copy()
					cv2.circle(data['im'], (ix+1,iy),1, (0,0,255), 5, 16)
					ix = ix+1
					cv2.imshow("Image", data['im'])
					continue
				# Key W => UP
	       		if k == ord('w'):
	       			data['im'] = img_copy.copy()
	        		cv2.circle(data['im'], (ix,iy-1),1, (0,0,255), 5, 16)
	        		iy = iy-1
	       			cv2.imshow("Image", data['im'])
	       			continue
	       		# Key S => DOWN
	       		if k == ord('s'):
	       			data['im'] = img_copy.copy()
	        		cv2.circle(data['im'], (ix,iy+1),1, (0,0,255), 5, 16)
	        		iy = iy+1
	       			cv2.imshow("Image", data['im'])
	       			continue
	       		# Key Z => BACK
	       		if k == ord('z'):
					data['im'] = img_copy.copy()
					cv2.imshow("Image", data['im'])
					continue
				# Key X => ENTER
	       		if k == ord('x'):
	       			if len(data['points']) < 4 :
						data['points'].append([x,y])
	       			break

def get_four_points(im):
    # Set up data to send to mouse handler
    data = {}
    data['im'] = im.copy()
    data['points'] = []
    
    #Set the callback function for any mouse event
    cv2.imshow("Image",im)
    cv2.setMouseCallback("Image", mouse_handler, data)
    cv2.waitKey(0)
    
    return data['points']

# Read destination image
for root, dirs, files in os.walk('/home/svoren258/Dokumenty/FIT_VUT/3_BIT/IBP/IBP/photo_templates_front/'):
	for file_name in files:
		if file_name.endswith('.txt'):
			continue
		im_dst = cv2.imread('photo_templates_front/'+file_name,1)
		im_dst = cv2.resize(im_dst, (0,0), fx=0.25, fy=0.25) 

		# Get four corners of the billboard
		pts_dst = get_four_points(im_dst)

		file = open('photo_templates_front/'+file_name+'skuska.txt','w')
		file.write(str(pts_dst)+"\n")
		file.close()
		
		# Display image.
		while(1):
			cv2.imshow("Image", im_dst)
			k = cv2.waitKey(20) & 0xFF
			if k == 27:
				break

		cv2.destroyAllWindows()