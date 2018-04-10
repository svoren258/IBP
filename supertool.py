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
import math
import cv2
import re
import ast
import sys, getopt
import errno
import json
from matplotlib import pyplot as plt
from PIL import Image

path_to_tmp = 'photo_templates_front2/'
path_to_rz = 'RZ/'
path_to_output = 'final/'

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

# Function shows image until keypressed
def showImage(image, name='img'):
	cv2.imshow(name,image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

# Function adds Gaussian noise
def add_gaussian_noise(image_in):
	noise_sigma = 20
	temp_image = np.float64(np.copy(image_in))

	h = temp_image.shape[0]
	w = temp_image.shape[1]
	noise = np.random.randn(h, w) * noise_sigma
	noisy_image = np.zeros(temp_image.shape, np.float64)

	if len(temp_image.shape) == 2:
	    noisy_image = temp_image + noise
	else:
	    noisy_image[:,:,0] = temp_image[:,:,0] + noise
	    noisy_image[:,:,1] = temp_image[:,:,1] + noise
	    noisy_image[:,:,2] = temp_image[:,:,2] + noise
	
	# noisy_image = convert_to_uint8(noisy_image)
	return noisy_image
   

# Another Gaussian noise
def gaussianNoise(img):
	m = (20,20,20) 
	s = (20,20,20)
	noise = cv2.randn(img,m,s)
	noisy_image = cv2.add(noise, img)
	return noisy_image


def convert_to_uint8(image_in):
    temp_image = np.float64(np.copy(image_in))
    showImage(temp_image)
    cv2.normalize(temp_image, temp_image, 0, 255, cv2.NORM_MINMAX, dtype=-1)
    return temp_image.astype(np.uint8)

# Function creates output directory
def createOutputDir():
	filename = path_to_output
	if not os.path.exists(os.path.dirname(filename)):
	    try:
	        os.makedirs(os.path.dirname(filename))
	    except OSError as exc: # Guard against race condition
	        if exc.errno != errno.EEXIST:
	            raise

	return filename

# Function creates array of template filenames
def createTemplates():
	my_filenames = []
	for root, dirs, files in os.walk(path_to_tmp):
		for tmp_name in files:
			if tmp_name.endswith('.txt'):
				continue
			my_filenames.append(tmp_name)
	return my_filenames

# Function creates JSON file related with output image, this JSON file contains output image specification
def createJson(file_name, coordinates, outputDir, i, gauss, motion):
	txtfile = open(path_to_rz + file_name + '.txt','r')
	reg_num = txtfile.readline()
	info = reg_num.split()
	txtfile.close()

	data = {
		'lp_text' : info[0],
		'nation' : info[1],
		'point0' : coordinates[0],
		'point1' : coordinates[1],
		'point2' : coordinates[2],
		'point3' : coordinates[3],
		'gaussian_blur' : gauss,
		'motion_blur' : motion,
	}

	json_string = json.dumps(data, sort_keys=True)
	json_file = open(outputDir+str(i)+'.jpg.json','w')
	json_file.write(json_string)
	json_file.close()

# Function returns final coordinates of the license plate included in output image
def getFinalCoords(coordinates_x, coordinates_y):
	new_coords_x = []
	new_coords_y = []

	for x in coordinates_x:
		x = x - (int(0.8*min(coordinates_x)))
		new_coords_x.append(x)
	
	for y in coordinates_y:
		y = y - (int(0.8*min(coordinates_y)))
		new_coords_y.append(y)

	final_coords = [[new_coords_y[0],new_coords_x[0]],[new_coords_y[1],new_coords_x[1]],[new_coords_y[2],new_coords_x[2]],[new_coords_y[3],new_coords_x[3]]]

	return final_coords

# Function creates output image by finding homography, warping perspective and merging that way source and destination image
def createOutputImage(im_src, im_dst, pts_src, pts_dst, coordinates_x, coordinates_y):

	# Find homography
	h, status = cv2.findHomography(pts_src, pts_dst)

	# Warp source image
	im_temp = cv2.warpPerspective(im_src, h, (im_dst.shape[1],im_dst.shape[0]), cv2.INTER_LINEAR)#, borderMode=cv2.BORDER_TRANSPARENT)
	
	# Black out polygonal area in destination image.
	cv2.fillConvexPoly(im_dst, pts_dst.astype(int), 0, 16)

	# Add warped source image to destination image.
	im_out = im_dst + im_temp

	return im_out;

	#Resize image to wanted size
	# output_img = im_out[int(0.8*min(coordinates_y)):int(1.2*max(coordinates_y)), int(0.8*min(coordinates_x)):int(1.2*max(coordinates_x))]

	# return output_img

# Function returns destination image
def getDestinationImage(tmp):
	im_dst = cv2.imread(path_to_tmp+tmp,1)
	im_dst = cv2.resize(im_dst, (0,0), fx=0.25, fy=0.25, interpolation = cv2.INTER_AREA)
	return im_dst

# Function returns source image
def getSourceImage(file_name):

	im_src = cv2.imread(path_to_rz+file_name,1)
	im_hsv = cv2.cvtColor(im_src, cv2.COLOR_BGR2HSV)

	# Brightness and contrast changing	
	for x in range(0, len(im_hsv)):
		for y in range(0, len(im_hsv[0])):
			im_hsv[x,y][2] *= 0.675

	im_src = cv2.cvtColor(im_hsv, cv2.COLOR_HSV2BGR)

	# Resize registration number to apply antialiasing
	im_src = cv2.resize(im_src, (0,0), fx=0.375, fy=0.375, interpolation = cv2.INTER_AREA)

	im_src = cv2.fastNlMeansDenoisingColored(im_src,None,8,8,7,21)

    #Application of Gaussian noise
	im_src = add_gaussian_noise(im_src)

	return im_src

# Fuction returns coordinates of license plate situated on destination image
def getDestinationPoints(tmp, coordinates, coordinates_x, coordinates_y):
	file = open(path_to_tmp + tmp + '.txt','r')
	points = file.read()
	#print points
	points = ast.literal_eval(points)
	for point in points:
		coordinates.append(point)
		coordinates_x.append(point[0])
		coordinates_y.append(point[1])

	pts_dst = np.vstack(points).astype(float)
	return pts_dst

# Function returns coordinates of license plate image (source image)
def getSourcePoints(im_src):
	size = im_src.shape

	# Getting source image points
	pts_src = np.array(
			           [
			            [0,0],
			            [size[1] - 1, 0],
			            [size[1] - 1, size[0] -1],
			            [0, size[0] - 1 ]
			            ],dtype=float
			           );
	return pts_src

# Function applies to the image motion blur
def applyMotionBlur(image):

	size = 15

	# generating the kernel
	kernel_motion_blur = np.zeros((size, size))
	kernel_motion_blur[int((size-1)/2), :] = np.ones(size)
	kernel_motion_blur = kernel_motion_blur / size

	# applying the kernel to the input image
	output = cv2.filter2D(image, -1, kernel_motion_blur)

	return output

def warpImage(img):
	rows, cols = img.shape[:2]

	#####################
	# Vertical wave

	img_output = np.zeros(img.shape, dtype=img.dtype)

	for i in range(rows):
	    for j in range(cols):
	        offset_x = int(25.0 * math.sin(2 * 3.14 * i / 180))
	        offset_y = 0
	        if j+offset_x < rows:
	            img_output[i,j] = img[i,(j+offset_x)%cols]
	        else:
	            img_output[i,j] = 0

	showImage(img, 'Input')
	showImage(img_output, 'Vertical wave')

	#####################
	# Horizontal wave

	img_output = np.zeros(img.shape, dtype=img.dtype)

	for i in range(rows):
	    for j in range(cols):
	        offset_x = 0
	        offset_y = int(16.0 * math.sin(2 * 3.14 * j / 150))
	        if i+offset_y < rows:
	            img_output[i,j] = img[(i+offset_y)%rows,j]
	        else:
	            img_output[i,j] = 0

	showImage(img_output, 'Horizontal wave')

	#####################
	# Both horizontal and vertical 

	img_output = np.zeros(img.shape, dtype=img.dtype)

	for i in range(rows):
	    for j in range(cols):
	        offset_x = int(20.0 * math.sin(2 * 3.14 * i / 150))
	        offset_y = int(20.0 * math.cos(2 * 3.14 * j / 150))
	        if i+offset_y < rows and j+offset_x < cols:
	            img_output[i,j] = img[(i+offset_y)%rows,(j+offset_x)%cols]
	        else:
	            img_output[i,j] = 0

	showImage(img_output, 'Multidirectional wave')

	#####################
	# Concave effect

	img_output = np.zeros(img.shape, dtype=img.dtype)

	for i in range(rows):
	    for j in range(cols):
	        offset_x = int(128.0 * math.sin(2 * 3.14 * i / (2*cols)))
	        offset_y = 0
	        if j+offset_x < cols:
	            img_output[i,j] = img[i,(j+offset_x)%cols]
	        else:
	            img_output[i,j] = 0


# Main function
def main():
	i = 1
	final_coords = []
	coordinates = []
	coordinates_x = []
	coordinates_y = []

	argparse(sys.argv[1:])
	outputDir = createOutputDir()
	templates = createTemplates()
	for root, dirs, files in os.walk(path_to_rz):
		for file_name in files:
			if file_name.endswith('.txt'):
				continue

			im_src = getSourceImage(file_name)

			pts_src = getSourcePoints(im_src)
			
			tmp = random.choice(templates)
			
			# Prints name of random chosen file from template files
			print(tmp)

			im_dst = getDestinationImage(tmp)

			pts_dst = getDestinationPoints(tmp, coordinates, coordinates_x, coordinates_y)
			
			im_out = createOutputImage(im_src, im_dst, pts_src, pts_dst, coordinates_x, coordinates_y)			

			final_coords = getFinalCoords(coordinates_x, coordinates_y)

			# Adding Gaussian blur added to output image
			blured_out = cv2.GaussianBlur(im_out,(5,5),0)
			createJson(file_name, final_coords, outputDir, i, True, False)

			# Applying motion blur on every second  outputimage
			#if (i % 2 == 0):
				# blured_out = applyMotionBlur(blured_out)
				# createJson(file_name, final_coords, outputDir, i, True, True)

			coordinates_x = []
			coordinates_y = []
			coordinates = []

			#Save image to output directory
			cv2.imwrite(outputDir+str(i)+'.jpg', blured_out)
			i += 1

main()