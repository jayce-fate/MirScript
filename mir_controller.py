import os
import time
import re
import cv2
import random
import numpy
import datetime

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

# ******************************************
# test
# ******************************************
# adb_controller.screenshot(settings.screenshot_path)
# game_controller.show_scope()

# game_controller.cast_shield()

# path_controller.generate_map_data()
# game_controller.close_map()
# start_get_exp()
# path_controller.show_map()

# adb_controller.restart_mumu()
# exp_controller.retart_routine()
# adb_controller.restart_adb()
# adb_controller.stop_app()
# adb_controller.start_app()

# adb_controller.screenshot(settings.screenshot_path)
# game_controller.click_npc_wen_biao_tou()

# path_controller.set_map_data("盟重土城")
# ya_biao_controller.go_to_lu_lao_ban()
#
# adb_controller.screenshot(settings.screenshot_path)
# match_loc = image_processor.multiple_match_template(
# 	settings.screenshot_path,r"template_images/ground_treasures/gold_m.png",0.005)

# path_controller.set_map_data()
# trash_controller.collect_ground_treasures()

# image_processor.show_hsv_tool(settings.screenshot_path)

# adb_controller.screenshot(settings.screenshot_path)

# game_controller.reactive_pet()
