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
			
			#print("heightRange",heightRange)
			#print()
			bottombound = heightRange - 20

			for l in range(2):
				#print("\ttopbound",topbound)
				
				#print("\t\tbottombound",bottombound)
				qSect.insert(l,(sect[i][topbound:bottombound, leftbound:rightbound])) #insert question part into qSect
				
				topbound = bottombound - 10 
				
				bottombound = bottombound + heightRange 
				#cv2.imwrite(os.path.join(path , str(l)+"a_an1.jpg"),qSect[l])
				
			for i in range(len(qSect)):
				
				
				widthQ,heightQ = qSect[i].shape[:2]
				
				if (i == 0):
					
					heightRange = int((heightQ)/7)
					
					leftbound = 80
					rightbound = widthQ #the lesser the value, the "right"-er the output
					topbound = 0
					
					
					#print("heightRange",heightRange)
					
					bottombound = heightRange + 30

					for l in range(8):
						#print("\ttopbound",topbound)
						
						#print("\t\tbottombound",bottombound)
						byQsect1.insert(listtrack,(qSect[i][topbound:bottombound, leftbound:rightbound])) #insert question part into qSect
						#print(l)
						topbound = bottombound - 22
						if l != 6:
							bottombound = bottombound + heightRange + 28
						else:
							bottombound = bottombound + heightRange + 20
						
						cv2.imwrite(os.path.join(path , "0"+str(listtrack)+"_section1.jpg"),byQsect1[listtrack])
						listtrack = listtrack + 1
				
				if (i == 1):
					heightRange = int((heightQ)/7)
					
					leftbound = 80
					rightbound = widthQ #the lesser the value, the "right"-er the output
					topbound = 0
				
					#print("heightRange",heightRange)
					
					bottombound = heightRange + 30	
					
					for l in range(7):
						byQsect1.insert(listtrack,(qSect[i][topbound:bottombound, leftbound:rightbound])) #insert question part into qSect
						#print(l)
						topbound = bottombound - 22
						if l != 6:
							bottombound = bottombound + heightRange + 28
						else:
							bottombound = bottombound + heightRange + 20
						if listtrack <10:
							headname = "0"+str(listtrack)
						else:
							headname = str(listtrack)
						cv2.imwrite(os.path.join(path ,headname+"_section1.jpg"),byQsect1[listtrack])
						listtrack = listtrack + 1	
							
				#print(widthQ,heightQ) 
			
		else:
			print("second part")
			
		
		
				
		WidthStart = WidthEnd
		
		
		
		
	return sect,qSect


def divideSmaller(img):
	height,width = img.shape[:2]
	boxheight = int(height/15)
	#print(boxheight)
	#return boxheight
def resizeSmaller(img):
	height,width = img.shape[:2]
	height = int((height/2) * 1)
	width = int((width/2) * 1)
	resized_img = cv2.resize(img,(width,height))
	return resized_img

def viewPixel(img): 
		
	height,width = img.shape[:2]
	#print("height", height)
	#print("width", width)
	return

def save_qSect(imgname):
	strname = imgname+"_"+datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
	mydir = os.path.join(os.getcwd(),strname)
	try:
		os.makedirs(mydir)
	except OSError as e:
		if e.errno != errno.EEXIST:
			raise  # This was not a "directory exist" error..
	#print(mydir)
	return mydir

