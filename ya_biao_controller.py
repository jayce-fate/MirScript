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

def start_ya_biao():
	print("开始押镖")
	path_controller.set_map_data("盟重土城")
	go_to_wen_biao_tou()
	go_to_lu_lao_ban()


def go_to_wen_biao_tou():
	#消除系统确定消息框
	game_controller.click_sure_btn()

	target_pos = (445, 206)
	game_controller.click_map()
	time.sleep(1.0)
	adb_controller.screenshot(settings.screenshot_path)
	game_controller.click_map_aim()
	game_controller.click_map_input()
	game_controller.click_map_input()
	game_controller.click_map_clear()
	point_str = "{},{}".format(target_pos[0], target_pos[1])
	adb_controller.input_text(point_str)
	game_controller.click_map_edit_confirm()
	game_controller.click_map_input_confirm()
	game_controller.click_xun_lu()
	game_controller.close_map()

	time.sleep(1.0)
	current_pos1 = mir_controller.get_current_coordinate()
	time.sleep(1.0)
	current_pos2 = mir_controller.get_current_coordinate()

	if current_pos1 != target_pos and current_pos1 == current_pos2:
		go_to_wen_biao_tou()

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

	mir_controller.get_current_coordinate()
	target_pos = settings.ya_biao_path[-1]
	path = path_controller.find_path(globals.current_pos, target_pos)
	mir_controller.step_go_by_path(path)

	# 等双倍时间
	while should_wait_until_double_time():
		time.sleep(10)

	#交付
	adb_controller.screenshot(settings.screenshot_path)
	game_controller.click_npc_lu_lao_ban()
	time.sleep(1.0)
	game_controller.click_finish_ya_biao()


def should_wait_until_double_time():
	# 范围时间
	time_min = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '19:00', '%Y-%m-%d%H:%M')
	time_max = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '20:00', '%Y-%m-%d%H:%M')

	# 当前时间
	current_time = datetime.datetime.now()

	# 判断当前时间是否在范围时间内
	if current_time > time_min and current_time < time_max:
	    return True
	else:
	    return False



#main
start_ya_biao()