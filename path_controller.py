import os
import time
import re
import cv2

import globals
import settings
import game_controller
import adb_controller

current_map_data = []

def get_map_img_path():
	adb_controller.screenshot(settings.screenshot_path)
	map_name = game_controller.read_map_name()
	map_img_path = "template_images/maps/{}.png".format(str(map_name))
	return map_img_path

def get_map_data_path():
	adb_controller.screenshot(settings.screenshot_path)
	map_name = game_controller.read_map_name()
	map_data_path = "template_images/maps/{}.txt".format(str(map_name))
	return map_data_path

def write_map_data(map_data_path, data_list):
	with open(map_data_path, 'w') as fp:
		for item in data_list:
			fp.write("%s\n" % str(item))

def read_map_data(map_data_path):
	data_list = []
	with open(map_data_path, 'r') as fp:
		for line in fp:
			# remove linebreak, the last character of each line
			x = line[:-1]
			without_quote = x.replace("(", "").replace(")", "")
			point = tuple(map(int, without_quote.split(',')))
			data_list.append(point)
	return data_list

def get_map_scale():
	adb_controller.screenshot(settings.screenshot_path)
	map_name = game_controller.read_map_name()
	scale = (1.0, 1.0, 0, 0)
	if map_name == "废矿东部":
		scale = (1.0, 1.0, 0, 0)
	elif map_name == "生死之间":
		scale = (14.8, 9.3, 60, 0)
	else:
		scale = (14.8, 9.3, 60, 0)
	return scale

def show_map():
	map_img_path = get_map_img_path()
	map_data_path = get_map_data_path()

	scale = get_map_scale()
	color = [0, 255, 0] #b,g,r
	color1 = [0, 0, 255] #b,g,r
	line_width = 10

	data_list = read_map_data(map_data_path)
	# 读取目标图片
	target = cv2.imread(map_img_path)
	for index in range(0, len(data_list)):
		point = data_list[index]
		for x_idx in range(0, line_width):
			for y_idx in range(0, line_width):
				point_y = int((point[1]) * scale[1] - line_width * 0.5) + x_idx + scale[3]
				point_x = int((point[0] + 1) * scale[0] - line_width * 0.5) + y_idx + scale[2]
				target[point_y, point_x] = color

	# debug
	# point = (83, 69)
	# for x_idx in range(0, line_width):
	# 	for y_idx in range(0, line_width):
	# 		point_y = int((point[1]) * scale[1] - line_width * 0.5) + x_idx + scale[3]
	# 		point_x = int((point[0] + 1) * scale[0] - line_width * 0.5) + y_idx + scale[2]
	# 		target[point_y, point_x] = color1

	# Display result image
	cv2.imshow('image', target)
	cv2.waitKey()

def get_map_size():
	adb_controller.screenshot(settings.screenshot_path)
	map_name = game_controller.read_map_name()
	size = (100, 100)
	if map_name == "废矿东部":
		size = (100, 100)
	elif map_name == "生死之间":
		size = (100, 100)
	else:
		size = (100, 100)
	return size

def set_map_data():
	# 初始化
	two_dimension_array = []
	map_size = get_map_size()
	for y_idx in range(0, map_size[1]):
		one_dimension_array = []
		for x_idx in range(0, map_size[0]):
			one_dimension_array.append(0)
		two_dimension_array.append(one_dimension_array)

	# print("two_dimension_array: \n{}".format(str(two_dimension_array)))

	#设置可达的点
	map_data_path = get_map_data_path()
	data_list = read_map_data(map_data_path)
	for index in range(0, len(data_list)):
		point = data_list[index]
		point_y = int(point[1])
		point_x = int(point[0])
		two_dimension_array[point_y][point_x] = 1
	global current_map_data
	current_map_data = two_dimension_array
	# print("current_map_data: \n{}".format(str(current_map_data)))

def get_path():
	# print("current_map_data: \n{}".format(str(current_map_data)))