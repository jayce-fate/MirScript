import os
import time
import re
import cv2
import random
import numpy
import datetime

import globals
import settings
import image_processor
import adb_controller
import game_controller
import path_controller
import mir_controller

block_point_cache = []

# 单步路径移动
def step_go_by_path(step_path):
	if len(step_path) == 0:
		return
	print("step_go_by_path: {}".format(str(step_path)))
	# 目标坐标
	target_pos = step_path[len(step_path) - 1]
	# 刷新当前坐标
	mir_controller.get_current_coordinate()
	# 最大尝试次数
	move_try_limit = settings.move_try_limit
	last_step_path = []
	while globals.current_pos[0] != target_pos[0] or globals.current_pos[1] != target_pos[1]:
		if move_try_limit > 0:
			move_try_limit = move_try_limit - 1

			if (globals.current_pos in step_path):
				index_of_current_pos = step_path.index(globals.current_pos)
				step_path = step_path[index_of_current_pos:]
			else:
				step_path = path_controller.find_path(globals.current_pos, target_pos)

			print("step_path:{}".format(str(step_path)))
			if len(last_step_path) >= 2 and last_step_path[0] == step_path[0]:
				next_pos = step_path[1]
				target_pos = step_path[-1]
				global block_point_cache
				if next_pos in block_point_cache:
					print("set_block:{}".format(str(next_pos)))
					block_point_cache.remove(next_pos)
					path_controller.set_block(next_pos)
					print("step_path[-1]:{}".format(str(target_pos)))
					step_path = path_controller.find_path(globals.current_pos, target_pos)
					if len(step_path) == 0:
						print("未找{}到{}的路径, 重置地图数据".format(str(globals.current_pos), str(target_pos)))
						path_controller.set_map_data()
						block_point_cache = []
						step_path = path_controller.find_path(globals.current_pos, target_pos)
				else:
					block_point_cache.append(next_pos)

			game_controller.move_by_path(step_path)

			last_step_path = step_path

			time.sleep(1.0)
			mir_controller.get_current_coordinate()
		else:
			print("已达最大重试次数，尝试重启游戏")
			raise SystemExit("RESTART")


def go_to_next_point(cave_path):
	# print("go_to_next_point")
	if globals.current_pos == (0, 0):
		mir_controller.get_current_coordinate()

	path_len = len(cave_path)

	globals.current_path_index = (globals.current_path_index + settings.one_time_move_distance) % path_len
	target_pos = cave_path[globals.current_path_index]
	# print("globals.current_pos:{}".format(str(globals.current_pos)))
	# print("target_pos:{}".format(str(target_pos)))
	if globals.current_pos == target_pos:
		return
	path = path_controller.find_path(globals.current_pos, target_pos)
	if len(path) > settings.one_time_move_distance + 1:
		target_pos = get_nearest_pos(cave_path)
		globals.current_path_index = cave_path.index(target_pos)
		path = path_controller.find_path(globals.current_pos, target_pos)

	if len(path) == 0:
		print("未找{}到{}的路径, 重置地图数据".format(str(globals.current_pos), str(target_pos)))
		path_controller.set_map_data()
		global block_point_cache
		block_point_cache = []
		path = path_controller.find_path(globals.current_pos, target_pos)

	step_go_by_path(path)


def get_nearest_pos(cave_path):
	current_pos = mir_controller.get_current_coordinate()
	print("current_pos: {}".format(str(current_pos)))
	path_len = len(cave_path)
	nearest_pos = cave_path[0]

	for index in range(1, path_len):
		position = cave_path[index]
		# print("position: {}".format(str(position)))
		current_pow = pow((position[0] - current_pos[0]), 2) + pow((position[1] - current_pos[1]), 2)
		# print("current_pow: {}".format(str(current_pow)))
		nearest_pow = pow((nearest_pos[0] - current_pos[0]), 2) + pow((nearest_pos[1] - current_pos[1]), 2)
		# print("nearest_pow: {}".format(str(nearest_pow)))
		if current_pow < nearest_pow:
			nearest_pos = position

	print("nearest_pos: {}".format(str(nearest_pos)))
	return nearest_pos