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

block_point_cache = []

# 单步路径移动
def step_go_by_path(step_path):
	if len(step_path) == 0:
		return
	print("step_go_by_path: {}".format(str(step_path)))
	# 目标坐标
	target_pos = step_path[len(step_path) - 1]
	# 刷新当前坐标
	get_current_coordinate()
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
					# 目标位置被堵住，直接返回
					if next_pos == target_pos:
						return
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
			get_current_coordinate()
		else:
			# 达到最大尝试次数，放弃，返回
			return


def go_to_next_point(cave_path):
	# print("go_to_next_point")
	if globals.current_pos == (0, 0):
		get_current_coordinate()

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
	current_pos = get_current_coordinate()
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


def get_current_coordinate():
	coordinate = game_controller.read_coordinate_text()
	if coordinate == None:
		 print("当前坐标获取失败，可能地图被收起，尝试再次开关地图")
		 # 尝试点击地图开关
		 game_controller.open_or_close_map()
		 time.sleep(0.2)
		 #再次读取坐标
		 coordinate = game_controller.read_coordinate_text()

	if coordinate == None:
		print("当前坐标获取失败，可能背包被打开，小地图被遮挡，或者游戏中断")
		if globals.read_coordinate_fail_remain > 0:
			globals.read_coordinate_fail_remain = globals.read_coordinate_fail_remain - 1
			print("尝试重新读取坐标，剩余次数:{}".format(str(globals.read_coordinate_fail_remain)))
			time.sleep(1.0)
			return get_current_coordinate()
		else:
			print("已达最大重试次数，尝试重启游戏")
			raise SystemExit("RESTART")

	if len(coordinate) != 2:
		print("len(coordinate) != 2")
		return get_current_coordinate_after_adjust()
	else:
		current_pos = (int(coordinate[0].replace(".","")), int(coordinate[1]))
		print("当前坐标: {}".format(str(current_pos)))
		if current_pos[0] != 0 and current_pos[1] != 0:
			# 重置最大失败重试次数
			globals.read_coordinate_fail_remain = settings.read_coordinate_fail_limit
			globals.current_pos = current_pos
			return current_pos
		else:
			if globals.read_coordinate_fail_remain > 0:
				globals.read_coordinate_fail_remain = globals.read_coordinate_fail_remain - 1
				print("尝试重新读取坐标，剩余次数:{}".format(str(globals.read_coordinate_fail_remain)))
				time.sleep(1.0)
				return get_current_coordinate()
			else:
				print("已达最大重试次数，尝试重启游戏")
				raise SystemExit("RESTART")


def get_current_coordinate_after_adjust():
	if globals.expect_current_pos[0] == 0 and globals.expect_current_pos[1] == 0:
		adjust_count = globals.adjust_count % 16
		if adjust_count == 0:
			game_controller.one_step_walk_left()
		elif adjust_count == 1:
			game_controller.one_step_walk_left_up()
		elif adjust_count == 2:
			game_controller.one_step_walk_up()
		elif adjust_count == 3:
			game_controller.one_step_walk_right_up()
		elif adjust_count == 4:
			game_controller.one_step_walk_right()
		elif adjust_count == 5:
			game_controller.one_step_walk_right_down()
		elif adjust_count == 6:
			game_controller.one_step_walk_down()
		elif adjust_count == 7:
			game_controller.one_step_walk_left_down()
		elif adjust_count == 8:
			game_controller.one_step_walk_left()
			game_controller.one_step_walk_left()
		elif adjust_count == 9:
			game_controller.one_step_walk_left_up()
			game_controller.one_step_walk_left_up()
		elif adjust_count == 10:
			game_controller.one_step_walk_up()
			game_controller.one_step_walk_up()
		elif adjust_count == 11:
			game_controller.one_step_walk_right_up()
			game_controller.one_step_walk_right_up()
		elif adjust_count == 12:
			game_controller.one_step_walk_right()
			game_controller.one_step_walk_right()
		elif adjust_count == 13:
			game_controller.one_step_walk_right_down()
			game_controller.one_step_walk_right_down()
		elif adjust_count == 14:
			game_controller.one_step_walk_down()
			game_controller.one_step_walk_down()
		elif adjust_count == 15:
			game_controller.one_step_walk_left_down()
			game_controller.one_step_walk_left_down()
		elif adjust_count == 16:
			game_controller.one_step_walk_left()
			game_controller.one_step_walk_left()
			game_controller.one_step_walk_left()
		elif adjust_count == 17:
			game_controller.one_step_walk_left_up()
			game_controller.one_step_walk_left_up()
			game_controller.one_step_walk_left_up()
		elif adjust_count == 18:
			game_controller.one_step_walk_up()
			game_controller.one_step_walk_up()
			game_controller.one_step_walk_up()
		elif adjust_count == 19:
			game_controller.one_step_walk_right_up()
			game_controller.one_step_walk_right_up()
			game_controller.one_step_walk_right_up()
		elif adjust_count == 20:
			game_controller.one_step_walk_right()
			game_controller.one_step_walk_right()
			game_controller.one_step_walk_right()
		elif adjust_count == 21:
			game_controller.one_step_walk_right_down()
			game_controller.one_step_walk_right_down()
			game_controller.one_step_walk_right_down()
		elif adjust_count == 22:
			game_controller.one_step_walk_down()
			game_controller.one_step_walk_down()
			game_controller.one_step_walk_down()
		elif adjust_count == 23:
			game_controller.one_step_walk_left_down()
			game_controller.one_step_walk_left_down()
			game_controller.one_step_walk_left_down()

		globals.adjust_count = adjust_count + 1
		return get_current_coordinate()
	else:
		print("use expect current coordinate: {}".format(str(globals.expect_current_pos)))
		return globals.expect_current_pos