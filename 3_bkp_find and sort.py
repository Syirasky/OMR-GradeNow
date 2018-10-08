#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  a.py
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

def findAllCnts(img):
	kernel = np.ones((3,3), np.uint8) #3
	img = doMorphologyEx(img, cv2.MORPH_OPEN, kernel)
	brcrop = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	brblur =  cv2.medianBlur(brcrop,1)  #1
	#brblur = doGaussianBlur(brcrop,(1,1))#1
	brblur = cv2.Canny(brblur, 10, 100)
	#brthresh = doAdaptiveThreshold(brblur)
	kernel = np.ones((5, 5), np.uint8)
	bthresh = doMorphologyEx(brblur, cv2.MORPH_CLOSE, kernel)
	_,cnts,_ = cv2.findContours(bthresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
	

	cv2.drawContours(img,cnts,-1,(0,12,255),1)
	
	cv2.imshow("test2",img)
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
				
		if area > 100 and area < 850:
			perimeter = cv2.arcLength(c,True)
			print("area,perimeter")
			print(area,perimeter)
			
			if perimeter < 120 and perimeter > 68:
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
		if w >= 19 and h >= 19 and ar >= 0.9 and ar <= 1.3:
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


img =  cv2.imread("14_section1.jpg")
imgcp = img.copy()
cnts = findAllCnts(img)
newcnts = filter_contours(cnts)
newcnts = sort_contours(newcnts)
i = 0
r = 18
g= 5
b = 41
while(i<4):
	
	cv2.drawContours(imgcp,newcnts,i,(r,12,b),-1)
	
	r = 50 + r
	g = 10 + r
	b = g + r
	i = i + 1

cv2.imshow("a",imgcp)
cv2.waitKey(0)


