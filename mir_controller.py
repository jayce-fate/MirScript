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
import move_controller

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
				return False
	return True


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
	item_coords = game_controller.check_ground_items(need_screenshot = False)
	item_count = len(item_coords)

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

# generate_map_data()
# game_controller.close_map()
# start_get_exp()
# path_controller.show_map()
