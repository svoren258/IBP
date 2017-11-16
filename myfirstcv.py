#!/usr/bin/python

import numpy as np
import io
import os
import random
import cv2
import re
import sys
import errno
from matplotlib import pyplot as plt
from PIL import Image


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


# img = cv2.imread('/home/svoren258/Dokumenty/myopencv/messi.jpg',0)
# plt.imshow(img, cmap = 'gray', interpolation = 'bicubic')
# plt.xticks([]), plt.yticks([])
# plt.show()

# cv2.imshow('image', img)
# k = cv2.waitKey(0) & 0xFF
# if k == 27:         # wait for ESC key to exit
#     cv2.destroyAllWindows() 
# elif k == ord('s'): # wait for 's' key to save and exit
#     cv2.imwrite('messigray.png',img)
#     cv2.destroyAllWindows()

# source = raw_input("Enter the path to scan:")
# os.chdir(source)

num_str = raw_input("pocet znaciek:")
num_int = int(num_str)
images = []
source = '/home/svoren258/Dokumenty/myopencv/characters/'
os.chdir(source)
for root, dirs, files in os.walk(source):
    for file_name in files:
        img = Image.open(os.path.join(root, file_name), 'r')
        images.append([img,file_name])

# filenames = ['0.png','1.png','2.png','3.png','4.png','5.png','6.png','7.png','8.png','9.png','A.png','B.png','C.png','D.png','E.png','F.png','H.png',
# 'I.png','J.png','K.png','L.png','M.png','N.png','P.png','R.png','S.png','T.png','U.png','V.png','X.png','Y.png','Z.png']
# for filename in filenames:
# 	char_img = Image.open(StringIO(filename), 'r')
# 	images.append(char_img)

# for imag in images:
# 	print imag

for i in range(num_int):
#char_img_w, char_img_h = char_img.size
	background = Image.open('/home/svoren258/Dokumenty/myopencv/vzor.png', 'r')
	#background = Image.new('RGBA', (1560, 330), (255, 255, 255, 255))
	#bg_w, bg_h = background.size
	stk_layout_img = Image.open('/home/svoren258/Dokumenty/myopencv/stk_ek2.png', 'r')
	stk_layout_offset = (681,53)
	background.paste(stk_layout_img, stk_layout_offset)

	if i % 2 == 0:
		stk_img = Image.open('/home/svoren258/Dokumenty/myopencv/stk.png','r')
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

	filename = "/home/svoren258/Dokumenty/myopencv/znacky/"
	if not os.path.exists(os.path.dirname(filename)):
	    try:
	        os.makedirs(os.path.dirname(filename))
	    except OSError as exc: # Guard against race condition
	        if exc.errno != errno.EEXIST:
	            raise

	background.save("/home/svoren258/Dokumenty/myopencv/znacky/znacka" + str(i) + ".png")