import os
import time
import re
import cv2
import random

import image_processor
import adb_controller

def stop_app():
	print("Stop App....")
	adb_controller.stop_app()

def test_match_and_click():
	print("match_and_click....")
	re = adb_controller.wait_to_match_and_click([r"template_images/clicktest2.png"],[0.15],True,300,1.123)

def test_wait_till_match():
	print("test_wait_until_match....")
	re = adb_controller.wait_till_match_any([r"template_images/clicktest3.png"],[0.05],True,60,3)
	print("after test_wait_until_match....")

def test_swip():
	print("test_swip....")
	adb_controller.swipe((500,360),(180,360),1000)

def test_wait_while_match():
	print("test_wait_while_match....")
	re = adb_controller.wait_while_match([r"template_images/clicktest3.png"],[0.01],600,3)
	print("after test_wait_while_match....")

while(True):
	# stop_app()

	# test_match_and_click()

	test_wait_till_match()

	# test_swip()

	# test_wait_while_match()

	exit(0)
