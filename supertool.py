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
import json
from matplotlib import pyplot as plt
from PIL import Image

# coordinates_x = []
# coordinates_y = []
# path_to_dst = ''
# path_to_src = ''

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
		print ('Usage: python supertool.py -t [path_to_tmp] -r [path_to_rz] -o [path_to_output]')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print ('Usage: python supertool.py -t [path_to_tmp] -r [path_to_rz] -o [path_to_output]')
			sys.exit()
		elif opt in ('-t'):
			path_to_tmp = arg
		elif opt in ('-r'):
			path_to_rz = arg
		elif opt in ('-o'):
			path_to_output = arg

	print ('Path to templates: ', path_to_tmp)
	print ('Path to rz: ', path_to_rz)
	print ('Path to output: ', path_to_output)

def showImage(image, name='img'):
	cv2.imshow(name,image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

# gaussian noise applying function
def add_gaussian_noise(image_in):
	noise_sigma = 15
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

	return noisy_image


def rgbChangeVal(min, max, image):
    #According to Black (minimum) and White (maximum) value of original registration number change values of channels in synthetic registration number
    #(B, G, R) = cv2.split(image)

    # for x in range(0,50):
       #  R[R == x] = min
       #  G[G == x] = min
       #  B[B == x] = min

	(B, G, R) = cv2.split(image)
	R[R == 0] = min
	G[G == 0] = min
	B[B == 0] = min	    
	R[R == 255] = max
	G[G == 255] = max
	B[B == 255] = max

	# merge the channels back together and return the image
	image = cv2.merge([B, G, R])
	return image
    
    

def createOutputDir():
	filename = path_to_output
	if not os.path.exists(os.path.dirname(filename)):
	    try:
	        os.makedirs(os.path.dirname(filename))
	    except OSError as exc: # Guard against race condition
	        if exc.errno != errno.EEXIST:
	            raise

	return filename

def createTemplates():
	my_filenames = []
	for root, dirs, files in os.walk(path_to_tmp):
		for tmp_name in files:
			if tmp_name.endswith('.txt'):
				continue
			my_filenames.append(tmp_name)
			#my_filenames = sorted(my_filenames)
	return my_filenames

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

def createJson(file_name, coordinates, outputDir, i):
	#open txt file with registration number and add max and min x and y coordinates and save in final directory as 00x.jpg.txt
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
		'point3' : coordinates[3]
	}

	json_string = json.dumps(data, sort_keys=True)
	json_file = open(outputDir+str(i)+'.jpg.json','w')
	json_file.write(json_string)
	json_file.close()

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

def createOutputImage(im_src, im_dst, pts_src, pts_dst, coordinates_x, coordinates_y):

	# Find homography
	h, status = cv2.findHomography(pts_src, pts_dst)

	# Warp source image
	#im_temp = cv2.warpPerspective(im_src, h, (im_dst.shape[1],im_dst.shape[0]), cv2.INTER_LINEAR)
	im_temp = cv2.warpPerspective(im_src, h, (im_dst.shape[1],im_dst.shape[0]), cv2.INTER_LINEAR)#, borderMode=cv2.BORDER_TRANSPARENT)
	

	# Get Perspective transformation matrix
	# pts_dst_array = np.array([[358,253],[674,348],[660,400],[363,307]],np.float32)
	# pts_src_array = np.array([[0,0],[1559,0],[1559,329],[0,329]],np.float32)

	# Another function to findHomography()
	#perspectiveMatrix = cv2.getPerspectiveTransform(pts_src_array, pts_dst_array)
	
	# print perspectiveMatrix
	# im_perspective = cv2.warpPerspective(im_src, perspectiveMatrix, (im_dst.shape[1],im_dst.shape[0]), flags=cv2.INTER_LINEAR)
	#showImage(im_perspective)

	# Black out polygonal area in destination image.
	cv2.fillConvexPoly(im_dst, pts_dst.astype(int), 0, 16)

	# ANTIALIASING to im_temp

	#showImage(im_temp, 'temp1')

	#showImage(im_dst)

	# Add warped source image to destination image.
	im_out = im_dst + im_temp

	#im_out = cv2.resize(im_out, (0,0), fx=0.75, fy=0.75, interpolation = cv2.INTER_AREA)
	#im_out = cv2.resize(im_out, (0,0), fx=0.75, fy=0.75, interpolation = cv2.INTER_LINEAR)
	#im_out = cv2.resize(im_out, (0,0), fx=0.75, fy=0.75, interpolation = cv2.INTER_CUBIC)

	#showImage(im_out,'im_out')
	#showImage(im_out_linear,'im_linear')
	#showImage(im_out_cubic,'im_cubic')

	return im_out
	#Resize image to wanted size
	#output_img = im_out[int(0.8*min(coordinates_y)):int(1.2*max(coordinates_y)), int(0.8*min(coordinates_x)):int(1.2*max(coordinates_x))]
	#im_out = im_out[int(0.75*0.8*min(coordinates_y)):int(0.75*1.2*max(coordinates_y)), int(0.75*0.8*min(coordinates_x)):int(0.75*1.2*max(coordinates_x))]
	
	#return output_img

def getDestinationImage(tmp):
	im_dst = cv2.imread(path_to_tmp+tmp,1)
	im_dst = cv2.resize(im_dst, (0,0), fx=0.25, fy=0.25, interpolation = cv2.INTER_AREA)
	return im_dst

def getSourceImage(file_name):

	im_src = cv2.imread(path_to_rz+file_name,1)
	im_hsv = cv2.cvtColor(im_src, cv2.COLOR_BGR2HSV)

	# Brightness and contrast changing	
	for x in range(0, len(im_hsv)):
		for y in range(0, len(im_hsv[0])):
			im_hsv[x,y][2] *= 0.675

	im_src = cv2.cvtColor(im_hsv, cv2.COLOR_HSV2BGR)

	# showImage(im_src, "img")

	# print height, width, channels

	# Changing RGB channel maximum and minimum value
	# im_src = rgbChangeVal(50,200,im_src)

	#showImage(im_src,'src')
	#showImage(im_src)
  
	#dst = cv2.fastNlMeansDenoisingColored(im_src,None,10,10,7,21)
	#im_src = cv2.fastNlMeansDenoisingColored(im_src,None,10,10,7,21)
	#im_src = cv2.GaussianBlur(dst,(5,5),0)

	#GAUSSIAN NOISE
	# row,col,ch = im_src.shape
	# mean = 0
	# var = 0.1
	# sigma = var**0.5
	# gauss = np.random.normal(mean,sigma,(row,col,ch))
	# gauss = gauss.reshape(row,col,ch)
	# im_src = im_src + gauss
	###########################################################

	#Histogram 
	# color = ('b','g','r')
	# for j,col in enumerate(color):
	# 	histr = cv2.calcHist([im_rgb],[j],None,[256],[0,256])
	# 	plt.plot(histr,color = col)
	# 	plt.xlim([0,256])
	# plt.show()
	############

	# pts_dst = np.vstack(points).astype(float)

	# Resize registration number to apply antialiasing
	im_src = cv2.resize(im_src, (0,0), fx=0.375, fy=0.375, interpolation = cv2.INTER_AREA)

	# showImage(im_src, 'src')

	im_src = cv2.fastNlMeansDenoisingColored(im_src,None,8,8,7,21)

	# showImage(im_src, 'src')

    #Application of Gaussian noise
	im_src = add_gaussian_noise(im_src)

	# showImage(im_src, "image")
	return im_src

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

def main():
	i = 1
	final_coords = []
	coordinates = []
	coordinates_x = []
	coordinates_y = []

	argparse(sys.argv[1:])
	outputDir = createOutputDir()
	templates = createTemplates()
	#i = 0
	for root, dirs, files in os.walk(path_to_rz):
		for file_name in files:
			if file_name.endswith('.txt'):
				continue

			# #PIL version
			# tmp = random.choice(my_filenames)
			# im = Image.open(path_to_tmp+tmp)
			# hist = Image.histogram(im)
			# print hist
			############
			im_src = getSourceImage(file_name)

			#showImage(im_src,'src')

			pts_src = getSourcePoints(im_src)

			tmp = random.choice(templates)
			#tmp = '047.jpg'
			print(tmp)

			#i += 1
			im_dst = getDestinationImage(tmp)


			pts_dst = getDestinationPoints(tmp, coordinates, coordinates_x, coordinates_y)
			
			#print coordinates
			
			#Changing the RGB channel values according to the intensity of grayscale image
			#The area, we are looking for in original image		
			# im_rgb = im_dst[int(min(coordinates_y)):int(max(coordinates_y)), int(min(coordinates_x)):int(max(coordinates_x))]

			# # the area of the image with the largest intensity value
			# gray = cv2.cvtColor(im_rgb, cv2.COLOR_BGR2GRAY)
			# (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)

			# # black and white values, 10% from smallest and greatest value (minVal, maxVal)
			# interval = (maxVal - minVal)
			# percentil = int(interval / 10)
			# white_num = minVal + percentil
			# black_num = maxVal - percentil

			#HSV - hue, saturation, value
			# x = cv2.merge([np.uint8([90]), np.uint8([90]), np.uint8([90])])
			# res = cv2.add(im_src,x)

			# hsv = cv2.cvtColor(im_src, cv2.COLOR_BGR2HSV)
			# showImage(hsv)
			# h, s, v = cv2.split(hsv)
			# v -= 50
			# darker = cv2.merge((h, s, v))
			# # #back to RGB
			# res = cv2.cvtColor(darker, cv2.COLOR_HSV2BGR)
			# showImage(res)

			# height, width = im_src.shape[:2]
			# print(height, width)
			# for y in range(0,height-1):
			# 	for x in range(0,width-1):
			# 		im_src[y,x] -= 150
			# showImage(im_src)
			#showImage(im_src)

			#########################################################
			
			im_out = createOutputImage(im_src, im_dst, pts_src, pts_dst, coordinates_x, coordinates_y)			

			final_coords = getFinalCoords(coordinates_x, coordinates_y)
			#showImage(im_out)
			# textdir = path_to_rz
			# if not os.path.exists(os.path.dirname(textdir)):
			#     try:
			#         os.makedirs(os.path.dirname(textdir))
			#     except OSError as exc: # Guard against race condition
			#         if exc.errno != errno.EEXIST:
			#             raise
			
			#Antialiasing
			#im_out = cv2.resize(im_out, (0,0), fx=1.0, fy=1.0, interpolation = cv2.INTER_AREA)

			#Antialiasing/Gaussian blur added to whole image
			blured_out = cv2.GaussianBlur(im_out,(5,5),0)

			createJson(file_name, final_coords, outputDir, i)

			coordinates_x = []
			coordinates_y = []
			coordinates = []

			#Save image to wanted directory
			#cv2.imwrite(filename+str(i)+'.jpg',im_out)
			cv2.imwrite(outputDir+str(i)+'.jpg',blured_out)

			i += 1
			#PIL variant of ANTIALIASING
			# im = Image.open(filename+str(i)+'.jpg')
			# width,height = im.size
			# out = im.resize((width, height), Image.ANTIALIAS)
			# out.save(filename+str(i)+'_PIL'+'.jpg', quality=100)
main()

############################################################################################################


# for root, dirs, files in os.walk(path_to_tmp):
# 	for file_name in files:
# 		if file_name.endswith('.txt'):
# 			continue
# 		my_filenames.append(file_name)
# 		my_filenames = sorted(my_filenames)

# for file_name in my_filenames:
# 	coordinates_x = []
# 	coordinates_y = []
# 	i += 1
# 	print file_name
# 	file = open(path_to_tmp+file_name+'.txt','r')
# 	#print file.read()
# 	points = file.read()
# 	#print points
# 	points = ast.literal_eval(points)
# 	# print points
# 	for point in points:
# 		coordinates_x.append(point[0])
# 		coordinates_y.append(point[1])
# 	# print coordinates_x
# 	# print coordinates_y
	
# 	pts_dst = np.vstack(points).astype(float)
# 	#print pts_dst
# 	# for root, dirs, reg_nums in os.walk(path_to_rz):
# 	# 	for regnum_name in reg_nums:
# 	# 		print regnum_name

# 	im_dst = cv2.imread('templates/'+file_name,1)

# 	im_dst = cv2.resize(im_dst, (0,0), fx=0.25, fy=0.25)

# 	rz = random.choice(os.listdir(path_to_rz))

# 	im_src = cv2.imread(path_to_rz+rz,1)

# 	size = im_src.shape

# 	# Create a vector of source points.
# 	pts_src = np.array(
# 	                   [
# 	                    [0,0],
# 	                    [size[1] - 1, 0],
# 	                    [size[1] - 1, size[0] -1],
# 	                    [0, size[0] - 1 ]
# 	                    ],dtype=float
# 	                   );

# 	# Calculate Homography between source and destination points
# 	h, status = cv2.findHomography(pts_src, pts_dst);

# 	# Warp source image
# 	im_temp = cv2.warpPerspective(im_src, h, (im_dst.shape[1],im_dst.shape[0]))

# 	# Black out polygonal area in destination image.
# 	cv2.fillConvexPoly(im_dst, pts_dst.astype(int), 0, 16)

# 	# Add warped source image to destination image.
# 	im_out = im_dst + im_temp

# 	#Resize image to wanted size
# 	im_out = im_out[int(0.8*min(coordinates_y)):int(1.2*max(coordinates_y)), int(0.8*min(coordinates_x)):int(1.2*max(coordinates_x))]

# 	textdir = 'RZTXT/'
# 	if not os.path.exists(os.path.dirname(textdir)):
# 	    try:
# 	        os.makedirs(os.path.dirname(textdir))
# 	    except OSError as exc: # Guard against race condition
# 	        if exc.errno != errno.EEXIST:
# 	            raise

# 	#open txt file with registration number and add max and min x and y coordinates and save in final directory as 00x.jpg.txt
# 	txtfile = open(textdir + rz + '.txt','r')
# 	reg_num = txtfile.readline()
# 	txtfile.close()

# 	data = {
# 		'string' : reg_num,
# 		'max X' : max(coordinates_x),
# 		'min X' : min(coordinates_x),
# 		'max Y' : max(coordinates_y),
# 		'min Y' : min(coordinates_y)
# 	}

# 	json_string = json.dumps(data, sort_keys=True)
# 	json_file = open(filename+str(i)+'.jpg.json','w')
# 	json_file.write(json_string)
# 	json_file.close()

# 	#Save image to wanted directory
# 	cv2.imwrite(filename+str(i)+'.jpg',im_out)