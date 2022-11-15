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
	print("ImageProcessor: start to match "+target_path+" by "+template_path)

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

	print("ImageProcessor: best match value :"+str(min_val)+"   match location:"+str(min_loc[0])+" "+str(min_loc[1]))

	if(min_val > threshold):
		print("ImageProcessor: match failed")
		return None
	else:
		print("ImageProcessor: match succeeded")

	if(scope != None):
		min_loc = (min_loc[0] + scope[2],min_loc[1] + scope[0])
	else:
		min_loc = (min_loc[0] + twidth/2,min_loc[1] + theight/2)

	return min_loc

# 匹配文字
def easyocr_read(reader,target_path,scope = None,lower_color = [],upper_color = []):
	target = cv2.imread(target_path)

	if(scope != None):
		# debug绘制
		# cv2.rectangle(target, (scope[2],scope[0]), (scope[3], scope[1]),(0,0,255),2)
		# cv2.imshow("MatchResult-----MatchingValue=",target)
		# cv2.waitKey()
		target = target[scope[0]:scope[1],scope[2]:scope[3]]

	if len(lower_color) != 0 and len(upper_color) != 0:
		# 定义HSV中颜色的范围 https://www.cnblogs.com/ericling/p/15508044.html
		hsv = cv2.cvtColor(target, cv2.COLOR_BGR2HSV )
		lower_color = numpy.array(lower_color)
		upper_color = numpy.array(upper_color)

		# 设置HSV的阈值使得只取目标颜色
		target = cv2.inRange(hsv,lower_color, upper_color)

	result = reader.readtext(target)

	for reline in result:
		print(reline)

	return result


# 中文文字匹配
def easyocr_read_cn(target_path,scope = None,lower_color = [],upper_color = []):
	reader = easyocr.Reader(['ch_sim','en'], gpu = False)
	return easyocr_read(reader, target_path, scope, lower_color, upper_color)


# 非中文匹配
def easyocr_read_en(target_path,scope = None,lower_color = [],upper_color = []):
	reader = easyocr.Reader(['en'], gpu = False)
	return easyocr_read(reader, target_path, scope, lower_color, upper_color)

