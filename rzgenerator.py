#!/usr/bin/python

import numpy as np
import io
import os
import random
import cv2
import shutil
import re
import sys, getopt
import errno
from matplotlib import pyplot as plt
from PIL import Image

inputnum = 0
outputdir = '../RZ/'
#characters = []
characters = ''

def argparse(argv):
	global inputnum
	global outputdir
	try:
		opts, args = getopt.getopt(argv,"hi:o:")
	except getopt.GetoptError:
		print 'Usage: python rzgenerator.py -i [number] -o [output_dir_path]'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'Usage: python rzgenerator.py -i [number] -o [output_dir_path]'
			sys.exit()
		elif opt in ("-i"):
			inputnum = arg
		elif opt in ("-o"):
			outputdir = arg

	print 'Input num is: ', inputnum
	print 'Output dir is: ', outputdir

argparse(sys.argv[1:])

# print(inputnum)

#function definitions
def generate_char(offset, images):
	character = random.choice(images)
	
	regex = r"([A-Z].png)"
	# if offset == (185, 20) and re.search(regex,character[1]):
	# 	character = generate_char(offset, images)

	# else:
	if offset == (358,53) and not re.search(regex,character[1]):
		character = generate_char(offset, images)
		
	for num_offset in [(205,53),(854,53),(1007,53),(1160,53),(1313,53)]:
		if offset == num_offset and re.search(regex,character[1]):
			character = generate_char(offset, images)
			break
	
	return character

# source = inputnum
# os.chdir(source)

# num_str = raw_input("pocet znaciek:")
# num_int = int(num_str)
images = []
source = '/home/svoren258/Dokumenty/FIT_VUT/3_BIT/IBP/IBP/characters/'
os.chdir(source)
for root, dirs, files in os.walk(source):
    for file_name in files:
        img = Image.open(os.path.join(root, file_name), 'r')
        images.append([img,file_name])


for i in range(int(inputnum)):
#char_img_w, char_img_h = char_img.size
	background = Image.open('/home/svoren258/Dokumenty/FIT_VUT/3_BIT/IBP/IBP/vzory/vzor_new.png', 'r')
	#background = Image.new('RGBA', (1560, 330), (255, 255, 255, 255))
	#bg_w, bg_h = background.size
	stk_layout_img = Image.open('/home/svoren258/Dokumenty/FIT_VUT/3_BIT/IBP/IBP/vzory/stk_ek2.png', 'r')
	stk_layout_offset = (681,53)
	background.paste(stk_layout_img, stk_layout_offset)

	#STK
	# if i % 2 == 0:
	# 	stk_img = Image.open('/home/svoren258/Dokumenty/FIT_VUT/3_BIT/IBP/IBP/vzory/stk.png','r')
	# 	stk_offset = (680,70)
	# 	background.paste(stk_img, stk_offset)

	offsets = [(205,53),(358,53),(511,53),(854,53),(1007,53),(1160,53),(1313,53)]

	# a_img = Image.open('/home/svoren258/Dokumenty/myopencv/characters/0.png','r')
	# for offset in offsets:
	# 	background.paste(a_img, offset)

	for offset in offsets:
		#print offset
		#character = random.choice(images)
		character = generate_char(offset, images)
		#characters.append(character[1][0])
		characters += character[1][0]
		#print character[1][0]
		background.paste(character[0], offset)
	# background.save('out.png')

	#Saving registration nubmer
	textdir = outputdir
	if not os.path.exists(os.path.dirname(textdir)):
	    try:
	        os.makedirs(os.path.dirname(textdir))
	    except OSError as exc: # Guard against race condition
	        if exc.errno != errno.EEXIST:
	            raise

	txtfile = open(textdir + 'rz' + str(i) + '.png.txt','w')
	txtfile.write(str(characters))
	txtfile.close()
	#characters = []
	characters = ''

	#Creating output directory
	# filename = outputdir
	# if not os.path.exists(os.path.dirname(filename)):
	#     try:
	#         os.makedirs(os.path.dirname(filename))
	#     except OSError as exc: # Guard against race condition
	#         if exc.errno != errno.EEXIST:
	#             raise
	# else:
	# 	shutil.rmtree(outputdir)
	# 	os.makedirs(os.path.dirname(outputdir))

	# filename = "/home/svoren258/Dokumenty/FIT_VUT/3_BIT/IBP/IBP/znacky"

	#image_data = np.asarray( background.getdata(), dtype='uint8' )

	#image_data = np.array(background.getdata(), np.uint8).reshape(background.size[0], background.size[1], 3)

	#image_data = np.asarray(background.getdata(), np.uint8)

	# img_data = background.convert('L')
	# print img_data
	# image_data = np.array(img_data)
	# print background.size
	# print image_data.size
	# shape = image_data.shape
	# print shape
	# cv2.imshow('image',image_data)
	# cv2.waitKey(20)

	background.save(outputdir + 'rz' + str(i) + '.png')

	###### OpenCV ######
	#image = cv2.imread(outputdir + 'rz' + str(i) + '.png',1)

	#cv2.imwrite(textdir + 'rz' + str(i) + '.png', image)
	#print image.shape
	
	#print type(image)
	
	#image_data = np.asarray(background)
	#print type(image_data)

	# (B, G, R) = cv2.split(image)

	# R[R == 0] = 50
	# G[G == 0] = 50
	# B[B == 0] = 50

	# R[R == 255] = 200 
 	# G[G == 255] = 200
 	# B[B == 255] = 200

	# #merge the channels back together and return the image
	# image = cv2.merge([B, G, R])

	# dst = cv2.fastNlMeansDenoisingColored(image,None,10,10,7,21)
	# blur = cv2.GaussianBlur(dst,(5,5),0)

	# cv2.imwrite(textdir + 'rz' + str(i) + '.png', blur)

	#cv2.imwrite(textdir + 'rz' + str(i) + '.png', image)

	# row,col,ch = dst.shape
	# s_vs_p = 0.5
	# amount = 0.004
	# out = np.copy(dst)
	# # Salt mode
	# num_salt = np.ceil(amount * dst.size * s_vs_p)
	# coords = [np.random.randint(0, j - 1, int(num_salt))
	#       for j in dst.shape]
	# out[coords] = 1

	# # Pepper mode
	# num_pepper = np.ceil(amount* dst.size * (1. - s_vs_p))
	# coords = [np.random.randint(0, j - 1, int(num_pepper))
	#       for j in dst.shape]
	# out[coords] = 0


	#cv2.imshow('out',out)
	# row,col,ch = dst.shape
	# gauss = np.random.randn(row,col,ch)
	# gauss = gauss.reshape(row,col,ch)        
	# noisy = dst + dst * gauss
	# cv2.imshow('noisy',noisy)
	#median = cv2.medianBlur(image,9)
	#cv2.imshow('bgr',out)

	# cv2.imwrite(textdir + 'rz' + str(i) + '.png', dst)

	#Averaging
	# kernel = np.ones((5,5),np.float32)/25
	# dst = cv2.filter2D(image,-1,kernel)
	# cv2.imshow('dst',dst)
	# m = (0,0,0) 
	# s = (0,0,0)
	# cv2.randn(image,m,s)

	#Denoising
	# dst = cv2.fastNlMeansDenoisingColored(image,None,10,10,7,21)
	# cv2.imshow('image',dst)

	#cv2.imshow('image',image)
	# blur = cv2.bilateralFilter(image,9,75,75)
	# cv2.imshow('blur',blur)
	
	#Only coloured object
	# median = cv2.medianBlur(image,9)
	# cv2.imshow('median',median)

	# noise_sigma = 35
	# temp_image = np.float64(np.copy(image))

	# h = temp_image.shape[0]
	# w = temp_image.shape[1]
	# noise = np.random.randn(h, w) * noise_sigma

	# noisy_image = np.zeros(temp_image.shape, np.float64)
	# if len(temp_image.shape) == 2:
	# 	noisy_image = temp_image + noise
	# else:
	# 	noisy_image[:,:,0] = temp_image[:,:,0] + noise
	# 	noisy_image[:,:,1] = temp_image[:,:,1] + noise
	# 	noisy_image[:,:,2] = temp_image[:,:,2] + noise

	# cv2.imshow('noisy image',noisy_image)

	#GAUSSIAN NOISE
	# row,col,ch= image.shape
	# mean = 0
	# var = 0.1
	# sigma = var**0.5
	# gauss = np.random.normal(mean,sigma,(row,col,ch))
	# gauss = gauss.reshape(row,col,ch)
	# noisy = image + gauss
	# cv2.imshow('noisy', noisy)

	#SPECKLE
	# row,col,ch = image.shape
	# gauss = np.random.randn(row,col,ch)
	# gauss = gauss.reshape(row,col,ch)        
	# noisy = image + image * gauss
	# cv2.imshow('noisy',noisy)

	#S&P
	# row,col,ch = image.shape
	# s_vs_p = 0.5
	# amount = 0.004
	# out = np.copy(image)
	# # Salt mode
	# num_salt = np.ceil(amount * image.size * s_vs_p)
	# coords = [np.random.randint(0, i - 1, int(num_salt))
	#       for i in image.shape]
	# out[coords] = 1

	# # Pepper mode
	# num_pepper = np.ceil(amount* image.size * (1. - s_vs_p))
	# coords = [np.random.randint(0, i - 1, int(num_pepper))
	#       for i in image.shape]
	# out[coords] = 0
	# cv2.imshow('out',out)
	
	# cv2.waitKey(0)