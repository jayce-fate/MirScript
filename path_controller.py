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

def get_map_data_path(map_name):
	adb_controller.screenshot(settings.screenshot_path)
	if not map_name:
		map_name = game_controller.read_map_name()
	map_data_path = "template_images/maps/{}.txt".format(str(map_name))
	return map_data_path

def get_map_data_cache_path():
	adb_controller.screenshot(settings.screenshot_path)
	map_name = game_controller.read_map_name()
	map_data_path = "template_images/maps/{}_cache.txt".format(str(map_name))
	return map_data_path

def write_map_data(map_data_path, data_list):
	with open(map_data_path, 'w') as fp:
		for item in data_list:
			fp.write("%s\n" % str(item))

def read_map_data(map_data_path):
	if not os.path.exists(map_data_path):
		return []

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

def get_map_size(map_name):
	adb_controller.screenshot(settings.screenshot_path)
	if not map_name:
		map_name = game_controller.read_map_name()
	size = (100, 100)
	if map_name == "废矿东部":
		size = (200, 200)
	elif map_name == "生死之间":
		size = (100, 100)
	elif map_name == "盟重土城":
		size = (1000, 800)
	else:
		size = (100, 100)
	return size

def set_map_data(map_name):
	# 初始化
	two_dimension_array = []
	map_size = get_map_size(map_name)
	for y_idx in range(0, map_size[1]):
		one_dimension_array = []
		for x_idx in range(0, map_size[0]):
			one_dimension_array.append(0)
		two_dimension_array.append(one_dimension_array)

	# print("two_dimension_array: \n{}".format(str(two_dimension_array)))

	#设置可达的点
	map_data_path = get_map_data_path(map_name)
	data_list = read_map_data(map_data_path)
	for index in range(0, len(data_list)):
		point = data_list[index]
		point_y = int(point[1])
		point_x = int(point[0])
		two_dimension_array[point_y][point_x] = 1
	global current_map_data
	current_map_data = two_dimension_array
	# print("current_map_data: \n{}".format(str(current_map_data)))



def find_path(start, end):
	# print("current_map_data: \n{}".format(str(current_map_data)))
	map_height = len(current_map_data)
	print("map_height: {}".format(str(map_height)))
	map_width = len(current_map_data[0])
	print("map_width: {}".format(str(map_width)))
	print("start: {}".format(str(start)))
	print("end: {}".format(str(end)))
	if start == end:
		print("start == end")
		return [end]

	paths = [[start]]
	# print("paths: {}".format(str(paths)))
	count = 0
	while True:
		count = count + 1
		total_count = len(paths)
		new_paths = []
		searched_points = []
		for idx in range(0, total_count):
			path = paths[idx]
			last_point = path[-1]
			# print("last_point: {}".format(str(last_point)))
			x = last_point[0]
			y = last_point[1]
			if 0 <= x - 1 and 0 <= y - 1:
				next_pos = (x - 1, y - 1)
				if current_map_data[next_pos[1]][next_pos[0]] == 1:
					if not next_pos in path and not next_pos in searched_points:
						searched_points.append(next_pos)
						new_path = list(path)
						new_path.append(next_pos)
						if new_path[-1] == end:
							return new_path
						new_paths.append(new_path)
			if 0 <= y - 1:
				next_pos = (x, y - 1)
				if current_map_data[next_pos[1]][next_pos[0]] == 1:
					if not next_pos in path and not next_pos in searched_points:
						searched_points.append(next_pos)
						new_path = list(path)
						new_path.append(next_pos)
						if new_path[-1] == end:
							return new_path
						new_paths.append(new_path)
			if x + 1 < map_width and 0 <= y - 1:
				next_pos = (x + 1, y - 1)
				if current_map_data[next_pos[1]][next_pos[0]] == 1:
					if not next_pos in path and not next_pos in searched_points:
						searched_points.append(next_pos)
						new_path = list(path)
						new_path.append(next_pos)
						if new_path[-1] == end:
							return new_path
						new_paths.append(new_path)
			if 0 <= x - 1:
				next_pos = (x - 1, y)
				if current_map_data[next_pos[1]][next_pos[0]] == 1:
					if not next_pos in path and not next_pos in searched_points:
						searched_points.append(next_pos)
						new_path = list(path)
						new_path.append(next_pos)
						if new_path[-1] == end:
							return new_path
						new_paths.append(new_path)
			if x + 1 < map_width:
				next_pos = (x + 1, y)
				if current_map_data[next_pos[1]][next_pos[0]] == 1:
					if not next_pos in path and not next_pos in searched_points:
						searched_points.append(next_pos)
						new_path = list(path)
						new_path.append(next_pos)
						if new_path[-1] == end:
							return new_path
						new_paths.append(new_path)
			if 0 <= x - 1 and y + 1 < map_height:
				next_pos = (x - 1, y + 1)
				if current_map_data[next_pos[1]][next_pos[0]] == 1:
					if not next_pos in path and not next_pos in searched_points:
						searched_points.append(next_pos)
						new_path = list(path)
						new_path.append(next_pos)
						if new_path[-1] == end:
							return new_path
						new_paths.append(new_path)
			if y + 1 < map_height:
				next_pos = (x, y + 1)
				if current_map_data[next_pos[1]][next_pos[0]] == 1:
					if not next_pos in path and not next_pos in searched_points:
						searched_points.append(next_pos)
						new_path = list(path)
						new_path.append(next_pos)
						if new_path[-1] == end:
							return new_path
						new_paths.append(new_path)
			if x + 1 < map_width and y + 1 < map_height:
				next_pos = (x + 1, y + 1)
				if current_map_data[next_pos[1]][next_pos[0]] == 1:
					if not next_pos in path and not next_pos in searched_points:
						searched_points.append(next_pos)
						new_path = list(path)
						new_path.append(next_pos)
						if new_path[-1] == end:
							return new_path
						new_paths.append(new_path)

		# print("paths: {}".format(str(paths)))
		# print("new_paths: {}".format(str(new_paths)))
		if count > map_height:
			print("count > map_height")
			return []
		elif 0 == len(new_paths):
			return []
		else:
			paths = new_paths


def set_block(pos):
	# print("pos: {}".format(str(pos)))
	# print("current_map_data: \n{}".format(str(current_map_data)))
	current_map_data[pos[1]][pos[0]] = 0
	# print("pos: {}".format(str(pos)))
	# print("current_map_data: \n{}".format(str(current_map_data)))


