import os
import time
import re
import cv2
import random

import image_processor
import adb_controller

while(True):
	print("current_time = {}".format(time.time()))
	re = adb_controller.wait_to_match_and_click([r"template_images/start1.png"],[0.15],True,300,1.123)
	exit(0)
