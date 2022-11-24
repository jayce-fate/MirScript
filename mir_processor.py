import os
import time
import re
import cv2
import random
import numpy

import globals
import settings
import image_processor
import adb_controller
import game_controller


def check_monster_reachable():
	monster_list = game_controller.get_monster_list()
	if len(monster_list) > 0:
		return True
	else:
		return False

def check_exp_getting():
	start_exp = game_controller.read_current_exp()
	print("当前经验值: {}".format(str(start_exp)))

	sleep_time = 10
	time.sleep(sleep_time)

	end_exp = game_controller.read_current_exp()
	print("经过{}秒,当前经验值: {}".format(sleep_time, str(end_exp)))

	# 经验读取失败，默认经验仍在增加，偏向于不移动(等过check_exp_getting的时间无怪再移动)
	cha = end_exp - start_exp
	print("{} - {} =  {}".format(str(end_exp), str(start_exp), str(cha)))
	if start_exp == None or end_exp == None or cha > 0:
		return True
	else:
		return False

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
		return get_current_coordinate_after_adjust()
	else:
		globals.read_coordinate_fail_remain = settings.read_coordinate_fail_limit
		current_x = int(coordinate[0].replace(".",""))
		current_y = int(coordinate[1])
		print("当前坐标: {},{}".format(str(current_x), str(current_y)))
		if current_x != 0:
			globals.current_x = current_x
		if current_y != 0:
			globals.current_y = current_y
		return current_x, current_y


def get_current_coordinate_after_adjust():
	if settings.expect_current_x == 0 and settings.expect_current_y == 0:
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
			game_controller.one_step_run_left()
		elif adjust_count == 17:
			game_controller.one_step_run_left_up()
		elif adjust_count == 18:
			game_controller.one_step_run_up()
		elif adjust_count == 19:
			game_controller.one_step_run_right_up()
		elif adjust_count == 20:
			game_controller.one_step_run_right()
		elif adjust_count == 21:
			game_controller.one_step_run_right_down()
		elif adjust_count == 22:
			game_controller.one_step_run_down()
		elif adjust_count == 23:
			game_controller.one_step_run_left_down()

		globals.adjust_count = adjust_count + 1
		return get_current_coordinate()
	else:
		print("use expect current coordinate: {},{}".format(str(settings.expect_current_x), str(settings.expect_current_y)))
		return settings.expect_current_x, settings.expect_current_y


def get_nearest_pos_index(cave_path):
	# print("get_nearest_pos_index")
	current_x, current_y = get_current_coordinate()

	path_len = len(cave_path)
	nearest_pos = (-1, -1)

	for index in range(0,path_len):
		position = cave_path[index]
		# print("position: {}".format(str(position)))
		current_pow = pow((position[0] - current_x), 2) + pow((position[1] - current_y), 2)
		# print("current_pow: {}".format(str(current_pow)))
		nearest_pow = pow((nearest_pos[0] - current_x), 2) + pow((nearest_pos[1] - current_y), 2)
		# print("nearest_pow: {}".format(str(nearest_pow)))
		if current_pow < nearest_pow:
			nearest_pos = position

	nearest_index = cave_path.index(nearest_pos)
	print("最近坐标序号: {}".format(str(nearest_index)))
	return nearest_index

def go_to_next_point(cave_path):
	# print("go_to_next_point path_index : {}".format(str(globals.current_path_index)))

	path_len = len(cave_path)
	globals.current_path_index = (globals.current_path_index + settings.one_time_move_distance) % path_len
	move_to_index_of_path(globals.current_path_index, cave_path)

	if not check_monster_reachable():
		go_to_next_point(cave_path)

def move_to_index_of_path(path_index,path):
	target_pos = path[path_index]
	# print("target_pos: {}".format(str(target_pos)))
	current_x = globals.current_x
	current_y = globals.current_y
	# 最大尝试次数
	move_retry_limit = settings.move_retry_limit
	while current_x != target_pos[0] or current_y != target_pos[1]:
		if move_retry_limit > 0:
			move_retry_limit = move_retry_limit - 1
			game_controller.move_from_to((current_x, current_y), target_pos)
			time.sleep(1.0)
			current_x, current_y = get_current_coordinate()
		else:
			print("已达最大重试次数，尝试重启游戏")
			raise SystemExit("RESTART")


def start_get_exp():
	print("开始练级")

	cave_path = game_controller.get_map_path()
	if len(cave_path) == 0:
		print("程序结束")
		return

	# 转换为单步路径
	# cave_path = game_controller.to_each_step_path(cave_path)

	try:
	    #前往距离最近的路径点
		globals.current_path_index = get_nearest_pos_index(cave_path)
		move_to_index_of_path(globals.current_path_index, cave_path)
		last_move_time = time.time()

		while(True):
			#消除系统确定消息框
			game_controller.click_sure_btn()

			#检查等级，等级等于29且未拜师，停止练级
			lv = game_controller.read_lv_text()
			if (lv >= 26 and lv <= 29) and (not game_controller.already_has_master()):
				for index in range(0, 20):
					print("等级已达到{}级，请先去拜师!!!".format(str(lv)))
				if (lv == 29):
					if globals.check_has_master_fail_remain > 0:
						globals.check_has_master_fail_remain = globals.check_has_master_fail_remain - 1
						print("达到29级，请先去拜师，再提示{}次将结束本程序".format(str(globals.read_coordinate_fail_remain)))
					else:
						print("达到29级，请先去拜师，练级结束")
						return

			if check_exp_getting():
				print("经验有增加")
				if time.time() - last_move_time > settings.move_check_time:
					if not check_monster_reachable():
						print("距离上次移动已达{}s，检查当前屏幕无怪，去下一个点".format(str(settings.move_check_time)))
						go_to_next_point(cave_path)
						last_move_time = time.time()
			else:
				print("经验没增加，去下一个点")
				#移动到下一个点
				go_to_next_point(cave_path)
				last_move_time = time.time()
	except SystemExit as err:
		if err.args[0] == "RESTART":
			print("重启游戏")
			game_controller.restart_game()
			start_get_exp()


# 练级
start_get_exp()


# ******************************************
# test
# ******************************************

# image_processor.show_hsv_tool(settings.screenshot_path)
# adb_controller.screenshot(settings.screenshot_path)
# game_controller.move_by_path(game_controller.to_each_step_path(settings.test_path))
# adb_controller.start_app()
# adb_controller.screenshot(settings.screenshot_path)
# adb_controller.stop_app()

