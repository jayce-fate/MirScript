import os
import time
import re
import cv2
import random
import numpy

import settings
import image_processor
import adb_controller
import game_controller

def stop_app():
	print("Stop App....")
	adb_controller.stop_app()

def test_match():
	match_loc = image_processor.match_template(
		settings.screenshot_path,r"template_images/screenshot.png",0.05,True)

def test_wait_till_match():
	print("test_wait_until_match....")
	re = adb_controller.wait_till_match_any([r"template_images/screenshot.png"],[0.05],True,60,3)
	print("after test_wait_until_match....")

def test_match_and_click():
	print("match_and_click....")
	re = adb_controller.wait_to_match_and_click([r"template_images/screenshot.png"],[0.15],True,300,1.123)

def test_swip():
	print("test_swip....")
	adb_controller.swipe((500,360),(180,360),1000)

def test_wait_while_match():
	print("test_wait_while_match....")
	re = adb_controller.wait_while_match([r"template_images/clicktest3.png"],[0.01],600,3)
	print("after test_wait_while_match....")

def test_screenshot():
	adb_controller.screenshot(r"temp_screenshot/last_screenshot.png")

def test_screenUnChange():
	adb_controller.screenshot(r"temp_screenshot/last_screenshot.png")
	# do something
	time.sleep(1)
	adb_controller.screenshot(r"temp_screenshot/screenshot.png")
	if(image_processor.match_template(r"temp_screenshot/last_screenshot.png",r"temp_screenshot/screenshot.png",0.01,False) == (0,0)):
		print("screenUnChange....")

def test_click():
	adb_controller.click((100,200))

def test_match_text():
	# re2 = adb_controller.wait_till_match_any_text(settings.go_hire_stop_options,5,1,scope = (343,500,338,900))
	go_hire_stop_options = ["请重新登陆","您的账号登录已过期,请重新登录"]
	re = adb_controller.wait_till_match_any_text(go_hire_stop_options,5,1)
	if(re != None):
		print("Found text match: {}".format(str(go_hire_stop_options)))

def check_monster_reachable():
	adb_controller.screenshot(settings.screenshot_path)
	game_controller.close_target_panel()
	game_controller.cast_fire_ball()
	adb_controller.screenshot(settings.screenshot_path)
	if game_controller.close_target_panel():
		print("monster reachable")
		return True
	else:
		print("monster not reachable")
		return False

def check_exp_getting():
	start_exp = game_controller.read_exp_text()
	if(start_exp != None):
		start_exp = start_exp[:-1]
		print("start_exp: {}".format(str(start_exp)))
	time.sleep(1)
	end_exp = game_controller.read_exp_text()
	if(end_exp != None):
		end_exp = end_exp[:-1]
		print("end_exp: {}".format(str(end_exp)))
	if start_exp != end_exp:
		return True
	else:
		return False

def get_current_coordinate():
	coordinate_str = game_controller.read_coordinate_text()
	if coordinate_str == None:
		return get_current_coordinate1()
	coordinate_str = coordinate_str.replace("[","")
	coordinate_str = coordinate_str.replace("]","")
	coordinate = coordinate_str.split(",")

	#可能解析成点号
	if len(coordinate) != 2:
		coordinate = coordinate_str.split(".")

	#还不对，扩大区域再测一次
	if len(coordinate) != 2:
		return get_current_coordinate1()
	else:
		current_x = int(coordinate[0].replace(".",""))
		current_y = int(coordinate[1])
		print("current coordinate: {},{}".format(str(current_x), str(current_y)))
		if current_x != 0:
			settings.current_x = current_x
		if current_y != 0:
			settings.current_y = current_y
		return current_x, current_y


def get_current_coordinate1():
	coordinate_str = game_controller.read_coordinate_text()
	coordinate_str = coordinate_str.replace("[","")
	coordinate_str = coordinate_str.replace("]","")
	coordinate = coordinate_str.split(",")
	#可能解析成点号
	if len(coordinate) != 2:
		coordinate = coordinate_str.split(".")

	current_x = 0
	current_y = 0

	if len(coordinate) != 2:
		return current_x,current_y
	else:
		current_x = int(coordinate[0])
		current_y = int(coordinate[1])
		print("current coordinate: {},{}".format(str(current_x), str(current_y)))
		if current_x != 0:
			settings.current_x = current_x
		if current_y != 0:
			settings.current_y = current_y
		return current_x, current_y

def get_nearest_pos_index(cave_path):
	print("get_nearest_pos_index")
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
	print("nearest_index: {}".format(str(nearest_index)))
	return nearest_index

def go_to_next_point(cave_path):
	print("go_to_next_point path_index : {}".format(str(settings.current_path_index)))

	path_len = len(cave_path)
	settings.current_path_index = (settings.current_path_index + 1) % path_len
	move_to_index_of_path(settings.current_path_index, cave_path)

	if not check_monster_reachable():
		go_to_next_point(cave_path)

def move_to_index_of_path(path_index,path):
	target_pos = path[path_index]
	print("target_pos: {}".format(str(target_pos)))
	current_x = settings.current_x
	current_y = settings.current_y
	while current_x != target_pos[0] or current_y != target_pos[1]:
		game_controller.move_from_to((current_x, current_y), target_pos)
		current_x, current_y = get_current_coordinate()

def start_get_exp_at_zombie_cave():
	#前往距离最近的路径点
	settings.current_path_index = get_nearest_pos_index(settings.zombie_cave_path)
	move_to_index_of_path(settings.current_path_index, settings.zombie_cave_path)

	while(True):
		if check_exp_getting():
			print("经验有增加")
		else:
			print("经验没增加")
			#消除系统确定消息框
			game_controller.click_sure_btn()

			#检查等级，等级等于29且未拜师，停止练级
			lv = game_controller.read_lv_text()
			if (int(lv) == 29) and (not game_controller.already_has_master()):
				print("达到29级，请先去拜师，练级结束")
				return

			#移动到下一个点
			go_to_next_point(settings.zombie_cave_path)


def start_get_exp_at_centipede_cave():
	#前往距离最近的路径点
	settings.current_path_index = get_nearest_pos_index(settings.centipede_cave_path)
	move_to_index_of_path(settings.current_path_index, settings.centipede_cave_path)

	while(True):
		if check_exp_getting():
			print("经验有增加")
		else:
			print("经验没增加")
			#消除系统确定消息框
			game_controller.click_sure_btn()

			#移动到下一个点
			go_to_next_point(settings.centipede_cave_path)



# 僵尸洞
# start_get_exp_at_zombie_cave()

# 蜈蚣洞
start_get_exp_at_centipede_cave()
