#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  GetMarkFromSection.py
#  
#  Copyright 2018 User <User@DESKTOP-17Q7VC8>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import numpy as np
import cv2
import matplotlib.pyplot as plt
from imutils.perspective import four_point_transform
from imutils import contours
import math
import imutils
import time
from pandas import DataFrame
import errno
import os
from datetime import datetime

def divideSection(bubbleregion,path):

	# [GET] region of every questions section
	height,width = bubbleregion.shape[:2]
	print("height", height)
	print("width", width)

	Y = height
	WidthStart = 0
	sect = list()
	qSect = list()
	byQsect1 = list()
	byQsect2 = list()
	byQsect3 = list()
	listtrack = 0
	for i in range(2):
		WidthEnd = int(width * (i+1)/2)
		print("******* Process for part",i,"***********")
		if i == 0:
			WidthStart = WidthStart + 10
			
		if i == 1:
			WidthStart = WidthStart - 5
			WidthEnd   = WidthEnd 
			
		
		sect.insert(i,(bubbleregion[120:Y-30 , WidthStart+30:WidthEnd])) # divide the part between two // sect[0] ada 31 - 45 question , sect[1] ada 46-selebihnya 
		
		if i == 0: #   ************ process sect[0] ***************** #

			y,x = sect[i].shape[:2]
			leftbound = 90
			rightbound = x - 50 #the lesser the value, the "right"-er the output
			topbound = 0
			
			heightRange = int((y)/2)
			
			print("heightRange",heightRange)
			print()
			bottombound = heightRange - 20

			for l in range(2):
				print("\ttopbound",topbound)
				
				print("\t\tbottombound",bottombound)
				qSect.insert(l,(sect[i][topbound:bottombound, leftbound:rightbound])) #insert question part into qSect
				
				topbound = bottombound - 10 
				
				bottombound = bottombound + heightRange 
				#cv2.imwrite(os.path.join(path , str(l)+"a_an1.jpg"),qSect[l])
				
			for i in range(len(qSect)):
				print()
				
				widthQ,heightQ = qSect[i].shape[:2]
				
				if (i == 0):
					
					heightRange = int((heightQ)/7)
					
					leftbound = 80
					rightbound = widthQ #the lesser the value, the "right"-er the output
					topbound = 0
					
					
					print("heightRange",heightRange)
					
					bottombound = heightRange + 30

					for l in range(8):
						print("\ttopbound",topbound)
						
						print("\t\tbottombound",bottombound)
						byQsect1.insert(listtrack,(qSect[i][topbound:bottombound, leftbound:rightbound])) #insert question part into qSect
						print(l)
						topbound = bottombound - 22
						if l != 6:
							bottombound = bottombound + heightRange + 28
						else:
							bottombound = bottombound + heightRange + 20
						
						cv2.imwrite(os.path.join(path , str(listtrack)+"_section1.jpg"),byQsect1[listtrack])
						listtrack = listtrack + 1
				
				if (i == 1):
					heightRange = int((heightQ)/7)
					
					leftbound = 80
					rightbound = widthQ #the lesser the value, the "right"-er the output
					topbound = 0
				
					print("heightRange",heightRange)
					
					bottombound = heightRange + 30	
					
					for l in range(7):
						byQsect1.insert(listtrack,(qSect[i][topbound:bottombound, leftbound:rightbound])) #insert question part into qSect
						print(l)
						topbound = bottombound - 22
						if l != 6:
							bottombound = bottombound + heightRange + 28
						else:
							bottombound = bottombound + heightRange + 20
						
						cv2.imwrite(os.path.join(path , str(listtrack)+"_section1.jpg"),byQsect1[listtrack])
						listtrack = listtrack + 1	
							
				print(widthQ,heightQ) 
			
		else:
			print("second part")
		
		
		
				
		WidthStart = WidthEnd
		
		
		
		
	return sect,qSect

def divideSmaller(img):
	height,width = img.shape[:2]
	boxheight = int(height/15)
	print(boxheight)
	return boxheight
def resizeSmaller(img):
	height,width = img.shape[:2]
	height = int((height/2) * 1)
	width = int((width/2) * 1)
	resized_img = cv2.resize(img,(width,height))
	return resized_img

def viewPixel(img): 
		
	height,width = img.shape[:2]
	print("height", height)
	print("width", width)
	return

def save_qSect(imgname):
	strname = imgname+"_"+datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
	mydir = os.path.join(os.getcwd(),strname)
	try:
		os.makedirs(mydir)
	except OSError as e:
		if e.errno != errno.EEXIST:
			raise  # This was not a "directory exist" error..
	print(mydir)
	return mydir

def findAllCnts(img):
	kernel = np.ones((1, 1), np.uint8) #3
	img = doMorphologyEx(img, cv2.MORPH_OPEN, kernel)
	brcrop = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	#brblur =  cv2.medianBlur(brcrop,5)  #1
	brblur = doGaussianBlur(brcrop,(3,3))#1
	
	brthresh = doAdaptiveThreshold(brblur)
	kernel = np.ones((5, 5), np.uint8)
	bthresh = doMorphologyEx(brthresh, cv2.MORPH_CLOSE, kernel)
	_,cnts,_ = cv2.findContours(brthresh.copy(),cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
	# done find contours
	docCnt = None
	print(len(cnts))
	# ensure that at least one contour was found
	return cnts

def doMorphologyEx(im,method,kern):
	out = cv2.morphologyEx(im, method, kern)
	return out
	
def doAdaptiveThreshold(image):
	out = cv2.adaptiveThreshold(image,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,7,2)
	return out

def doGaussianBlur(im,numhere):
	out = cv2.GaussianBlur(im,numhere ,0)
	return out
	
def doMedianBlur(im,numhere):
	out = cv2.medianBlur(im,numhere)
	return out

def doBlur(im,numhere):
	out = cv2.blur(im,numhere)
	return out

def doThreshold(im):
	out = cv2.threshold(im, 128, 255, cv2.THRESH_BINARY)
	return out

def filter_contours(brcnts):
	# [FILTER] filter the bubble from other contours
	print("brcnts length ",len(brcnts))

	newbrcnts = []
	for c in brcnts:
		area = cv2.contourArea(c)
				
		if area > 350 and area < 580:
			perimeter = cv2.arcLength(c,True)
			print("area,perimeter")
			print(area,perimeter)
			
			if perimeter < 120 and perimeter > 75:
				newbrcnts.append(c)
	# done process
	bubblecnts = []
	 
	# loop over the contours
	print("ar,w,h")
		
	for c in newbrcnts:
		# compute the bounding box of the contour, then use the
		# bounding box to derive the aspect ratio
		(x, y, w, h) = cv2.boundingRect(c)
		ar = w / float(h)
		
		print(ar,w,h)
		# in order to label the contour as a question, region
		# should be sufficiently wide, sufficiently tall, and
		# have an aspect ratio approximately equal to 1
		if w >= 22 and h >= 22 and ar >= 0.9 and ar <= 1.2:
			bubblecnts.append(c)

	return bubblecnts

def sort_contours(cnts, method="left-to-right"):
	# initialize the reverse flag and sort index
	reverse = False
	i = 0
 
	# handle if we need to sort in reverse
	if method == "right-to-left" or method == "bottom-to-top":
		reverse = True
 
	# handle if we are sorting against the y-coordinate rather than
	# the x-coordinate of the bounding box
	if method == "top-to-bottom" or method == "bottom-to-top":
		i = 1
 
	# construct the list of bounding boxes and sort them from top to
	# bottom
	boundingBoxes = [cv2.boundingRect(c) for c in cnts]
	(cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
		key=lambda b:b[1][i], reverse=reverse))
 
	# return the list of sorted contours and bounding boxes
	return cnts


imgname = "g (2).jpg"
image = cv2.imread(imgname)
image = resizeSmaller(image)
path = save_qSect(imgname)
sect,qSect = divideSection(image,path)

cv2.waitKey(0)
