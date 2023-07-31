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
btn_controller.click_confirm()
# print("bind_gold: {}".format(str(bind_gold)))
