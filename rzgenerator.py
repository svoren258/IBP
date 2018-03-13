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
outputdir = '../../RZ/'
#characters = []
nation = ''
characters = ''

def argparse(argv):
	global inputnum
	global outputdir
	global nation
	try:
		opts, args = getopt.getopt(argv,"hi:o:t:")
	except getopt.GetoptError:
		print 'Usage: python rzgenerator.py -i [number] -o [output_dir_path] -t [nation]'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'Usage: python rzgenerator.py -i [number] -o [output_dir_path] -t [nation]'
			sys.exit()
		elif opt in ("-i"):
			inputnum = arg
		elif opt in ("-o"):
			outputdir = arg
		elif opt in ("-t"):
			nation = arg

	print 'Input num is: ', inputnum
	print 'Output dir is: ', outputdir
	print 'Nation: ', nation


#function definitions
def generate_char(offset, images, nation):
	character = random.choice(images)
	regex = r"([A-Z].png)"
	regex2 = r"(A|B|C|E|H|J|K|L|M|P|S|T|U|Z.png)"

	if (nation == 'cz'):
		if offset == (205,53) and character[1] == '0.png':
			character = generate_char(offset, images, nation)
			return character
		
		# if offset == (185, 20) and re.search(regex,character[1]):
		# 	character = generate_char(offset, images)

		# else:
		if offset == (358,53) and not re.search(regex2,character[1]):
			character = generate_char(offset, images, nation)
			
		for num_offset in [(205,53),(854,53),(1007,53),(1160,53),(1313,53)]:
			if offset == num_offset and re.search(regex,character[1]):
				character = generate_char(offset, images, nation)
				break
	
	elif (nation == 'sk'):
		for num_offset in [(683,40),(853,40),(1023,40)]:
			if offset == num_offset and re.search(regex,character[1]):
				character = generate_char(offset, images, nation)

		for num_offset in [(1193,40),(1363,40)]:
			if offset == num_offset and not re.search(regex,character[1]):
				character = generate_char(offset, images, nation)

	return character

def addDistrict(offset1, offset2, background, source):
	sk_shortcuts = ['BA','BL','BB','BJ','BN','BR',
					'BS','BY','CA','DK','DS','DT',
					'GA','GL','HC','HE','IL','KA',
					'KE','KK','KM','KN','KS','LC',
					'LE','LM','LV','MA','MI','ML',
					'MT','MY','NR','NM','NO','NZ',
					'PB','PD','PE','PK','PN','PO',
					'PP','PT','PU','RA','RK','RS',
					'RV','SA','SB','SC','SE','SI',
					'SK','SL','SN','SO','SP','SV',
					'TT','TN','TO','TR','TS','TV',
					'VK','VT','ZA','ZC','ZH','ZM','ZV']

	rand = random.randint(0,72)
	background.paste(Image.open(source+sk_shortcuts[rand][0]+'.png'),offset1)
	background.paste(Image.open(source+sk_shortcuts[rand][1]+'.png'),offset2)
	return sk_shortcuts[rand]

def main():
	images = []
	argparse(sys.argv[1:])

	if (nation == 'sk'):
		source = '/home/svoren258/Dokumenty/FIT_VUT/3_BIT/IBP/IBP/SK/characters/'
	elif (nation == 'cz'):
		source = '/home/svoren258/Dokumenty/FIT_VUT/3_BIT/IBP/IBP/CZ/characters/'

	os.chdir(source)
	for root, dirs, files in os.walk(source):
	    for file_name in files:
	        img = Image.open(os.path.join(root, file_name), 'r')
	        images.append([img,file_name])


	for i in range(int(inputnum)):
		characters = ''
		if (nation == 'sk'):
			background = Image.open('/home/svoren258/Dokumenty/FIT_VUT/3_BIT/IBP/IBP/SK/vzor_final4.png', 'r')
			sign_img = Image.open('/home/svoren258/Dokumenty/FIT_VUT/3_BIT/IBP/IBP/SK/znak.png','r')
			sign_img_offset = (524,100)
			background.paste(sign_img, sign_img_offset)
			offsets = [(683,40),(853,40),(1023,40),(1193,40),(1363,40)]
			characters += addDistrict((196,40), (366,40), background, source)

		elif (nation == 'cz'):	
			background = Image.open('/home/svoren258/Dokumenty/FIT_VUT/3_BIT/IBP/IBP/CZ/vzor_new3.png', 'r')
		#background = Image.new('RGBA', (1560, 330), (255, 255, 255, 255))
		#bg_w, bg_h = background.size

			stk_layout_img = Image.open('/home/svoren258/Dokumenty/FIT_VUT/3_BIT/IBP/IBP/CZ/stk_ek7.png', 'r')
			stk_layout_offset = (681,41) #(681,53)
			background.paste(stk_layout_img, stk_layout_offset)

			#STK
			if i % 2 == 0:
				stk_img = Image.open('/home/svoren258/Dokumenty/FIT_VUT/3_BIT/IBP/IBP/CZ/stk7.png','r')
				stk_offset = (693,63) #(680,58)
				background.paste(stk_img, stk_offset, stk_img)

			#EK
			if i % 4 == 0:
				ek_img = Image.open('/home/svoren258/Dokumenty/FIT_VUT/3_BIT/IBP/IBP/CZ/ek.png','r')
				ek_offset = (695,188)
				background.paste(ek_img, ek_offset, ek_img)

			offsets = [(205,53),(358,53),(511,53),(854,53),(1007,53),(1160,53),(1313,53)]

		# a_img = Image.open('/home/svoren258/Dokumenty/myopencv/characters/0.png','r')
		# for offset in offsets:
		# 	background.paste(a_img, offset)

		# for offset in offsets:
		# 	if offset == (205,53):
		# 		char = Image.open('/home/svoren258/Dokumenty/FIT_VUT/3_BIT/IBP/IBP/characters/D.png', 'r')
		# 		background.paste(char, offset)
		# 	elif offset == (358,53):
		# 		char = Image.open('/home/svoren258/Dokumenty/FIT_VUT/3_BIT/IBP/IBP/characters/A.png', 'r')
		# 		background.paste(char, offset)
		# 	elif offset == (511,53):
		# 		char = Image.open('/home/svoren258/Dokumenty/FIT_VUT/3_BIT/IBP/IBP/characters/K.png', 'r')
		# 		background.paste(char, offset)
		# 	elif offset == (854,53):
		# 		char = Image.open('/home/svoren258/Dokumenty/FIT_VUT/3_BIT/IBP/IBP/characters/U.png', 'r')
		# 		background.paste(char, offset)
		# 	elif offset == (1007,53):
		# 		char = Image.open('/home/svoren258/Dokumenty/FIT_VUT/3_BIT/IBP/IBP/characters/J.png', 'r')
		# 		background.paste(char, offset)
		# 	elif offset == (1160,53):
		# 		char = Image.open('/home/svoren258/Dokumenty/FIT_VUT/3_BIT/IBP/IBP/characters/E.png', 'r')
		# 		background.paste(char, offset)
		# 	elif offset == (1313,53):
		# 		char = Image.open('/home/svoren258/Dokumenty/FIT_VUT/3_BIT/IBP/IBP/characters/M.png', 'r')
		# 		background.paste(char, offset)

		for offset in offsets:
			#print offset
			#character = random.choice(images)
			character = generate_char(offset, images, nation)

			#characters.append(character[1][0])
			characters += character[1][0]
			#print character[1][0]
			background.paste(character[0], offset)

		#Saving registration nubmer
		textdir = outputdir
		if not os.path.exists(os.path.dirname(textdir)):
		    try:
		        os.makedirs(os.path.dirname(textdir))
		    except OSError as exc: # Guard against race condition
		        if exc.errno != errno.EEXIST:
		            raise

		txtfile = open(textdir + 'rz' + str(i) + '.png.txt','w')
		txtfile.write(str(characters)+ ' ' + nation)
		txtfile.close()
		background.save(outputdir + 'rz' + str(i) + '.png')
main()
