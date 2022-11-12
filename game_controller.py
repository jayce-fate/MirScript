import os
import time
import re
import cv2

import adb_controller
import image_processor
import settings

def one_step_walk_left():
	print("one_step_walk_left....")
	adb_controller.swipe((300,600),(250,600),1000)

def one_step_walk_right():
	print("one_step_walk_right....")
	adb_controller.swipe((300,600),(350,600),1000)

def one_step_walk_up():
	print("one_step_walk_up....")
	adb_controller.swipe((300,600),(300,550),1000)

def one_step_walk_down():
	print("one_step_walk_down....")
	adb_controller.swipe((300,600),(300,650),1000)

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

def read_lv_text():
	re = adb_controller.read_text(scope = (56,100,58,104))
	if(re != None):
		print("lv text Found: {}".format(str(re)))
		return re

def read_exp_text():
	re = adb_controller.read_text(scope = (56,100,181,316))
	if(re != None):
		# print("exp text Found: {}".format(str(re)))
		return re

def click_sure_btn():
	print("click_sure_btn....")
	match_loc = image_processor.match_template(
		settings.screenshot_path,r"template_images/btn_sure.png",0.05,True)
	if(match_loc != None):
		adb_controller.click(match_loc)