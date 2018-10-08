#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  sort and grade.py
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
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	brblur =  cv2.medianBlur(gray,1)  #1
	#brblur = doGaussianBlur(gray,(1,1))#1
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

def gradeNow(image):
	
	cnts = findAllCnts(image.copy())
	
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	blurred = cv2.GaussianBlur(gray, (5, 5), 0)
	edged = cv2.Canny(blurred, 75, 200)

	thresh = cv2.threshold(gray, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
	cv2.imshow("thresh",thresh)
	
	filteredcnts = filter_contours(cnts)
	sortedcnts = sort_contours(filteredcnts)
	
	bubbled = None
	for (j, c) in enumerate(sortedcnts):
			# construct a mask that reveals only the current
			# "bubble" for the question
			mask = np.zeros(thresh.shape, dtype="uint8")
			cv2.drawContours(mask, [c], -1, 255, -1)
	 
			# apply the mask to the thresholded image, then
			# count the number of non-zero pixels in the
			# bubble area
			mask = cv2.bitwise_and(thresh, thresh, mask=mask)
			total = cv2.countNonZero(mask)
			print("Total",total)
			if bubbled is None or total > bubbled[0]:
				bubbled = (total, j)
			print("bubbled[1]")
			print(bubbled[1])
	return



img =  cv2.imread("14_section1.jpg")
gradeNow(img)
cv2.waitKey(0)


