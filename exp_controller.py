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

		# 血量低，可能背包满了，红喝不出来
		if not game_controller.is_me_healthy():
			trash_controller.try_get_bag_space(1)

		if trash_controller.collect_ground_treasures() > 0:
			continue

		#检查宝宝血量是否健康
		if not game_controller.is_pet_healthy():
			if game_controller.select_boss():
				# 攻击boss
				game_controller.cast_shield()
				game_controller.cast_lighting()
			else:
				# 往回跑，试图召回宠物
				game_controller.reactive_pet()
				game_controller.cast_shield()
				move_controller.go_to_previous_point()
				game_controller.reactive_pet()

			time.sleep(5.0)
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


def restart_routine(restart_mumu_adb = False):
	try:
		print("重启游戏")

		if restart_mumu_adb:
			adb_controller.restart_mumu()
			time.sleep(30)
			adb_controller.restart_adb()

		game_controller.restart_game()
		success = game_controller.active_pet()
		if success:
			start()
		else:
			game_controller.restart_game()
	except Exception as e:
		print('exception:', e)
		reason = e.args[0]
		if reason == "RESTART":
			restart_routine()
		elif "NoneType" in reason:
			print("adb 断开")
			restart_routine(True)
		else:
			restart_routine()
	else:
		print('unknown exception')


def start():
	try:
		start_get_exp()
	except Exception as e:
		print('exception:', e)
		reason = e.args[0]
		if reason == "RESTART":
			restart_routine()
		elif "NoneType" in reason:
			print("adb 断开")
			restart_routine(True)
		else:
			restart_routine()
	else:
		print('unknown exception')


