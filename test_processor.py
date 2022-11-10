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

while(True):
	# stop_app()

	test_match_and_click()

	exit(0)
