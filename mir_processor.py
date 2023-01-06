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

def check_monster_reachable():
	monster_list = game_controller.get_monster_list()
	# print("monster_list: {}".format(str(monster_list)))
	if len(monster_list) > 0:
		return True
	else:
		return False

def check_exp_getting():
	for index in range(0, 5):
		if game_controller.got_exp_add_text():
			print("exp adding")
			return True
		else:
			print("exp cheking")

	print("exp not adding")
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


block_point_cache = []
# 单步路径移动，如果脱离路径，会先到当前路径距离目标路径最近点
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
				# # 从当前坐标先到最近的点，再执行路径
				# nearest_pos = get_nearest_pos(step_path)
				# print("nearest_pos:{}".format(str(nearest_pos)))
				# # path_to_nearest_pos = get_step_path_to(nearest_pos)
				# path_to_nearest_pos = path_controller.find_path(globals.current_pos, nearest_pos)
				# print("path_to_nearest_pos:{}".format(str(path_to_nearest_pos)))
				# index_of_nearest_pos = step_path.index(nearest_pos)
				# print("index_of_nearest_pos:{}".format(str(index_of_nearest_pos)))
				# step_path = step_path[index_of_nearest_pos+1:]
				# print("step_path:{}".format(str(step_path)))
				# step_path = path_to_nearest_pos + step_path
				# print("step_path:{}".format(str(step_path)))
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
	# print("go_to_next_point")
	if globals.current_pos == (0, 0):
		get_current_coordinate()

	path_len = len(cave_path)

	# step_path = []
	# if globals.current_pos in cave_path:
	# 	next_path_index = (globals.current_path_index + settings.one_time_move_distance) % path_len
	# 	target_pos = cave_path[next_path_index]
	# 	if globals.current_pos == target_pos:
	# 		return
	#
	# 	step_path_tmp = [target_pos]
	# 	for index in range(0, path_len):
	# 		path_index = (path_len + next_path_index - 1 - index) % path_len
	# 		pos = cave_path[path_index]
	# 		step_path_tmp = [pos] + step_path_tmp
	# 		if len(step_path_tmp) > settings.one_time_move_distance + 1:
	# 			print("len(step_path_tmp) > settings.one_time_move_distance + 1")
	# 			break
	# 		if globals.current_pos == pos:
	# 			if len(step_path_tmp) <= settings.one_time_move_distance + 1:
	# 				step_path = step_path_tmp
	# 				globals.current_path_index = next_path_index
	# 			break
	#
	# if len(step_path) == 0:
	# 	nearest_pos = get_nearest_pos(cave_path)
	# 	globals.current_path_index = cave_path.index(nearest_pos)
	# 	step_path = get_step_path_to(nearest_pos)
	#
	# step_go_by_path(step_path)

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




def check_level():
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


def start_get_exp():
	print("开始练级")

	cave_path = game_controller.get_map_path()
	# print("start_get_exp cave_path0:{}".format(str(cave_path)))
	if len(cave_path) == 0:
		print("程序结束")
		return

	path_controller.set_map_data()
	global block_point_cache
	block_point_cache = []

	# 转换为单步路径
	cave_path = game_controller.to_each_step_path(cave_path)
	# print("start_get_exp cave_path1:{}".format(str(cave_path)))

	try:
		nearest_pos = get_nearest_pos(cave_path)
		globals.current_path_index = cave_path.index(nearest_pos)
		last_move_time = 0
		# last_check_bag_capacity_time = 0

		while(True):
			if game_controller.connection_lose():
				print("断开")
				raise SystemExit("RESTART")
			else:
				#消除系统确定消息框
				game_controller.click_sure_btn()

			if collect_ground_treasures() > 0:
				# last_check_bag_capacity_time = time.time()
				continue

			# if time.time() - last_check_bag_capacity_time > settings.move_bag_capacity_time:
			# 	last_check_bag_capacity_time = time.time()
			# 	if is_bag_full():
			# 		drop_trashes()
			# check_level()

			if check_exp_getting():
				print("经验有增加")
				if time.time() - last_move_time > settings.move_check_time:
					while not is_monster_nearby(): #or not check_monster_reachable():
						print("距离上次移动已达{}s，检查当前屏幕无怪，去下一个点".format(str(settings.move_check_time)))
						go_to_next_point(cave_path)
						last_move_time = time.time()
			else:
				print("经验没增加")
				#移动到下一个点
				go_to_next_point(cave_path)
				last_move_time = time.time()
				while not is_monster_nearby(): #or not check_monster_reachable():
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
		else:
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


def should_wait_until_double_time():
	# 范围时间
	time_min = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '19:00', '%Y-%m-%d%H:%M')
	time_max = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '20:01', '%Y-%m-%d%H:%M')

	# 当前时间
	current_time = datetime.datetime.now()

	# 判断当前时间是否在范围时间内
	if current_time > time_min and current_time < time_max:
	    return True
	else:
	    return False


def go_to_lu_lao_ban():
	cave_path = settings.ya_biao_path
	if len(cave_path) == 0:
		print("程序结束")
		return

	# 转换为单步路径
	cave_path = game_controller.to_each_step_path(cave_path)
	settings.one_time_move_distance = 100
	try:
		nearest_pos = get_nearest_pos(cave_path)
		globals.current_path_index = cave_path.index(nearest_pos)
		last_move_time = 0;

		while(True):
			#消除系统确定消息框
			game_controller.click_sure_btn()

			path_len = len(cave_path)
			# 出口
			if (globals.current_path_index + settings.one_time_move_distance) == path_len - 1:
				break;
			elif (globals.current_path_index + settings.one_time_move_distance) > path_len - 1:
				settings.one_time_move_distance = path_len - 1 - globals.current_path_index

			go_to_next_point(cave_path)
			last_move_time = time.time()

		# 等双倍时间
		while should_wait_until_double_time():
			time.sleep(10)

		#交付
		adb_controller.screenshot(settings.screenshot_path)
		game_controller.click_npc_lu_lao_ban()
		time.sleep(1.0)
		game_controller.click_finish_ya_biao()
	except SystemExit as err:
		if err.args[0] == "RESTART":
			print("重启游戏")
			game_controller.restart_game()
			start_ya_biao()


def start_ya_biao():
	print("开始押镖")
	path_controller.set_map_data()
	go_to_wen_biao_tou()
	go_to_lu_lao_ban()


def loop_drop_one_item(trash_name, is_green = False, force_drop = False):
	print("loop_drop_one_item:" + trash_name + str(is_green) + str(force_drop))
	if game_controller.select_item(trash_name):
		game_controller.click_drop()
		if force_drop:
			game_controller.click_confirm_drop()
			# print("click_confirm_drop")
			adb_controller.screenshot(settings.screenshot_path)
			loop_drop_one_item(trash_name, is_green, force_drop)
		else:
			time.sleep(0.1)
			adb_controller.screenshot(settings.screenshot_path)
			if game_controller.is_quality():
				game_controller.click_cancel_drop()
				adb_controller.screenshot(settings.screenshot_path)
			else:
				if is_green:
					game_controller.click_confirm_drop()
					adb_controller.screenshot(settings.screenshot_path)
				loop_drop_one_item(trash_name, is_green, force_drop)

def drop_trashes_loop():
	adb_controller.screenshot(settings.screenshot_path)

	trash_list = settings.trash_list_white
	list_len = len(trash_list)
	for index in range(0, list_len):
		trash_name = trash_list[index]
		print("trash_name: {}".format(str(trash_name)))
		loop_drop_one_item(trash_name)

	trash_list = settings.trash_list_green
	list_len = len(trash_list)
	for index in range(0, list_len):
		trash_name = trash_list[index]
		print("trash_name: {}".format(str(trash_name)))
		loop_drop_one_item(trash_name, is_green = True)

	trash_list = settings.trash_list_force_drop
	list_len = len(trash_list)
	for index in range(0, list_len):
		trash_name = trash_list[index]
		print("trash_name: {}".format(str(trash_name)))
		loop_drop_one_item(trash_name, force_drop = True)

def drop_trashes(neen_open_close_bag = True):
	if neen_open_close_bag:
		game_controller.open_bag()
		time.sleep(0.5)

	game_controller.wipe_down_bag()
	game_controller.click_arrange_bag()
	time.sleep(2.0)
	drop_trashes_loop()
	# 按整理再来一次，使物品顺序相反，减少同一种物品因为极品，没有继续循环的问题
	# game_controller.click_arrange_bag()
	# time.sleep(2.0)
	# drop_trashes_loop()
	if neen_open_close_bag:
		game_controller.click_left_return()
		game_controller.click_right_return()

def is_bag_full():
	game_controller.open_bag()
	time.sleep(0.5)

	is_bag_full = game_controller.is_bag_full()

	game_controller.click_left_return()
	game_controller.click_right_return()

	return is_bag_full

def generate_map_data():
	map_data_path = path_controller.get_map_data_path()
	map_data_cache_path = path_controller.get_map_data_cache_path()
	map_size = path_controller.get_map_size()

	#获取预设路径
	cave_path = game_controller.get_map_path()
	if len(cave_path) == 0:
		print("len(cave_path) == 0")
		return
	# 转换为单步路径
	cave_path = game_controller.to_each_step_path(cave_path)

	# if os.path.exists(map_data_path):
	data_list = path_controller.read_map_data(map_data_path)
	for idx in range(0, len(cave_path)):
		point = cave_path[idx]
		if not point in data_list:
			data_list.append(point)

	path_controller.write_map_data(map_data_path, data_list)

	game_controller.click_map()
	time.sleep(1.0)

	start_scope = 0
	generate_scope = (7, 7)
	current_data_list = path_controller.read_map_data(map_data_path)
	checked_point_list = path_controller.read_map_data(map_data_cache_path)
	for idx in range(0, len(cave_path)):
		base_point = cave_path[idx]
		for y_idx in range(base_point[1] - generate_scope[1], base_point[1] + generate_scope[1] + 1):
			for x_idx in range(base_point[0] - generate_scope[0], base_point[0] + generate_scope[0] + 1):
				if x_idx < base_point[0] - start_scope or base_point[0] + start_scope < x_idx:
					if y_idx < base_point[1] - start_scope or base_point[1] + start_scope < y_idx:
						point = (x_idx, y_idx)
						if not point in current_data_list and not point in checked_point_list:
							game_controller.click_map_aim()
							game_controller.click_map_input()
							game_controller.click_map_input()
							game_controller.click_map_clear()
							point_str = "{},{}".format(point[0], point[1])
							adb_controller.input_text(point_str)
							game_controller.click_map_edit_confirm()
							game_controller.click_map_input_confirm()
							time.sleep(0.2)
							adb_controller.screenshot(settings.screenshot_path)
							match_loc = image_processor.match_template(
								settings.screenshot_path,r"template_images/map_point_indicate.png",0.1)
							if(match_loc != None):
								current_data_list.append(point)
								path_controller.write_map_data(map_data_path, current_data_list)

							if not point in checked_point_list:
								checked_point_list.append(point)
								path_controller.write_map_data(map_data_cache_path, checked_point_list)

	# path_controller.write_map_data(map_data_path, current_data_list)


	# for y_idx in range(69, 89):
	# 	data_list = path_controller.read_map_data(map_data_path)
	# 	for x_idx in range(73, 76):
	# 		point = (x_idx, y_idx)
	# 		game_controller.click_map_aim()
	# 		game_controller.click_map_input()
	# 		game_controller.click_map_input()
	# 		game_controller.click_map_clear()
	# 		point_str = "{},{}".format(point[0], point[1])
	# 		adb_controller.input_text(point_str)
	# 		game_controller.click_map_edit_confirm()
	# 		game_controller.click_map_input_confirm()
	# 		time.sleep(0.2)
	# 		adb_controller.screenshot(settings.screenshot_path)
	# 		match_loc = image_processor.match_template(
	# 			settings.screenshot_path,r"template_images/map_point_indicate.png",0.1)
	# 		if(match_loc != None):
	# 			if not point in data_list:
	# 				data_list.append(point)
	# 			else:
	# 				print("point: {} already in map data list".format(str(point)))
	#
	# 	path_controller.write_map_data(map_data_path, data_list)

def try_get_bag_space(space_need):
	if space_need > 0:
		game_controller.open_bag()
		time.sleep(0.5)
		remain_capacity = game_controller.read_bag_remain_capacity()
		if space_need <= remain_capacity:
			game_controller.click_left_return()
			game_controller.click_right_return()
			return True
		else:
			drop_trashes(neen_open_close_bag = False)
			remain_capacity = game_controller.read_bag_remain_capacity()
			if space_need <= remain_capacity:
				game_controller.click_left_return()
				game_controller.click_right_return()
				return True

			for idx in range(0, space_need - remain_capacity):
				if not game_controller.drink_red():
					break

			remain_capacity = game_controller.read_bag_remain_capacity()
			if space_need <= remain_capacity:
				game_controller.click_left_return()
				game_controller.click_right_return()
				return True

			for idx in range(0, space_need - remain_capacity):
				if not game_controller.drink_sun_water():
					break

			remain_capacity = game_controller.read_bag_remain_capacity()
			if space_need <= remain_capacity:
				game_controller.click_left_return()
				game_controller.click_right_return()
				return True

	return False

def handle_bag_full():
	while game_controller.got_bag_full_text():
		if not try_get_bag_space(1):
			print("背包已满，无法腾出空间，休息2秒")
			time.sleep(2)

def collect_ground_treasures():
	adb_controller.screenshot(settings.screenshot_path)
	# current_pos = get_current_coordinate()
	item_coords = game_controller.check_ground_items(need_screenshot = False)
	item_count = len(item_coords)
	# gold_coords = game_controller.check_ground_golds(need_screenshot = False)
	# gold_count = len(gold_coords)
	# treasure_count = item_count + gold_count

	# 多腾点空间，以免金币上面有别的东西
	# if try_get_bag_space(treasure_count):
	# 	path_all = [current_pos]
	# 	for idx in range(0, item_count):
	# 		print("捡绿色物品")
	# 		coord = item_coords[idx]
	# 		path = path_controller.find_path(path_all[len(path_all) - 1], coord)
	# 		path_all = path_all + path[1:]
	# 		current_pos = globals.current_pos
	#
	# 	for idx in range(0, gold_count):
	# 		print("捡金币")
	# 		coord = gold_coords[idx]
	# 		path = path_controller.find_path(path_all[len(path_all) - 1], coord)
	# 		path_all = path_all + path[1:]
	# 		current_pos = globals.current_pos
	#
	# 	step_go_by_path(path_all)
	#
	# 	collect_count = treasure_count
	# else:
	# 	collect_count = 0

	collect_count = 0
	for idx in range(0, item_count):
		print("捡绿色物品")
		coord = item_coords[idx]
		path = path_controller.find_path(globals.current_pos, coord)
		if len(path) > 0:
			step_go_by_path(path)
			collect_count = collect_count + 1
			handle_bag_full()

	gold_coords = game_controller.check_ground_golds()
	while 0 < len(gold_coords):
		for idx in range(0, len(gold_coords)):
			print("捡金币")
			coord = gold_coords[idx]
			path = path_controller.find_path(globals.current_pos, coord)
			step_go_by_path(path)
			collect_count = collect_count + 1
			handle_bag_full()
		gold_coords = game_controller.check_ground_golds()

	return collect_count


def is_monster_nearby():
	adb_controller.screenshot(settings.screenshot_path1)
	adb_controller.screenshot(settings.screenshot_path2)
	masks = []
	masks.append((0,34,440,1234)) #顶部滚动通知
	masks.append((42,198,1354,1664)) #右上角地图
	masks.append((796,936,625,1196)) #底部聊天窗口
	masks.append((358,600,710,980)) #我自己
	masks.append((152,274,756,910)) #经验提示框1
	masks.append((796,936,470,610)) #血、魔球
	match_loc = image_processor.match_template(
		settings.screenshot_path1, settings.screenshot_path2, 0.0001, masks = masks)
	if(match_loc != None):
		print("monster not nearby")
		return False
	else:
		print("monster nearby")
		return True


# ******************************************
# test
# ******************************************
# adb_controller.screenshot(settings.screenshot_path)
# game_controller.show_scope()

generate_map_data()
# game_controller.close_map()
# start_get_exp()
# path_controller.show_map()
