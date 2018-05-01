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
pl_spz = ''

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
				' 	(according to nationality shortcut - cz/sk/pl/h as third input argument) and saves them to output directiory,\n'
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
	global pl_spz
	character = random.choice(images)
	regex = r"([A-Z].png)"
	regex1 = r"([1-9].png)"
	regex2 = r"(A|B|C|E|H|J|K|L|M|P|S|T|U|Z.png)"
	regex3 = r"([0-9].png)"

	if (nation == 'cz'):
		if offset == (205,53) and not re.search(regex1, character[1]):
			character = generate_char(offset, images, nation)
			return character

		if offset == (358,53) and not re.search(regex2,character[1]):
			character = generate_char(offset, images, nation)
			
		for num_offset in [(511,53),(854,53),(1007,53),(1160,53),(1313,53)]:
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

	elif (nation == 'h'): # [(250,48),(460,48),(670,48),(990,48),(1170,48),(1350,48)]
		for num_offset in [(250,48),(460,48),(670,48),(260,48),(470,48),(680,48)]:
			if offset == num_offset and not re.search(regex,character[1]):
				character = generate_char(offset, images, nation)

		for num_offset in [(990,48),(1170,48),(1350,48),(1000,48),(1180,48),(1360,48)]:
			if offset == num_offset and  not re.search(regex3,character[1]):
				character = generate_char(offset, images, nation)

	return character

def return_char(type_of_char, images):
	numbers = r"([0-9].png)"
	notnull = r"([1-9].png)"
	letters = r"(A|C|E|F|G|H|J|K|L|M|N|P|R|S|T|U|W|X|Y.png)"
	char = random.choice(images)
	if (type_of_char == 'letter'):
		while (not re.search(letters, char[1])):
			char = random.choice(images)
	elif (type_of_char == 'number'):
		while (not re.search(numbers, char[1])):
			char = random.choice(images)
	elif (type_of_char == 'notnull'):
		while(not re.search(notnull, char[1])):
			char = random.choice(images)
	return char

# Function adds district shortcut in case of generating poland license number
def addDistrictPL(offset1, offset2, offset3, background, source):
	pl_shortcuts3 = ['ZSW','ZKA','ZPL','ZGL','ZLO','ZGY','ZKL','ZSL','ZKO','ZSZ','ZSD','ZDR','ZWA','ZCH','ZMY','ZPY','ZST',
					 'ZGR','GSL','GBY','GLE','GWE','GPU','GSP','GND','GMB','GSZ','GKW','GTC','GST','GDA','GCH','GCZ','GBY',
					 'GKS','NEB','NBR','NBA','NLI','NIL','NNM','NOS','NDZ','NOS','NOL','NNI','NSZ','NKE','NWE','NGO','NOE',
					 'NEL','NPI','NGI','NMR','BSU','BSE','BAU','BGR','BKL','BSK','BMN','BLM','BZA','BWM','FSD','FGW','FSU',
					 'FMI','FSL','FKR','FSW','FZA','FZG','FNW','FWS','PZL','PCT','PCH','PWA','POB','PSZ','PNT','POB','PWA',
					 'PGN','POZ','PGO','PWL','PKS','PSE','PSR','PWR','PSL','PKN','PKO','PLE','PGS','PJA','PKL','PTU','PKA',
					 'PPL','PRA','PKR','POS','POT','PKE','CSE','CTU','CSW','CBY','CNA','CGR','CWA','CBR','CRY','CZN','CMG',
					 'CAL','CWL','CRA','WZU','WML','WPZ','WOS','WSE','WCI','WMA','WGS','WPL','WPN','WPU','WWY','WOR','WSC',
					 'WND','WWL','WWE','WSK','WZY','WGM','WPR','WOT','WOT','WLS','WKZ','WBR','WPY','WSZ','WRA','WZW','LLU',
					 'LRY','LRA','LPA','LLB','LWL','LPU','LLE','LOP','LUB','LSW','LKR','LKS','LCH','LJA','LZA','LHR','LBL',
					 'LTM','DZG','DBL','DPL','DBL','DLB','DLE','DLU','DGL','DGR','DLW','DZL','DJA','DJE','DKA','DBA','DSR',
					 'DWL','DTR','DSR','DSW','DWR','DOL','DOA','DST','DZA','DKL','DDZ','ONA','OKL','OOL','OPO','ONY','OPR',
					 'OKR','OST','OGL','EKU','ELC','ELE','EPD','EZG','ESK','EBR','EZD','ELA','EPA','ELW','ETM','ERW','EOP',
					 'ERA','EPJ','EWE','EBE','TKN','TLW','TSK','TST','TOS','TOP','TSA','TSZ','TBU','TKA','TJE','SKL','SCZ',
					 'SLU','SMY','SZA','STA','SGL','SRS','SBE','SBE','SBL','SPS','SRB','SZO','SRC','SWD','SJZ','SZY','KOL',
					 'KRA','KCH','KOS','KWA','KSU','KPR','KMY','KNT','KBC','KTT','KNS','KGR','KNS','KTA','KDA','RTA','RST',
					 'RKL','RLE','RZE','RLA','RDE','RRS','RSR','RJS','RKR','RBR','RPZ','RJA','RLU','RPR','RSA','RLS']

	pl_shortcuts2 = ['BL','BS','CB','CG','CT','CW','DB','DJ','DL','DW',
					 'EL','EP','ES','FG','FZ','GA','GD','GS','KK','KR',
					 'KN','KT','LB','LC','LU','LZ','NE','NO','OP','OB',
					 'OK','PK','PL','PN','PO','PY','PP','PZ','RK','RP',
					 'RT','RZ','SB','SC','SD','SG','SJ','SK','SL','SM',
					 'SO','SR','ST','SW','SY','SZ','TK','WA','WB','WD',
					 'WE','WF','WJ','WK','WL','WN','WO','WT','WU','WP',
					 'WV','WS','WR','WW','WX','WY','WZ','ZK','ZS']
	

	if (offset3 == 0):
		rand = random.randint(0,78)
		background.paste(Image.open(source+'/'+pl_shortcuts2[rand][0]+'.png'),offset1)
		background.paste(Image.open(source+'/'+pl_shortcuts2[rand][1]+'.png'),offset2)
		return pl_shortcuts2[rand]
	
	else:
		rand = random.randint(0,287)
		background.paste(Image.open(source+'/'+pl_shortcuts3[rand][0]+'.png'),offset1)
		background.paste(Image.open(source+'/'+pl_shortcuts3[rand][1]+'.png'),offset2)
		background.paste(Image.open(source+'/'+pl_shortcuts3[rand][2]+'.png'),offset3)
		return pl_shortcuts3[rand]

# Function adds district shortcut in case of generating slovak license number
def addDistrictSK(offset1, offset2, background, source):
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
	background.paste(Image.open(source+'/'+sk_shortcuts[rand][0]+'.png'),offset1)
	background.paste(Image.open(source+'/'+sk_shortcuts[rand][1]+'.png'),offset2)
	return sk_shortcuts[rand]

def generate_pl_char(character, images, offset, background):
	global characters
	if (character == 'number'):
		number = return_char('number', images)
		background.paste(number[0], offset)
		characters += number[1][0]
	elif (character == 'letter'):
		letter = return_char('letter', images)
		background.paste(letter[0], offset)
		characters += letter[1][0]

	elif (character == 'notnull'):
		notnull = return_char('notnull', images)
		background.paste(notnull[0], offset)
		characters += notnull[1][0]

def createImagesArray(images, source):
	os.chdir(source)
	for root, dirs, files in os.walk(source):
	    for file_name in files:
	        img = Image.open(os.path.join(root, file_name), 'r')
	        images.append([img,file_name])

	return images

def carType(nation, source):
	if nation == 'h':
		if source == os.path.abspath('H/characters_e/'):
			return ' E-CAR or CNG'
		elif source == os.path.abspath('H/characters_taxi/'):
			return ' TAXI'
		elif source == os.path.abspath('H/characters_truck/'):
			return ' TRUCK'
		else:
			return ''
	else:
		return ''

# Main function
def main():
	global characters
	images = []
	argparse(sys.argv[1:])

	if (nation == 'sk'):
		source = os.path.abspath('SK/characters/')
	elif (nation == 'cz'):
		source = os.path.abspath('CZ/characters/')
	elif (nation == 'pl'):
		source = os.path.abspath('PL/characters/')
	elif (nation == 'h'):
		source = os.path.abspath('H/characters/')
	else:
		print('Wrong nationality shortcut inserted, try help for more information.')
		return


	for i in range(int(inputnum)):
		characters = ''
		if (nation == 'sk'):
			if (i != 0):
				os.chdir('../..')
			background = Image.open(os.path.abspath('SK/vzor_sk.png'),'r')
			sign_img = Image.open(os.path.abspath('SK/znak_vec.png'),'r')
			sign_img_offset = (524,100)
			background.paste(sign_img, sign_img_offset)
			offsets = [(683,40),(853,40),(1023,40),(1193,40),(1363,40)]
			characters += addDistrictSK((196,40), (366,40), background, source)
			images = createImagesArray(images, source)

		elif (nation == 'cz'):	
			if (i != 0):
				os.chdir('../../')
			background = Image.open(os.path.abspath('CZ/vzor_cz.png'),'r')
			stk_layout_img = Image.open(os.path.abspath('CZ/stk_ek.png'),'r')
			stk_layout_offset = (681,41)
			background.paste(stk_layout_img, stk_layout_offset)
			images = createImagesArray(images, source)

			# STK
			if i % 2 == 0:
				stk_img = Image.open(os.path.abspath('../stk.png'),'r')
				stk_offset = (693,63)
				background.paste(stk_img, stk_offset, stk_img)

			# EK
			if i % 4 == 0:
				ek_img = Image.open(os.path.abspath('../ek.png'),'r')
				ek_offset = (695,188)
				background.paste(ek_img, ek_offset, ek_img)

			offsets = [(205,53),(358,53),(511,53),(854,53),(1007,53),(1160,53),(1313,53)]


		elif (nation == 'h'):
			images = []
			if (i % 5 == 0):
				source = os.path.abspath('H/characters/')
				background = Image.open(os.path.abspath('H/vzor2_h.png'), 'r')
				dash_img = Image.open(os.path.abspath('H/-.png'), 'r')
				dash_offset = (890,150)
				offsets = [(260,48),(470,48),(680,48),(1000,48),(1180,48),(1360,48)]
				images = createImagesArray(images, source)
				
			elif (i % 5 == 1):
				# source1 = os.path.abspath('H/characters/')
				background = Image.open(os.path.abspath('../vzor3_h.png'), 'r')
				dash_img = Image.open(os.path.abspath('../-.png'), 'r')
				dash_offset = (880,150)
				offsets = [(250,48),(460,48),(670,48),(990,48),(1170,48),(1350,48)]
				images = createImagesArray(images, source)

			elif (i % 5 == 2):
				source = os.path.abspath('../../H/characters_taxi/')
				background = Image.open(os.path.abspath('../vzor4_h.png'), 'r')
				dash_img = Image.open(os.path.abspath('../-_taxi.png'), 'r')
				dash_offset = (880,150)
				offsets = [(250,48),(460,48),(670,48),(990,48),(1170,48),(1350,48)]
				images = createImagesArray(images, source)

			elif (i % 5 == 3):
				source = os.path.abspath('../../H/characters_truck/')
				background = Image.open(os.path.abspath('../vzor5_h.png'), 'r')
				dash_img = Image.open(os.path.abspath('../-_truck.png'),'r')
				dash_offset = (880,150)
				offsets = [(250,48),(460,48),(670,48),(990,48),(1170,48),(1350,48)]
				images = createImagesArray(images, source)

			elif (i % 5 == 4):
				source = os.path.abspath('../../H/characters_e/')
				background = Image.open(os.path.abspath('../vzor6_h.png'),'r')
				dash_img = Image.open(os.path.abspath('../-_e.png'), 'r')
				dash_offset = (880,150)
				offsets = [(250,48),(460,48),(670,48),(990,48),(1170,48),(1350,48)]
				images = createImagesArray(images, source)
				os.chdir('../../')
			background.paste(dash_img, dash_offset)

		elif (nation == 'pl'):
			images = createImagesArray(images, source)
			background = Image.open(os.path.abspath('../../PL/vzor_pl.png'),'r')
			if (i % 3 == 0):
				background.paste(Image.open(os.path.abspath('../../PL/znamka.png')),(545,135))
				characters += addDistrictPL((170,55),(348,55),0,background, source)
				offsets = [(635,55),(805,55),(985,55),(1155,55),(1330,55)]
				rand_num = random.randint(1,5)
				if (rand_num == 1):
					for offset in offsets:
						if (offset == (635,55)):
							generate_pl_char('notnull', images, offset, background)	
						else:
							generate_pl_char('number', images, offset, background)

				elif (rand_num == 2):
					for offset in offsets:
						if (offset == (635,55)):
							generate_pl_char('notnull', images, offset, background)	
						elif (offset == (805,55)):
							generate_pl_char('letter', images, offset, background)
						else:
							generate_pl_char('number', images, offset, background)

				elif (rand_num == 3):
					for offset in offsets: 
						if (offset == (635,55)):
							generate_pl_char('notnull', images, offset, background)	
						elif (offset == (1155,55) or offset == (1330,55)):
							generate_pl_char('letter', images, offset, background)
						else:
							generate_pl_char('number', images, offset, background)

				elif (rand_num == 4):
					for offset in offsets:
						if (offset == (635,55)):
							generate_pl_char('notnull', images, offset, background)	
						elif (offset == (1330,55)):
							generate_pl_char('letter', images, offset, background)
						else:
							generate_pl_char('number', images, offset, background)

				elif (rand_num == 5):
					for offset in offsets:
						if (offset == (635,55)):
							generate_pl_char('notnull', images, offset, background)	
						elif (offset == (805,55) or offset == (985,55)):
							generate_pl_char('letter', images, offset, background)
						else:
							generate_pl_char('number', images, offset, background)

			elif (i % 3 == 1):
				background.paste(Image.open(os.path.abspath('../../PL/znamka.png')),(715,135))
				characters += addDistrictPL((170,55),(348,55),(530,55),background, source)
				offsets = [(805,55),(980,55),(1155,55),(1330,55)]
				rand_num = random.randint(1,8)

				if (rand_num == 1):
					for offset in offsets:
						if (offset == (805,55)):
							generate_pl_char('letter', images, offset, background)
						else:
							generate_pl_char('number', images, offset, background)

				elif (rand_num == 2):
					for offset in offsets:
						if (offset == (805,55)):
							generate_pl_char('notnull', images, offset, background)	
						elif (offset == (1155,55) or offset == (1330,55)):
							generate_pl_char('letter', images, offset, background)
						else:
							generate_pl_char('number', images, offset, background)

				elif (rand_num == 3):
					for offset in offsets:
						if (offset == (805,55)):
							generate_pl_char('notnull', images, offset, background)	
						elif (offset == (978,55)):
							generate_pl_char('letter', images, offset, background)
						else:
							generate_pl_char('number', images, offset, background)

				elif (rand_num == 4):
					for offset in offsets:
						if (offset == (1330,55)):
							generate_pl_char('notnull', images, offset, background)	
						elif (offset == (1155,55)):
							generate_pl_char('letter', images, offset, background)
						else:
							generate_pl_char('number', images, offset, background)

				elif (rand_num == 5):
					for offset in offsets:
						if (offset == (978,55) or offset == (1155,55)):
							generate_pl_char('letter', images, offset, background)
						else:
							generate_pl_char('notnull', images, offset, background)

				elif (rand_num == 6):
					for offset in offsets:
						if (offset == (805,55) or offset == (978,55)):
							generate_pl_char('letter', images, offset, background)
						else:
							generate_pl_char('notnull', images, offset, background)

				elif (rand_num == 7):
					for offset in offsets:
						if (offset == (805,55) or offset ==  (1330,55)):
							generate_pl_char('letter', images, offset, background)
						else:
							generate_pl_char('notnull', images, offset, background)

				elif (rand_num == 8):
					for offset in offsets:
						if (offset == (978,55)):
							generate_pl_char('number', images, offset, background)
						else:
							generate_pl_char('notnull', images, offset, background)


			elif (i % 3 == 2):
				background.paste(Image.open(os.path.abspath('../../PL/znamka.png')),(640,135))
				characters += addDistrictPL((150,55),(315,55),(480,55),background, source)
				offsets = [(700,55),(870,55),(1040,55),(1205,55),(1370,55)]
				rand_num = random.randint(1,3)
				if (rand_num == 1):
					for offset in offsets:
						generate_pl_char('notnull', images, offset, background)

				elif (rand_num == 2):
					for offset in offsets:
						if (offset == (1370,55)):
							generate_pl_char('letter', images, offset, background)
						else:
							generate_pl_char('notnull', images, offset, background)

				elif (rand_num == 3):
					for offset in offsets:
						if (offset == (1205,55) or offset == (1370,55)):
							generate_pl_char('letter', images, offset, background)

						else:
							generate_pl_char('notnull', images, offset, background)

		if (nation == 'sk' or nation == 'cz' or nation =='h'):
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

		type_of_car = carType(nation, source)
		# Creating .txt file that includes to license-plate number 
		txtfile = open(textdir + 'rz' + str(i) + '.png.txt','w')
		txtfile.write(str(characters)+ ' ' + nation + type_of_car)
		txtfile.close()
		background.save(outputdir + 'rz' + str(i) + '.png')
main()
