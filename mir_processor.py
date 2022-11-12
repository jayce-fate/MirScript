import os
import time
import re
import cv2
import random

import settings
import image_processor
import adb_controller
import game_controller

def stop_app():
	print("Stop App....")
	adb_controller.stop_app()

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
	else:
		print("monster not reachable")

def check_exp_getting():
	start_exp = game_controller.read_exp_text()
	if(start_exp != None):
		start_exp = start_exp[:-1]
		print("start_exp: {}".format(str(start_exp)))
	time.sleep(10)
	end_exp = game_controller.read_exp_text()
	if(end_exp != None):
		end_exp = end_exp[:-1]
		print("end_exp: {}".format(str(end_exp)))

while(True):
	check_exp_getting()

	exit(0)
