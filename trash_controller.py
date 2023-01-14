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


def loop_drink_one_item(trash_name):
	print("loop_drink_one_item:" + trash_name)
	if game_controller.drink_item(trash_name):
		loop_drink_one_item(trash_name)


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

	trash_list = settings.trash_list_drink
	list_len = len(trash_list)
	for index in range(0, list_len):
		trash_name = trash_list[index]
		print("trash_name: {}".format(str(trash_name)))
		loop_drink_one_item(trash_name)

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
				if not game_controller.drink_item("强效金疮药"):
					break

			time.sleep(0.5)
			remain_capacity = game_controller.read_bag_remain_capacity()
			if space_need <= remain_capacity:
				game_controller.click_left_return()
				game_controller.click_right_return()
				return True

			for idx in range(0, space_need - remain_capacity):
				if not game_controller.drink_item("强效太阳水"):
					break

			remain_capacity = game_controller.read_bag_remain_capacity()
			if space_need <= remain_capacity:
				game_controller.click_left_return()
				game_controller.click_right_return()
				return True

		game_controller.click_left_return()
		game_controller.click_right_return()

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
			move_controller.step_go_by_path(path)
			collect_count = collect_count + 1
			handle_bag_full()

	gold_coords = game_controller.check_ground_golds()
	while 0 < len(gold_coords):
		for idx in range(0, len(gold_coords)):
			print("捡金币")
			coord = gold_coords[idx]
			path = path_controller.find_path(globals.current_pos, coord)
			move_controller.step_go_by_path(path)
			collect_count = collect_count + 1
			handle_bag_full()
		gold_coords = game_controller.check_ground_golds()

	return collect_count