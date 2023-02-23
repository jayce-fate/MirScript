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
adb_controller.connect()
adb_controller.screenshot(settings.screenshot_path)
# game_controller.click_btn_login()
# exp_controller.restart_routine()
# if game_controller.is_save_power_mode():
#     print("省电")
# game_controller.read_pet_HP()
# game_controller.click_npc_meng_zhong_lao_bing()
# game_controller.click_transfer_cave("骷髅洞")
# exp_controller.fly_to_exp_map()
# item_list = {
#   "超级金创药": 6,
# }
# trash_controller.buy_items(item_list)
# game_controller.click_right_menu("商店")
# time.sleep(1)
# adb_controller.screenshot(settings.screenshot_path)
# game_controller.click_left_menu("绑金")
# game_controller.batch_drink_item("mo_fa_yao_zhong_liang")
# game_controller.click_msg_box("知道了")
# game_controller.click_sure_btn()
# game_controller.drink_item("wu_mu_jian")
# exp_controller.fly_to_exp_map()
# image_processor.show_hsv_tool("temp_screenshot/screenshot_debug.png")
# exp_controller.fly_to_exp_map()
# move_controller.go_to_town()
# game_controller.cast_back_town()
# game_controller.cast_heal()
# game_controller.cast_invisible()
# move_controller.navigate_to_point((338,338))
# exp_controller.restart_routine()
# game_controller.read_lv_area_text()
# trash_controller.loop_drop_one_item("ji_neng_shu")
# move_controller.get_current_coordinate()
# path_controller.set_map_data()
# trash_controller.collect_ground_treasures()
# game_controller.cast_defence()
# game_controller.cast_heal()
# game_controller.cast_invisible()
# adb_controller.input_text("100,100")
# trash_controller.drop_trashes()
# game_controller.drink_item("qiang_xiao_jin_chuang_yao")
# game_controller.click_confirm_batch_use()
# image_processor.show_hsv_tool("template_images/skill_all1.png")
# game_controller.cast_shield()
# game_controller.set_occupation()
# print("occupation = ", globals.occupation)

# exp_controller.restart_routine(True)
# adb_controller.restart_emulator()
# exp_controller.restart_routine(True)
# game_controller.click_npc_lu_lao_ban()
# game_controller.click_finish_ya_biao()

# trash_controller.try_get_bag_space(2)


# game_controller.close_map()
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

# cave_path = [(480,308), (491,337)]
# cave_path = game_controller.to_each_step_path(cave_path)
# path_controller.generate_map_data(cave_path)
#
# cave_path = [(680,513), (709,539)]
# cave_path = game_controller.to_each_step_path(cave_path)
# path_controller.generate_map_data(cave_path)

# path_controller.generate_map_data([(110,92),(92,108),(114,136),(162,177),(166,128),(49,93),(40,54),(47,39)])
# game_controller.close_map()
# start_get_exp()
# path_controller.show_map()

# adb_controller.restart_emulator()
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
#     settings.screenshot_path,r"template_images/ground_treasures/gold_m.png",0.005)

# path_controller.set_map_data()
# trash_controller.collect_ground_treasures()

# image_processor.show_hsv_tool(settings.screenshot_path)

# adb_controller.screenshot(settings.screenshot_path)

# game_controller.reactive_pet()
