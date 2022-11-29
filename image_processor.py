import os
import time
import re
import cv2
import easyocr
import numpy
from PIL import Image

import settings

# 图片匹配
def match_template(target_path,template_path,threshold = 0.05,scope = None):
	# print("ImageProcessor: start to match "+target_path+" by "+template_path)

	# 读取目标图片
	target = cv2.imread(target_path)
	# 读取模版图片
	template = cv2.imread(template_path)
	# 获得模版图片的宽高尺寸
	theight, twidth = template.shape[:2]

	# 对应y0,y1 x0,x1
	if(scope != None):
		target = target[scope[0]:scope[1],scope[2]:scope[3]]

	# 执行模版匹配，采用的匹配方式cv2.TM_SQDIFF_NORMED
	result = cv2.matchTemplate(target,template,cv2.TM_SQDIFF_NORMED)

	# 寻找矩阵（一维数组当做向量，用Mat定义）中的最大值和最小值的匹配结果及其位置
	# 对于cv2.TM_SQDIFF及cv2.TM_SQDIFF_NORMED方法，min_val越趋近于0匹配度越好，匹配位置取min_loc
	# 对于其他方法max_val越趋近于1匹配度越好，匹配位置取max_loc
	min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)


	# 绘制矩形边框，将匹配区域标注出来
	# min_loc：矩形定点
	# (min_loc[0]+twidth, min_loc[1]+theight) 矩形的宽高
	# (0,0,255)矩形边框的颜色，2矩形边框宽度

	# strmin_val = str(min_val)
	# cv2.rectangle(target, min_loc, (min_loc[0]+twidth, min_loc[1]+theight),(0,0,255),2)
	# cv2.imshow("MatchResult-----MatchingValue="+strmin_val,target)
	# cv2.waitKey()

	# print("ImageProcessor: best match value :"+str(min_val)+"   match location:"+str(min_loc[0])+" "+str(min_loc[1]))

	if(min_val > threshold):
		print("ImageProcessor: match failed: " + template_path)
		return None
	else:
		print("ImageProcessor: match succeeded: " + template_path + " scope: (" + str(min_loc[1]) + "," + str(min_loc[1] + theight) + "," + str(min_loc[0]) + "," + str(min_loc[0] + twidth) + ")")

	if(scope != None):
		min_loc = (min_loc[0] + scope[2],min_loc[1] + scope[0])
	else:
		min_loc = (min_loc[0] + twidth/2,min_loc[1] + theight/2)

	return min_loc

# 匹配文字
def easyocr_read(reader,target_path,scope = None,lower_color = [],upper_color = []):
	# print("easyocr_read: "+target_path)
	target = cv2.imread(target_path)

	if(scope != None):
		target = target[scope[0]:scope[1],scope[2]:scope[3]]

	if len(lower_color) != 0 and len(upper_color) != 0:
		# 定义HSV中颜色的范围 https://www.cnblogs.com/ericling/p/15508044.html
		hsv = cv2.cvtColor(target, cv2.COLOR_BGR2HSV )
		lower_color = numpy.array(lower_color)
		upper_color = numpy.array(upper_color)

		# 设置HSV的阈值使得只取目标颜色
		mask = cv2.inRange(hsv,lower_color, upper_color)
		target = cv2.bitwise_and(target, target, mask=mask)

	# Display result image
	# cv2.imshow('image', target)
	# cv2.waitKey()

	result = reader.readtext(target)

	# for reline in result:
	# 	print(reline)

	return result


# 中文文字匹配
def easyocr_read_cn(target_path,scope = None,lower_color = [],upper_color = []):
	reader = easyocr.Reader(['ch_sim','en'], gpu = False)
	return easyocr_read(reader, target_path, scope, lower_color, upper_color)


# 非中文匹配
def easyocr_read_en(target_path,scope = None,lower_color = [],upper_color = []):
	reader = easyocr.Reader(['en'], gpu = False)
	return easyocr_read(reader, target_path, scope, lower_color, upper_color)


# 显示hsv调试工具
def show_hsv_tool(target_path, scope = None):
	def nothing(x):
		pass

	# Load image
	image = cv2.imread(target_path)

	if(scope != None):
		image = image[scope[0]:scope[1],scope[2]:scope[3]]

	# Create a window
	cv2.namedWindow('image')

	# Create trackbars for color change
	# Hue is from 0-179 for Opencv
	cv2.createTrackbar('HMin', 'image', 0, 179, nothing)
	cv2.createTrackbar('SMin', 'image', 0, 255, nothing)
	cv2.createTrackbar('VMin', 'image', 0, 255, nothing)
	cv2.createTrackbar('HMax', 'image', 0, 179, nothing)
	cv2.createTrackbar('SMax', 'image', 0, 255, nothing)
	cv2.createTrackbar('VMax', 'image', 0, 255, nothing)

	# Set default value for Max HSV trackbars
	cv2.setTrackbarPos('HMax', 'image', 179)
	cv2.setTrackbarPos('SMax', 'image', 255)
	cv2.setTrackbarPos('VMax', 'image', 255)

	# Initialize HSV min/max values
	hMin = sMin = vMin = hMax = sMax = vMax = 0
	phMin = psMin = pvMin = phMax = psMax = pvMax = 0

	while(1):
		# Get current positions of all trackbars
		hMin = cv2.getTrackbarPos('HMin', 'image')
		sMin = cv2.getTrackbarPos('SMin', 'image')
		vMin = cv2.getTrackbarPos('VMin', 'image')
		hMax = cv2.getTrackbarPos('HMax', 'image')
		sMax = cv2.getTrackbarPos('SMax', 'image')
		vMax = cv2.getTrackbarPos('VMax', 'image')

		# Set minimum and maximum HSV values to display
		lower = numpy.array([hMin, sMin, vMin])
		upper = numpy.array([hMax, sMax, vMax])

		# Convert to HSV format and color threshold
		hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
		mask = cv2.inRange(hsv, lower, upper)
		result = cv2.bitwise_and(image, image, mask=mask)

		# Print if there is a change in HSV value
		if((phMin != hMin) | (psMin != sMin) | (pvMin != vMin) | (phMax != hMax) | (psMax != sMax) | (pvMax != vMax) ):
			print("(hMin = %d , sMin = %d, vMin = %d), (hMax = %d , sMax = %d, vMax = %d)" % (hMin , sMin , vMin, hMax, sMax , vMax))
			phMin = hMin
			psMin = sMin
			pvMin = vMin
			phMax = hMax
			psMax = sMax
			pvMax = vMax

		# Display result image
		cv2.imshow('image', result)
		if cv2.waitKey(10) & 0xFF == ord('q'):
			break
	cv2.destroyAllWindows()

