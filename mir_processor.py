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
	if start_exp == None or end_exp == None:
		return True

	cha = end_exp - start_exp
	print("{} - {} =  {}".format(str(end_exp), str(start_exp), str(cha)))
	if cha > 0:
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
		print("use expect current coordinate: {}".format(str(globals.expect_current_pos)))
		return globals.expect_current_pos


def get_nearest_pos(cave_path):
	current_pos = globals.current_pos
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

	return nearest_pos

# 单步路径移动，如果脱离路径，会先到当前路径距离目标路径最近点
def step_go_by_path(step_path, must_walk = False):
	print("step_go_by_path: {}".format(str(step_path)))
	# 目标坐标
	target_pos = step_path[len(step_path) - 1]
	# 刷新当前坐标
	get_current_coordinate()
	# 最大尝试次数
	move_try_limit = settings.move_try_limit
	while globals.current_pos[0] != target_pos[0] or globals.current_pos[1] != target_pos[1]:
		if move_try_limit > 0:
			move_try_limit = move_try_limit - 1

			if (globals.current_pos in step_path):
				index_of_current_pos = step_path.index(globals.current_pos)
				step_path = step_path[index_of_current_pos:]
			else:
				# 从当前坐标先到最近的点，再执行路径
				nearest_pos = get_nearest_pos(step_path)
				path_to_nearest_pos = get_step_path_to(nearest_pos)
				index_of_nearest_pos = step_path.index(nearest_pos)
				step_path = step_path[index_of_nearest_pos+1:]
				step_path = path_to_nearest_pos + step_path
				# print("step_path:{}".format(str(step_path)))

			game_controller.move_by_path(step_path, must_walk)

			time.sleep(1.0)
			get_current_coordinate()
		else:
			print("已达最大重试次数，尝试重启游戏")
			raise SystemExit("RESTART")

# 获取移动路劲
def get_step_path_to(target_pos):
	# 从当前坐标开始
	step_path = [globals.current_pos, target_pos]
	step_path = game_controller.to_each_step_path(step_path)
	# print("step_path: {}".format(str(step_path)))
	return step_path

def go_to_next_point(cave_path):
	# print("go_to_next_point cave_path:{}".format(str(cave_path)))
	if globals.current_pos == (0, 0):
		get_current_coordinate()

	path_len = len(cave_path)

	step_path = []
	if globals.current_pos in cave_path:
		# print("globals.current_pos in cave_path")
		globals.current_path_index = (globals.current_path_index + settings.one_time_move_distance) % path_len
		# print("globals.current_path_index = {}".format(str(globals.current_path_index)))
		target_pos = cave_path[globals.current_path_index]
		# print("target_pos = {}".format(str(target_pos)))

		if globals.current_pos == target_pos:
			return

		step_path = [target_pos]
		for index in range(0, path_len):
			path_index = (path_len + globals.current_path_index - 1 - index) % path_len
			# print("path_index = {}".format(str(path_index)))
			pos = cave_path[path_index]
			step_path = [pos] + step_path
			# print("step_path = {}".format(str(step_path)))
			if globals.current_pos == pos:
				break
	else:
		# print("globals.current_pos NOT in cave_path")
		nearest_pos = get_nearest_pos(cave_path)
		# print("nearest_pos：{}".format(str(nearest_pos)))
		globals.current_path_index = cave_path.index(nearest_pos)
		# print("globals.current_path_index{}".format(str(globals.current_path_index)))
		step_path = get_step_path_to(nearest_pos)

	step_go_by_path(step_path)



def start_get_exp():
	print("开始练级")

	cave_path = game_controller.get_map_path()
	# print("start_get_exp cave_path0:{}".format(str(cave_path)))
	if len(cave_path) == 0:
		print("程序结束")
		return

	# 转换为单步路径
	cave_path = game_controller.to_each_step_path(cave_path)
	# print("start_get_exp cave_path1:{}".format(str(cave_path)))

	try:
		nearest_pos = get_nearest_pos(cave_path)
		globals.current_path_index = cave_path.index(nearest_pos)
		last_move_time = 0;

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
					while not check_monster_reachable():
						print("距离上次移动已达{}s，检查当前屏幕无怪，去下一个点".format(str(settings.move_check_time)))
						go_to_next_point(cave_path)
						last_move_time = time.time()
			else:
				print("经验没增加，去下一个点")
				#移动到下一个点
				go_to_next_point(cave_path)
				last_move_time = time.time()
				while not check_monster_reachable():
					go_to_next_point(cave_path)
					last_move_time = time.time()
	except SystemExit as err:
		if err.args[0] == "RESTART":
			print("重启游戏")
			game_controller.restart_game()
			success = game_controller.active_pet()
			if success:
				start_get_exp()
			else:
				game_controller.restart_game()


def go_to_wen_biao_tou():
	#消除系统确定消息框
	game_controller.click_sure_btn()

	game_controller.click_map()
	time.sleep(1.0)
	adb_controller.screenshot(settings.screenshot_path)
	game_controller.click_map_npc_wen_biao_tou()
	game_controller.click_xun_lu()
	game_controller.close_map()

	while True:
		current_pos = get_current_coordinate()
		if abs(current_pos[0] - 438) < 20 and abs(current_pos[1] - 211) < 20:
			break

	step_path = get_step_path_to((443,206))
	step_go_by_path(step_path)

	#消除系统确定消息框
	game_controller.click_sure_btn()
	adb_controller.screenshot(settings.screenshot_path)
	game_controller.click_npc_wen_biao_tou()
	time.sleep(0.1)

	#改为点击固定点
	adb_controller.screenshot(settings.screenshot_path)
	game_controller.click_accept_ya_biao()


def go_to_lu_lao_ban():
	cave_path = settings.ya_biao_path
	if len(cave_path) == 0:
		print("程序结束")
		return

	# 转换为单步路径
	cave_path = game_controller.to_each_step_path(cave_path)
	settings.one_time_move_distance = 16
	try:
		nearest_pos = get_nearest_pos(cave_path)
		globals.current_path_index = cave_path.index(nearest_pos)
		last_move_time = 0;

		while(True):
			#消除系统确定消息框
			game_controller.click_sure_btn()
			go_to_next_point(cave_path)
			last_move_time = time.time()

	except SystemExit as err:
		if err.args[0] == "RESTART":
			print("重启游戏")
			game_controller.restart_game()
			start_ya_biao()


def start_ya_biao():
	print("开始押镖")
	go_to_wen_biao_tou()
	go_to_lu_lao_ban()






# 练级
# start_get_exp()


# ******************************************
# test
# ******************************************

# game_controller.click_map()
# adb_controller.screenshot(settings.screenshot_path)
# game_controller.click_npc_wen_biao_tou()
# game_controller.click_xun_lu()
# game_controller.close_map()
# adb_controller.screenshot(settings.screenshot_path)
# game_controller.click_accept_ya_biao()
# go_to_lu_lao_ban()

