import os
import time
import re
import cv2

import adb_controller
import image_processor
import settings

def one_step_walk_left():
	print("one_step_walk_left....")
	adb_controller.swipe((300,600),(250,600),500)

def one_step_walk_right():
	print("one_step_walk_right....")
	adb_controller.swipe((300,600),(350,600),500)

def one_step_walk_up():
	print("one_step_walk_up....")
	adb_controller.swipe((300,600),(300,550),500)

def one_step_walk_down():
	print("one_step_walk_down....")
	adb_controller.swipe((300,600),(300,650),500)

def one_step_walk_left_up():
	print("one_step_walk_left_up....")
	adb_controller.swipe((300,600),(250,550),500)

def one_step_walk_right_up():
	print("one_step_walk_right_up....")
	adb_controller.swipe((300,600),(350,550),500)

def one_step_walk_left_down():
	print("one_step_walk_left_down....")
	adb_controller.swipe((300,600),(250,650),500)

def one_step_walk_right_down():
	print("one_step_walk_right_down....")
	adb_controller.swipe((300,600),(350,650),500)

def one_step_run_left():
	print("one_step_run_left....")
	adb_controller.swipe((400,600),(100,600),200)

def one_step_run_right():
	print("one_step_run_right....")
	adb_controller.swipe((400,600),(700,600),200)

def one_step_run_up():
	print("one_step_run_up....")
	adb_controller.swipe((400,600),(400,300),200)

def one_step_run_down():
	print("one_step_run_down....")
	adb_controller.swipe((400,600),(400,900),200)

def one_step_run_left_up():
	print("one_step_run_left_up....")
	adb_controller.swipe((400,600),(100,300),200)

def one_step_run_right_up():
	print("one_step_run_right_up....")
	adb_controller.swipe((400,600),(700,300),200)

def one_step_run_left_down():
	print("one_step_run_left_down....")
	adb_controller.swipe((400,600),(100,900),200)

def one_step_run_right_down():
	print("one_step_run_right_down....")
	adb_controller.swipe((400,600),(700,900),200)

def close_target_panel():
	print("close_target_panel....")
	match_loc = image_processor.match_template(
		settings.screenshot_path,r"template_images/btn_target_close.png",0.05,True)
	if(match_loc != None):
		adb_controller.click(match_loc)
		return True
	else:
		return False

def cast_fire_ball():
	print("cast_fire_ball....")
	match_loc = image_processor.match_template(
		settings.screenshot_path,r"template_images/skill_fire_ball.png",0.05,True)
	if(match_loc != None):
		adb_controller.click(match_loc)

def read_coordinate_text():
	re = adb_controller.read_text(scope = (42,82,1550,1660))
	if(re != None):
		print("coordinate text Found: {}".format(str(re)))
		return re

def read_coordinate_text1():
	re = adb_controller.read_text(scope = (32,92,1540,1670))
	if(re != None):
		print("coordinate text Found: {}".format(str(re)))
		return re

def read_lv_text():
	re = adb_controller.read_text_direct(scope = (56,100,58,104))
	if(re != None):
		print("lv text Found: {}".format(str(re)))
		return re

def already_has_master():
	re = adb_controller.read_text_direct(scope = (450,482,742,918))
	if(re != None):
		print("master text Found: {}".format(str(re)))
		if "徒弟" in re:
			return True
	return False

def read_exp_text():
	re = adb_controller.read_text(scope = (56,100,181,316))
	if(re != None):
		# print("exp text Found: {}".format(str(re)))
		return re

def click_sure_btn():
	print("click_sure_btn....")

	# 公告可能会连续出三次
	for tab_index in range(0,3):
		adb_controller.screenshot(settings.screenshot_path)
		match_loc = image_processor.match_template(
			settings.screenshot_path,r"template_images/btn_sure.png",0.05,True)
		if(match_loc != None):
			adb_controller.click(match_loc)
		else:
			time.sleep(0.001)


def move_from_to(from_pos, to_pos):
	print("move from pos: {}".format(str(from_pos)))
	print("move to pos: {}".format(str(to_pos)))

	move_x = to_pos[0] - from_pos[0]
	move_y = to_pos[1] - from_pos[1]

	abs_move_x = abs(move_x)
	abs_move_y = abs(move_y)

	move_count = abs_move_x
	if abs_move_x != 0 and abs_move_y != 0:
		move_count = abs_move_x
		if abs_move_y < abs_move_x:
			move_count = abs_move_y
	elif abs_move_x == 0:
		move_count = abs_move_y
	elif abs_move_y == 0:
		move_count = abs_move_x

	updated_from_pos = list(from_pos)
	print("begin while move_count: {}".format(str(move_count)))
	while move_count > 0:
		print("move_count: {}".format(str(move_count)))
		step = 1
		if move_count > 1:
			step = 2

		if move_x > 0 and move_y > 0:
			updated_from_pos[0] = updated_from_pos[0] + step
			updated_from_pos[1] = updated_from_pos[1] + step
			if step == 2:
				one_step_run_right_down()
			else:
				one_step_walk_right_down()
		elif move_x > 0 and move_y < 0:
			updated_from_pos[0] = updated_from_pos[0] + step
			updated_from_pos[1] = updated_from_pos[1] - step
			if step == 2:
				one_step_run_right_up()
			else:
				one_step_walk_right_up()
		elif move_x < 0 and move_y > 0:
			updated_from_pos[0] = updated_from_pos[0] - step
			updated_from_pos[1] = updated_from_pos[1] + step
			if step == 2:
				one_step_run_left_down()
			else:
				one_step_walk_left_down()
		elif move_x < 0 and move_y < 0:
			updated_from_pos[0] = updated_from_pos[0] - step
			updated_from_pos[1] = updated_from_pos[1] - step
			if step == 2:
				one_step_run_left_up()
			else:
				one_step_walk_left_up()
		elif move_x > 0 and move_y == 0:
			updated_from_pos[0] = updated_from_pos[0] + step
			if step == 2:
				one_step_run_right()
			else:
				one_step_walk_right()
		elif move_x < 0 and move_y == 0:
			updated_from_pos[0] = updated_from_pos[0] - step
			if step == 2:
				one_step_run_left()
			else:
				one_step_walk_left()
		elif move_x == 0 and move_y > 0:
			updated_from_pos[1] = updated_from_pos[1] + step
			if step == 2:
				one_step_run_down()
			else:
				one_step_walk_down()
		elif move_x == 0 and move_y < 0:
			updated_from_pos[1] = updated_from_pos[1] - step
			if step == 2:
				one_step_run_up()
			else:
				one_step_walk_up()
		move_count = move_count - step

	if to_pos[0] - updated_from_pos[0] != 0 or to_pos[1] - updated_from_pos[1] != 0:
		move_from_to(tuple(updated_from_pos), to_pos)
