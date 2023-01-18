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
import utils

# ******************************************
# test
# ******************************************

# adb_controller.screenshot(settings.screenshot_path)
# game_controller.read_map_name()

# masks = []
# masks.append((0,34,440,1234)) #顶部滚动通知
# masks.append((42,198,1354,1664)) #右上角地图
# masks.append((796,936,625,1196)) #底部聊天窗口
# print("masks 0 = ", masks)
# masks = utils.convert_masks(masks)
# print("masks 1 = ", masks)


# path_controller.show_map()

# game_controller.select_boss()

# trash_controller.loop_drink_one_item("强效魔法药")

# trash_controller.handle_bag_full()
# trash_name = game_controller.filter_trash_name("白色虎齿项链年雪霜万年雪霜")
# print("trash_name = ", trash_name)

# adb_controller.screenshot(settings.screenshot_path)
# game_controller.show_scope()

# game_controller.cast_shield()

# path_controller.generate_map_data([(110,92),(92,108),(114,136),(162,177),(166,128),(49,93),(40,54),(47,39)])
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
