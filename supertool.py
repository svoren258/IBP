#!/usr/bin/python

from __future__ import division
import numpy as np
import io
import os
import random
import cv2
import re
import ast
import sys, getopt
import errno
from matplotlib import pyplot as plt
from PIL import Image

coordinates_x = []
coordinates_y = []
# path_to_dst = ''
# path_to_src = ''

path_to_tmp = 'templates/'
path_to_rz = 'RZ/'
path_to_output = 'final/'
my_filenames = []

def argparse(argv):
	global path_to_tmp
	global path_to_rz
	global path_to_output
	try:
		opts, args = getopt.getopt(argv,"ht:r:o:")
	except getopt.GetoptError:
		print 'Usage: python supertool.py -t [path_to_tmp] -r [path_to_rz] -o [path_to_output]'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'Usage: python supertool.py -t [path_to_tmp] -r [path_to_rz] -o [path_to_output]'
			sys.exit()
		elif opt in ('-t'):
			path_to_tmp = arg
		elif opt in ('-r'):
			path_to_rz = arg
		elif opt in ('-o'):
			path_to_output = arg

	print 'Path to templates: ', path_to_tmp
	print 'Path to rz: ', path_to_rz
	print 'Path to output: ', path_to_output

argparse(sys.argv[1:])

i = 0

filename = path_to_output
if not os.path.exists(os.path.dirname(filename)):
    try:
        os.makedirs(os.path.dirname(filename))
    except OSError as exc: # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise

for root, dirs, files in os.walk(path_to_tmp):
	for file_name in files:
		if  file_name.endswith('.txt'):
			continue
		my_filenames.append(file_name)
		my_filenames = sorted(my_filenames)
		# print file_name
		# print int(file_name[0]+file_name[1]+file_name[2])
		# if (int(file_name[0]+file_name[1]+file_name[2]) == i):
		# 	break
		# elif (int(file_name[0]+file_name[1]+file_name[2]) != i):
		# 	continue
for file_name in my_filenames:
	coordinates_x = []
	coordinates_y = []
	i += 1
	print file_name
	file = open(path_to_tmp+file_name+'.txt','r')
	#print file.read()
	points = file.read()
	#print points
	points = ast.literal_eval(points)
	# print points
	for point in points:
		coordinates_x.append(point[0])
		coordinates_y.append(point[1])
	# print coordinates_x
	# print coordinates_y
	
	pts_dst = np.vstack(points).astype(float)
	#print pts_dst
	# for root, dirs, reg_nums in os.walk(path_to_rz):
	# 	for regnum_name in reg_nums:
	# 		print regnum_name

	im_dst = cv2.imread('templates/'+file_name,1)

	im_dst = cv2.resize(im_dst, (0,0), fx=0.25, fy=0.25)

	rz = random.choice(os.listdir(path_to_rz))
	im_src = cv2.imread(path_to_rz+rz,1)

	size = im_src.shape

	# Create a vector of source points.
	pts_src = np.array(
	                   [
	                    [0,0],
	                    [size[1] - 1, 0],
	                    [size[1] - 1, size[0] -1],
	                    [0, size[0] - 1 ]
	                    ],dtype=float
	                   );

	# Calculate Homography between source and destination points
	h, status = cv2.findHomography(pts_src, pts_dst);

	# Warp source image
	im_temp = cv2.warpPerspective(im_src, h, (im_dst.shape[1],im_dst.shape[0]))

	# Black out polygonal area in destination image.
	cv2.fillConvexPoly(im_dst, pts_dst.astype(int), 0, 16)

	# Add warped source image to destination image.
	im_out = im_dst + im_temp

	#Resize image to wanted size
	im_out = im_out[int(0.8*min(coordinates_y)):int(1.2*max(coordinates_y)), int(0.8*min(coordinates_x)):int(1.2*max(coordinates_x))]

	#Save image to wanted directory
	cv2.imwrite(filename+str(i)+'.jpg',im_out)

#my_filenames = my_filenames.sort()
#my_filenames = sort_list(my_filenames)
# my_filenames = sorted(my_filenames)
# print my_filenames
#print sorted(my_filenames, key=my_filenames[0])
#print my_filenames