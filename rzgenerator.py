#!/usr/bin/python
# -*- coding: utf-8 -*-

# Author: Ondrej Svoreň, 3 BIT
# Subject: IBP - Bachelor Thesis
# Thesis Name: Synthetic Dataset Generator for Traffic Analysis
# Supervisor: prof. Ing. Adam Herout PhD.
# School Year: 2017/18

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
nation = ''
characters = ''

# Argument parser
def argparse(argv):
	global inputnum
	global outputdir
	global nation
	try:
		opts, args = getopt.getopt(argv,"hi:o:t:")
	except getopt.GetoptError:
		print 'Usage: python rzgenerator.py -i [amount] -o [output_dir_path] -t [nationality_shortcut]'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print (
				'Usage: python rzgenerator.py -i [amount] -o [output_dir_path] -t [nationality_shortcut]\n'
				'	Application generates certain amount (first input argument) of czech or slovak license plates\n'
				' 	(according to nationality shortcut - cz/sk as third input argument) and saves them to output directiory,\n'
				'	which path is specified by second input argument argument (\'RZ/\' by default).'
				)
			sys.exit()
		elif opt in ("-i"):
			inputnum = arg
		elif opt in ("-o"):
			outputdir = arg
		elif opt in ("-t"):
			nation = arg

	print 'Amount: ', inputnum
	print 'Output directoty path: ', outputdir
	print 'Nationality shortcut: ', nation


# Function returns character according to czech or slovak license number rules 
def generate_char(offset, images, nation):
	character = random.choice(images)
	regex = r"([A-Z].png)"
	regex2 = r"(A|B|C|E|H|J|K|L|M|P|S|T|U|Z.png)"

	if (nation == 'cz'):
		if offset == (205,53) and character[1] == '0.png':
			character = generate_char(offset, images, nation)
			return character

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

# Function adds district shortcut in case of generating slovak license number
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

# Main function
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
			background = Image.open('/home/svoren258/Dokumenty/FIT_VUT/3_BIT/IBP/IBP/SK/vzor_sk.png', 'r')
			sign_img = Image.open('/home/svoren258/Dokumenty/FIT_VUT/3_BIT/IBP/IBP/SK/znak.png','r')
			sign_img_offset = (524,100)
			background.paste(sign_img, sign_img_offset)
			offsets = [(683,40),(853,40),(1023,40),(1193,40),(1363,40)]
			characters += addDistrict((196,40), (366,40), background, source)

		elif (nation == 'cz'):	
			background = Image.open('/home/svoren258/Dokumenty/FIT_VUT/3_BIT/IBP/IBP/CZ/vzor_cz.png', 'r')

			stk_layout_img = Image.open('/home/svoren258/Dokumenty/FIT_VUT/3_BIT/IBP/IBP/CZ/stk_ek.png', 'r')
			stk_layout_offset = (681,41) #(681,53)
			background.paste(stk_layout_img, stk_layout_offset)

			# STK
			if i % 2 == 0:
				stk_img = Image.open('/home/svoren258/Dokumenty/FIT_VUT/3_BIT/IBP/IBP/CZ/stk.png','r')
				stk_offset = (693,63) #(680,58)
				background.paste(stk_img, stk_offset, stk_img)

			# EK
			if i % 4 == 0:
				ek_img = Image.open('/home/svoren258/Dokumenty/FIT_VUT/3_BIT/IBP/IBP/CZ/ek.png','r')
				ek_offset = (695,188)
				background.paste(ek_img, ek_offset, ek_img)

			offsets = [(205,53),(358,53),(511,53),(854,53),(1007,53),(1160,53),(1313,53)]

		for offset in offsets:
			character = generate_char(offset, images, nation)
			characters += character[1][0]
			background.paste(character[0], offset)

		# Saving registration nubmer
		textdir = outputdir
		if not os.path.exists(os.path.dirname(textdir)):
		    try:
		        os.makedirs(os.path.dirname(textdir))
		    except OSError as exc: # Guard against race condition
		        if exc.errno != errno.EEXIST:
		            raise

		# Creating .txt file that includes to license-plate number 
		txtfile = open(textdir + 'rz' + str(i) + '.png.txt','w')
		txtfile.write(str(characters)+ ' ' + nation)
		txtfile.close()
		background.save(outputdir + 'rz' + str(i) + '.png')
main()
