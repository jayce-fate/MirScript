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
# game_controller.is_bang_jin_item_list()
trash_controller.repair_all()
# t1 = time.time()
# my_lose_HP = game_controller.get_my_lose_HP()
# print("my_lose_HP = ", my_lose_HP)
# current_map_name = game_controller.read_map_name()
# print("current_map_name = ", current_map_name)
# print("time span = ", time.time() - t1)
# character.name = "郭襄"
# exp_controller.go_to_dark_area()
# trash_controller.batch_sell_item('bai_se_hu_chi_xiang_lian', force = False)
# character.name = "雷电将军"
# character.level = 1
# game_controller.restart_game()
# game_controller.select_character("雷电将军", 37)
# move_controller.random_move_one_step()
# path_controller.set_map_data("盟重土城")
# path = path_controller.find_path((824,631), (838,641))
# print("path = ", str(path))
# btn_controller.click_accept_ya_biao()
# time.sleep(0.5)
# adb_controller.screenshot(settings.screenshot_path)
# user_controller.get_character_name()
# exp_controller.get_subsidy()
# exp_controller.get_exp_subsidy()

# name = game_controller.read_character_name()
# print(name)
# occupation = game_controller.get_occupation()
# print(occupation)
# print(int(occupation))
# str2 = '<p>,<o>p3大傻逼啊1assd：//'
# res2 = re.sub("[^a-zA-Z0-9\u4e00-\u9fa5]", '', str2)
# print(res2)

# game_controller.read_character_name()
# item_list = {
#   "超级魔法药": 1,
#   "超级金创药": 1,
#   "随机传送卷包": 1,
#   "地牢逃脱卷": 1,
#   "棕色栗子": 1,
#   "黄色药粉(中)": 1,
#   "灰色药粉(中)": 1,
#   "护身符(大)": 1,
#   "魔法药中包": 1,
# }
# trash_controller.buy_items(item_list)
# btn_controller.click_item_menu_at_index(9)
# game_controller.get_my_health()
# game_controller.open_bag()
# btn_controller.click_right_menu("整理")
# game_controller.wipe_up_bag()
# time.sleep(0.5)
# trash_controller.drink_item("jun_xiang")
# trash_controller.batch_drink_item("ji_neng_shu")
# print(settings.device_address)
# globals.current_lvl = 7
# exp_controller.routine_lvl_seven()
# globals.current_lvl = 30
# trash_controller.batch_drink_item('ji_neng_shu')
# btn_controller.click_right_menu('出售')
# item_list = {
#     "护身符(大)": 12,
#     "超级魔法药": 12,
#     "地牢逃脱卷": 1,
#     "随机传送卷": 3,
#     "棕色栗子": 1,
# }
# shortage_list = trash_controller.get_supply_shortage_list(item_list)
# trash_controller.buy_items(shortage_list)
# trash_controller.count_trashes()
# trash_controller.sell_trashes()
# while btn_controller.click_sure_btn():
#     adb_controller.screenshot(settings.screenshot_path)
# btn_controller.click_btn_login()
# exp_controller.restart_routine()
# if game_controller.is_save_power_mode():
#     print("省电")
# game_controller.read_pet_HP()
# btn_controller.click_npc_meng_zhong_lao_bing()
# btn_controller.click_transfer_cave("骷髅洞")
# exp_controller.fly_to_exp_map()
# item_list = {
#   "超级金创药": 6,
# }
# trash_controller.buy_items(item_list)
# btn_controller.click_right_menu("商店")
# time.sleep(1)
# adb_controller.screenshot(settings.screenshot_path)
# btn_controller.click_left_menu("绑金")
# trash_controller.batch_drink_item("mo_fa_yao_zhong_liang")
# btn_controller.click_msg_box("知道了")
# btn_controller.click_sure_btn()
# trash_controller.drink_item("wu_mu_jian")
# exp_controller.fly_to_exp_map()
# image_processor.show_hsv_tool("temp_screenshot/screenshot_debug.png")
# exp_controller.fly_to_exp_map()
# move_controller.go_to_town()
# skill_controller.cast_back_town()
# skill_controller.cast_heal()
# skill_controller.cast_invisible()
# exp_controller.restart_routine()
# game_controller.read_lv_area_text()
# trash_controller.loop_drop_one_item("ji_neng_shu")
# move_controller.get_current_coordinate()
# path_controller.set_map_data()
# trash_controller.collect_ground_treasures()
# skill_controller.cast_defence()
# skill_controller.cast_heal()
# skill_controller.cast_invisible()
# adb_controller.input_text("100,100")
# trash_controller.drop_trashes()
# trash_controller.drink_item("qiang_xiao_jin_chuang_yao")
# btn_controller.click_confirm_batch_use()
# image_processor.show_hsv_tool("template_images/skill_all1.png")
# skill_controller.cast_shield()

# exp_controller.restart_routine(True)
# adb_controller.restart_emulator()
# exp_controller.restart_routine(True)
# btn_controller.click_npc_lu_lao_ban()
# btn_controller.click_finish_ya_biao()

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

# skill_controller.cast_shield()

# path_controller.generate_map_data([(115,133),(110,140)])
# game_controller.close_map()
# start_get_exp()
# path_controller.show_map()

# adb_controller.restart_emulator()
# exp_controller.retart_routine()
# adb_controller.restart_adb()
# adb_controller.stop_app()
# adb_controller.start_app()

# adb_controller.screenshot(settings.screenshot_path)
# btn_controller.click_npc_wen_biao_tou()

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
