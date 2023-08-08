import os
import time
import re
import cv2
import random
import numpy
from datetime import datetime
from datetime import timedelta

import globals
import settings
import image_processor
import adb_controller
import game_controller
import path_controller
import move_controller
import exp_controller
import ya_biao_controller
import trash_controller
import skill_controller
import btn_controller
import utils
import user_controller
import character

# ******************************************
# test
# ******************************************
adb_controller.connect()
adb_controller.screenshot(settings.screenshot_path)

# result = game_controller.read_bind_gold()
# print("result: {}".format(str(result)))

# result = game_controller.read_current_exp()
# print("result: {}".format(str(result)))

# image_processor.show_hsv_tool(settings.screenshot_path)

current_pet_max_HP = game_controller.get_pet_current_max_HP()
print("current_pet_max_HP: {}".format(str(current_pet_max_HP)))

# match_scope = (132,160,400,580)
# match_scope = utils.convert_scope(match_scope, (1664, 936))
# image_processor.show_hsv_tool(settings.screenshot_debug, match_scope)
