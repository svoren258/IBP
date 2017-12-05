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

coordinates_x = []
coordinates_y = []

def mouse_handler(event, x, y, flags, data) :
    global coordinates_y, coordinates_x
    if event == cv2.EVENT_LBUTTONDOWN :
    	if len(data['points']) < 4 :
	        img_copy = data['im'].copy()
	        cv2.circle(data['im'], (x,y),1, (0,0,255), 5, 16);
	        cv2.imshow("Image", data['im']);
	        ix,iy = x, y
	        while(1):
	        	k = cv2.waitKey(20) & 0xFF
	        	if k == ord('a'):
	        		data['im'] = img_copy.copy()
	        		cv2.circle(data['im'], (ix-1,iy),1, (0,0,255), 5, 16)
	        		ix = ix-1
	       			cv2.imshow("Image", data['im'])
	       			continue
	       		if k == ord('d'):
					data['im'] = img_copy.copy()
					cv2.circle(data['im'], (ix+1,iy),1, (0,0,255), 5, 16)
					ix = ix+1
					cv2.imshow("Image", data['im'])
					continue
	       		if k == ord('w'):
	       			data['im'] = img_copy.copy()
	        		cv2.circle(data['im'], (ix,iy-1),1, (0,0,255), 5, 16)
	        		iy = iy-1
	       			cv2.imshow("Image", data['im'])
	       			continue
	       		if k == ord('s'):
	       			data['im'] = img_copy.copy()
	        		cv2.circle(data['im'], (ix,iy+1),1, (0,0,255), 5, 16)
	        		iy = iy+1
	       			cv2.imshow("Image", data['im'])
	       			continue
	       		if k == ord('z'):
					data['im'] = img_copy.copy()
					cv2.imshow("Image", data['im'])
					continue
	       		if k == ord('x'):
	       			if len(data['points']) < 4 :
					data['points'].append([x,y])
					coordinates_x.append(x)
					coordinates_y.append(y)
	       			break
        # if len(data['points']) < 4 :
        #     data['points'].append([x,y])

def get_four_points(im):
    
    # Set up data to send to mouse handler
    data = {}
    data['im'] = im.copy()
    data['points'] = []
    
    #Set the callback function for any mouse event
    cv2.imshow("Image",im)
    cv2.setMouseCallback("Image", mouse_handler, data)
    cv2.waitKey(0)
    
    # Convert array to np.array
    points = np.vstack(data['points']).astype(float)
    
    return points


#if __name__ == '__main__' :

# Read source image.
#im_src = cv2.imread('/home/svoren258/Dokumenty/FIT_VUT/3_BIT/IBP/Les_Horribles_Cernettes_in_1992.jpg');
im_src = cv2.imread('/home/svoren258/Dokumenty/FIT_VUT/3_BIT/IBP/IBP/znacky/znacka1.png',1)

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


# Read destination image
#im_dst = cv2.imread('/home/svoren258/Dokumenty/FIT_VUT/3_BIT/IBP/times_square_night_2013.jpg');
im_dst = cv2.imread('/home/svoren258/Dokumenty/FIT_VUT/3_BIT/IBP/fotosada/IMG_20171120_132413.jpg',1)

im_dst = cv2.resize(im_dst, (0,0), fx=0.25, fy=0.25) 

im_bef = im_dst.copy()
# Get four corners of the billboard
print 'Click on four corners and then press ENTER'
pts_dst = get_four_points(im_dst)

# Calculate Homography between source and destination points
h, status = cv2.findHomography(pts_src, pts_dst);

# Warp source image
im_temp = cv2.warpPerspective(im_src, h, (im_dst.shape[1],im_dst.shape[0]))

# Black out polygonal area in destination image.
cv2.fillConvexPoly(im_dst, pts_dst.astype(int), 0, 16)

# Add warped source image to destination image.
im_out = im_dst + im_temp

# Resize image to wanted size
im_out = im_out[int(0.8*min(coordinates_y)):int(1.2*max(coordinates_y)), int(0.8*min(coordinates_x)):int(1.2*max(coordinates_x))]


# Display image.
while(1):
	cv2.imshow("Image", im_out)
	#cv2.imshow("Before", im_bef)
	k = cv2.waitKey(20) & 0xFF
	if k == 27:
		break
# cv2.waitKey(0);
cv2.destroyAllWindows()



# ix,iy = -1,-1
# coordinates_x = []
# coordinates_y = []
# coordinates = []
# # mouse callback function
# def draw_point(event,x,y,flags,param):
#     global ix,iy,coordinates_x, coordinates_y, coordinates
#     if event == cv2.EVENT_LBUTTONDBLCLK:
#         cv2.circle(img_dst,(x,y),1,(255,255,255),-1)
#         ix,iy = x,y
#         coordinates_x.append(x)
#         coordinates_y.append(y)
#         coordinates.append([y,x])

# #img = cv2.imread('/home/svoren258/Dokumenty/FIT_VUT/3_BIT/IBP/fotosada/IMG_20171120_132413.jpg',1)
# img = cv2.imread('/home/svoren258/Dokumenty/FIT_VUT/3_BIT/IBP/times_square_night_2013.jpg',1)

# #plt.imshow(img, cmap = 'gray', interpolation = 'bicubic')
# #plt.xticks([]), plt.yticks([])
# #plt.show()
# img_dst = cv2.resize(img, (0,0), fx=0.25, fy=0.25) 
# #crop_img = small[200:300, 200:400] # Crop from x, y, w, h -> 100, 200, 300, 400

# # Create a black image, a window and bind the function to window
# # img = np.zeros((512,512,3), np.uint8)
# cv2.namedWindow('image')

# cv2.setMouseCallback('image',draw_point)

# while(1):
#     cv2.imshow('image',img_dst)
#     k = cv2.waitKey(20) & 0xFF
#     if k == 27:
#         break
#     elif k == ord('a'):
#     	print coordinates
#     	print "coordinates x:", coordinates_x
#     	print "coordinates_y:", coordinates_y
#     	print "min x:", min(coordinates_x)
#     	print "min y:", min(coordinates_y)
#     	print "max x:", max(coordinates_x)
#     	print "max y:", max(coordinates_y)
#     elif k == ord('x'):
    	
#     	#cropped_spz = small[min(coordinates_y):max(coordinates_y), min(coordinates_x):max(coordinates_x)] 
#     	#cropped = small[int(0.8*min(coordinates_y)):int(1.2*max(coordinates_y)), int(0.8*min(coordinates_x)):int(1.2*max(coordinates_x))]
#     	#imgRowsSpz = cropped_spz.shape[0]
#     	#imgColsSpz = cropped_spz.shape[1]
#     	#channelsSpz = cropped_spz.shape[2]
#     	#imgRows = cropped.shape[0]
#     	#imgCols = cropped.shape[1]
#     	#channels = img.shape[2]
#     	#print imgRows
#     	#print imgCols
#     	#print channels

#     	#print imgRowsSpz
#     	#print imgColsSpz
#     	#print channelsSpz

#     	#print cropped_spz
#     	# cropped_spz_y_min = min(coordinates_y)-(int(0.8*min(coordinates_y)))
#     	# cropped_spz_x_min = min(coordinates_x)-(int(0.8*min(coordinates_x)))
#     	# cropped_spz_y_max = max(coordinates_y)-(int(0.8*min(coordinates_y)))
#     	# cropped_spz_x_max = max(coordinates_x)-(int(0.8*min(coordinates_x)))
#     	# S = (0.5, 0.5, 0.5, 0.5)
#     	# D = (0.5, 0.5, 0.5, 0.5)
#     	#img_src = cv2.imread('/home/svoren258/Dokumenty/FIT_VUT/3_BIT/IBP/IBP/znacky/znacka1.png',1)
#     	img_src = cv2.imread('/home/svoren258/Dokumenty/FIT_VUT/3_BIT/IBP/Les_Horribles_Cernettes_in_1992.jpg',1)
    	

#     	# size_y = max(coordinates_y) - min(coordinates_y)
#     	# size_x = max(coordinates_x) - min(coordinates_x)
#     	# # print size_y
#     	# # size_x = (1560*size_y)/330
#     	# # print size_x

#     	# resize_x = size_x/1560	
#     	# resize_y = size_y/330
    	
#     	# img_src = cv2.resize(img_src,None,fx=resize_x, fy=resize_y)
    	
#     	spzRows = img_src.shape[0]
#     	spzCols = img_src.shape[1]
#     	print spzRows
#     	print spzCols 
#     	# print coordinates

#     	pts_dst = np.array([[coordinates[0]],[coordinates[1]],[coordinates[2]],[coordinates[3]]])

#     	pts_src = np.array([[0,0],[spzCols-1,0],[spzCols-1,spzRows-1],[0, spzRows-1]])


#     	#pts_dst = np.array([[coordinates_y[0],coordinates_x[0]],[coordinates_y[1],coordinates_x[1]],[coordinates_y[2],coordinates_x[2]],[coordinates_y[3],coordinates_x[3]]])
#     	#pts_dst = np.array([[coordinates_y[0],coordinates_x[0]],[coordinates_y[3],coordinates_x[3]],[coordinates_y[2],coordinates_x[2]],[coordinates_y[1],coordinates_x[1]]])
#     	#pts_dst = np.array([[coordinates_y[1],coordinates_x[1]],[coordinates_y[2],coordinates_x[2]],[coordinates_y[3],coordinates_x[3]],[coordinates_y[0],coordinates_x[0]]])
#     	#pts_dst = np.array([[coordinates_y[1],coordinates_x[1]],[coordinates_y[0],coordinates_x[0]],[coordinates_y[3],coordinates_x[3]],[coordinates_y[2],coordinates_x[2]]])
#     	#pts_dst = np.array([[coordinates_y[2],coordinates_x[2]],[coordinates_y[3],coordinates_x[3]],[coordinates_y[0],coordinates_x[0]],[coordinates_y[1],coordinates_x[1]]])
#     	#pts_dst = np.array([[coordinates_y[2],coordinates_x[2]],[coordinates_y[1],coordinates_x[1]],[coordinates_y[0],coordinates_x[0]],[coordinates_y[3],coordinates_x[3]]])
#     	#pts_dst = np.array([[coordinates_y[3],coordinates_x[3]],[coordinates_y[0],coordinates_x[0]],[coordinates_y[1],coordinates_x[1]],[coordinates_y[2],coordinates_x[2]]])
#     	#pts_dst = np.array([[coordinates_y[3],coordinates_x[3]],[coordinates_y[2],coordinates_x[2]],[coordinates_y[1],coordinates_x[1]],[coordinates_y[0],coordinates_x[0]]])

#     	h, status = cv2.findHomography(pts_src, pts_dst)

#     	img_out = cv2.warpPerspective(img_src, h, (img_dst.shape[1],img_dst.shape[0]))
#     	cv2.imshow('img_src', img_src)
#     	cv2.imshow('img_dst', img_dst)
#     	cv2.imshow('final',img_out)
#     	#cv2.imshow('spz',cropped)
#     	# rows,cols,channels = spz_img.shape
#     	# roi = cropped[0:rows, 0:cols]
#     	# dst = cv2.add(spz_img, cropped)
#     	# cv2.imshow('dst',dst)
#     	# cropped[0:rows,0:cols] = dst
#     	# cv2.imshow('dst',cropped)
#     	# OverlayImage(cropped, spz_img, size_x, size_y, size_src_x, size_src_y, cropped_spz_x_min, cropped_spz_y_min, S, D)
#     	# cv2.imshow('cropped', cropped)
#     	# cv2.imshow('spz',spz_img)

#     	#resize_image(small)
# cv2.destroyAllWindows()

# # cv2.imshow('smaller image', small)
# # #cv2.imshow('cropped image', crop_img)
# # k = cv2.waitKey(0) & 0xFF
# # if k == 27:         # wait for ESC key to exit
# #     cv2.destroyAllWindows() 
# # elif k == ord('s'): # wait for 's' key to save and exit
# #     cv2.imwrite('mypic.png',small)
# #     cv2.destroyAllWindows()