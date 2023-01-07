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
import trash_controller


def start_get_exp():
	print("开始练级")

	cave_path = game_controller.get_map_path()
	if len(cave_path) == 0:
		print("程序结束")
		return

	path_controller.set_map_data()

	# 转换为单步路径
	cave_path = game_controller.to_each_step_path(cave_path)

	nearest_pos = move_controller.get_nearest_pos(cave_path)
	globals.current_path_index = cave_path.index(nearest_pos)
	last_move_time = 0

	while(True):
		#消除系统确定消息框
		game_controller.click_sure_btn()
		#检测断开消息框
		if game_controller.connection_lose():
			print("断开")
			raise Exception("RESTART")

		if trash_controller.collect_ground_treasures() > 0:
			continue

		if game_controller.check_exp_getting():
			print("经验有增加")
			if time.time() - last_move_time > settings.move_check_time:
				while not game_controller.is_monster_nearby():
					print("距离上次移动已达{}s，检查当前屏幕无怪，去下一个点".format(str(settings.move_check_time)))
					move_controller.go_to_next_point(cave_path)
					last_move_time = time.time()
		else:
			print("经验没增加")
			#移动到下一个点
			move_controller.go_to_next_point(cave_path)
			last_move_time = time.time()
			while not game_controller.is_monster_nearby():
				move_controller.go_to_next_point(cave_path)
				last_move_time = time.time()


def retart_routine():
	print("重启游戏")
	game_controller.restart_game()
	success = game_controller.active_pet()
	if success:
		start()
	else:
		game_controller.restart_game()


def start():
	try:
		start_get_exp()
	except Exception as err:
		print('exception:', err)
		reason = err.args[0]
		if reason == "RESTART":
			retart_routine()
		elif "NoneType" in reason:
			print("adb 断开")
			adb_controller.restart_mumu()
			time.sleep(30)
			adb_controller.restart_adb()
			retart_routine()
	except:
		print('unknown exception')


