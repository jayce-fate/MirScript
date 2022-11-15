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

def get_monster_list():
	print("获取怪物列表....")
	lower_color = [0,0,118]
	upper_color = [179,255,255]
	result = image_processor.easyocr_read_cn(settings.screenshot_path,(24,870,948,1512),lower_color,upper_color)
	for reline in result:
		re_text = reline[1].replace(" ","")
		print("monster name Found: {}".format(str(re_text)))
	return result

def close_target_panel():
	print("close_target_panel....")
	match_loc = image_processor.match_template(
		settings.screenshot_path,r"template_images/btn_target_close.png",0.05)
	if(match_loc != None):
		adb_controller.click(match_loc)
		return True
	else:
		return False

def cast_fire_ball():
	print("cast_fire_ball....")
	match_loc = image_processor.match_template(
		settings.screenshot_path,r"template_images/skill_fire_ball.png",0.05)
	if(match_loc != None):
		adb_controller.click(match_loc)

def open_target_list():
	print("open_target_list....")
	adb_controller.click((1185, 584))

def open_monster_list():
	print("open_monster_list....")
	match_loc = image_processor.match_template(
		settings.screenshot_path,r"template_images/btn_monster.png",0.6)
	if(match_loc != None):
		adb_controller.click(match_loc)

def close_target_list():
	print("close_target_list....")
	match_loc = image_processor.match_template(
		settings.screenshot_path,r"template_images/btn_return.png",0.05)
	if(match_loc != None):
		adb_controller.click(match_loc)

def read_coordinate_text():
	adb_controller.screenshot(settings.screenshot_path)
	# 坐标颜色绿色参数
	lower_color = [35,43,46]
	upper_color = [75,255,255]
	result = image_processor.easyocr_read_en(settings.screenshot_path,(42,82,1550,1660),lower_color,upper_color)
	for reline in result:
		re_text = reline[1].replace(" ","")
		re_text = re.findall(r'\d+', re_text)
		if(len(re_text) != 0):
			print("coordinate text Found: {}".format(str(re_text)))
		return re_text
	return None

def read_lv_text():
	# 等级颜色米色参数
	lower_color = [0,0,212]
	upper_color = [179,255,255]
	result = image_processor.easyocr_read_en(settings.screenshot_path,(56,100,58,104),lower_color,upper_color)
	for reline in result:
		re_text = reline[1].replace(" ","")
		re_text = re.findall(r'\d+', re_text)
		if(len(re_text) != 0):
			print("lv text Found: {}".format(str(re_text[0])))
			return re_text[0]
		else:
			return -1

# 不截屏读取文字
def read_text_direct(scope = None):
	result = image_processor.easyocr_read_cn(settings.screenshot_path,scope = scope)
	for reline in result:
		re_text = reline[1].replace(" ","")
		return re_text

def already_has_master():
	re = read_text_direct(scope = (450,482,742,918))
	if(re != None):
		print("master text Found: {}".format(str(re)))
		if "徒" in re or "的" in re or "弟" in re:
			return True
	return False

def read_current_exp():
	adb_controller.screenshot(settings.screenshot_path)
	# 经验颜色米色参数
	lower_color = [0,0,212]
	upper_color = [179,255,255]
	result = image_processor.easyocr_read_en(settings.screenshot_path,(56,100,181,316),lower_color,upper_color)
	for reline in result:
		re_text = reline[1].replace(" ","")
		if(re_text != None):
			# print("exp text Found: {}".format(str(re_text)))
			digit_array = re.findall(r'\d+\.?\d*', re_text)
			# print("digit_array: {}".format(str(digit_array)))
			for index in range(0,len(digit_array)):
				return float(digit_array[index])
	return None

def click_sure_btn():
	print("click_sure_btn....")

	# 公告可能会连续出三次
	for tab_index in range(0,3):
		adb_controller.screenshot(settings.screenshot_path)
		match_loc = image_processor.match_template(
			settings.screenshot_path,r"template_images/btn_sure.png",0.05)
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

	if move_count > 20:
		print("invalid move_count: {}, give up".format(str(move_count)))
		return

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
	else:
		settings.expect_current_x = to_pos[0]
		settings.expect_current_y = to_pos[1]
