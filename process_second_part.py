#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  process_second_part.py
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

def resizeSmaller(img):
	height,width = img.shape[:2]
	height = int((height/2) * 1)
	width = int((width/2) * 1)
	resized_img = cv2.resize(img,(width,height))
	return resized_img

def divideSection(bubbleregion):
	height,width = bubbleregion.shape[:2]
	print("height", height)
	print("width", width)
	widthDivided = width/2
	
	
	
	return



imgname = "d.jpg"
image = cv2.imread(imgname)
image = resizeSmaller(image)

