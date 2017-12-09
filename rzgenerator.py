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
	background = Image.open('/home/svoren258/Dokumenty/FIT_VUT/3_BIT/IBP/IBP/vzory/vzor_final.png', 'r')
	#background = Image.new('RGBA', (1560, 330), (255, 255, 255, 255))
	#bg_w, bg_h = background.size
	stk_layout_img = Image.open('/home/svoren258/Dokumenty/FIT_VUT/3_BIT/IBP/IBP/vzory/stk_ek2.png', 'r')
	stk_layout_offset = (681,53)
	background.paste(stk_layout_img, stk_layout_offset)

	if i % 2 == 0:
		stk_img = Image.open('/home/svoren258/Dokumenty/FIT_VUT/3_BIT/IBP/IBP/vzory/stk.png','r')
		stk_offset = (680,70)
		background.paste(stk_img, stk_offset)

	offsets = [(205,53),(358,53),(511,53),(854,53),(1007,53),(1160,53),(1313,53)]

	# a_img = Image.open('/home/svoren258/Dokumenty/myopencv/characters/0.png','r')
	# for offset in offsets:
	# 	background.paste(a_img, offset)

	for offset in offsets:
		#print offset
		#character = random.choice(images)
		character = generate_char(offset, images)
		# print character[1]
		background.paste(character[0], offset)
	# background.save('out.png')
	filename = outputdir
	if not os.path.exists(os.path.dirname(filename)):
	    try:
	        os.makedirs(os.path.dirname(filename))
	    except OSError as exc: # Guard against race condition
	        if exc.errno != errno.EEXIST:
	            raise
	# else:
	# 	shutil.rmtree(outputdir)
	# 	os.makedirs(os.path.dirname(outputdir))

	# filename = "/home/svoren258/Dokumenty/FIT_VUT/3_BIT/IBP/IBP/znacky"

	background.save(outputdir + "rz" + str(i) + ".png")