import os
import time
import re
import cv2
import easyocr
from PIL import Image

import settings


last_match_loc = None

# 图片匹配
def match_template(target_path,template_path,threshold = 0.05,return_center = True
					,print_debug = True,scope = None,except_locs = None):
	if(print_debug):
		print("ImageProcessor: start to match "+target_path+" by "+template_path)

	if(print_debug and except_locs != None):
		print("ImageProcessor: except_locs: "+str(except_locs))

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
	# print("result is: ", result)

	# 归一化处理
	# cv2.normalize(result, result, 0, 1, cv2.NORM_MINMAX, -1)

	# 去掉except_locs中的坐标（已经匹配上），为1就是匹配失败
	# result中k是y轴，j是x轴
	rheight, rwidth = result.shape[:2]
	if(except_locs != None):
		for except_loc in except_locs:
			if(except_loc == None):
				continue
			for j in range(except_loc[0] - settings.except_dist,except_loc[0] + settings.except_dist):
				for k in range(except_loc[1] - settings.except_dist,except_loc[1] + settings.except_dist):
					if(j>=0 and j<rwidth and k>=0 and k<rheight):
						result[k][j] = 1

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


	if(print_debug):
		print("ImageProcessor: best match value :"+str(min_val)+"   match location:"+str(min_loc[0])+" "+str(min_loc[1]))

	if(min_val > threshold):
		if(print_debug):
			print("ImageProcessor: match failed")
		return None
	else:
		if(print_debug):
			print("ImageProcessor: match succeeded")

	last_match_loc = min_loc

	if(return_center):
		min_loc = (min_loc[0] + twidth/2,min_loc[1] + theight/2)

	if(scope != None):
		min_loc = (min_loc[0] + scope[2],min_loc[1] + scope[0])

	return min_loc

# 文字匹配
def easyocr_read(target_path,print_debug = False,scope = None):
	reader = easyocr.Reader(['ch_sim','en'], gpu = False)
	target = cv2.imread(target_path)

	if(scope != None):
		# debug绘制
		# cv2.rectangle(target, (scope[2],scope[0]), (scope[3], scope[1]),(0,0,255),2)
		# cv2.imshow("MatchResult-----MatchingValue=",target)
		# cv2.waitKey()
		target = target[scope[0]:scope[1],scope[2]:scope[3]]

	result = reader.readtext(target)

	if(print_debug):
		for reline in result:
			print(reline)

	return result
