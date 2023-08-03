import os
import time
import re
import cv2
import random
import numpy
from datetime import datetime

import globals
import settings
import utils
import image_processor
import adb_controller
import game_controller
import path_controller
import move_controller
import trash_controller
import skill_controller
import btn_controller
import user_controller
import enums
import ya_biao_controller
import match_controller

def summon_pet():
    print('道士重新召唤宝宝')
    if user_controller.get_character_level() >= 35:
        if not skill_controller.cast_dog():
            skill_controller.cast_skeleton()
            skill_controller.cast_skeleton()
    else:
        if not skill_controller.cast_skeleton():
            print("学习召唤骷髅")
            game_controller.open_bag_and_drink("ji_neng_shu", batch=True)
            skill_controller.cast_skeleton()

def wait_till_max_lvl_max():
    print("wait_till_max_lvl_max")
    game_controller.reactive_pet()
    # 当前等级最大血量
    current_pet_max_HP = game_controller.get_pet_current_max_HP()
    # 可以达到的最大血量
    pet_max_HP = game_controller.get_pet_max_HP()
    print("current_pet_max_HP: {}".format(str(current_pet_max_HP)))
    print("pet_max_HP: {}".format(str(pet_max_HP)))
    if current_pet_max_HP == 0:
        print("current_pet_max_HP == 0")
        if user_controller.get_character_occupation() == enums.Occupation.Taoist:
            summon_pet()

    read_pet_current_max_HP_retry_times = 60
    while current_pet_max_HP != pet_max_HP:
        time.sleep(10)
        game_controller.dismissSureDialog(False)
        current_pet_max_HP = game_controller.get_pet_current_max_HP()
        pet_max_HP = game_controller.get_pet_max_HP()
        print("current_pet_max_HP: {}".format(str(current_pet_max_HP)))
        print("pet_max_HP: {}".format(str(pet_max_HP)))
        if current_pet_max_HP == 0:
            print("read_pet_current_max_HP_retry_times: {}".format(str(read_pet_current_max_HP_retry_times)))
            read_pet_current_max_HP_retry_times = read_pet_current_max_HP_retry_times - 1
            if read_pet_current_max_HP_retry_times <= 0:
                print("read_pet_current_max_HP_retry_times <= 0")
                raise Exception("RESTART")

    print("pet HP reach Max")
    #消除省电模式
    if game_controller.is_save_power_mode():
        btn_controller.click_center_of_screen()
        adb_controller.screenshot(settings.screenshot_path)

    go_back_town_and_fly()


def go_back_town_and_fly():
    print("go_back_town_and_fly")
    # 回城
    move_controller.navigate_to_point((339,338), fly_to_exp_map)

def go_back_town_and_restart():
    print("go_back_town_and_restart")
    skill_controller.cast_back_town()
    time.sleep(2.0)
    start()

def fly_to_exp_map():
    print("fly_to_exp_map")
    game_controller.dismissSureDialog()

    #领取低保
    if user_controller.can_get_subsidy():
        get_subsidy()

    #领取经验
    if user_controller.can_get_exp_subsidy():
        get_exp_subsidy()

    #老兵等目标血量面板会挡住绑金数字
    game_controller.close_target_panel()
    bind_gold = game_controller.get_bag_bind_gold(keep_open=True)
    #补给
    buy_supplies(bind_gold)
    adb_controller.screenshot(settings.screenshot_path)

    #道士检查是否学习隐身术，否者买一本
    if user_controller.get_character_occupation() == enums.Occupation.Taoist and user_controller.get_character_level() >= 20 and user_controller.get_character_level() <= 25:
        if not skill_controller.cast_invisible():
            item_list = {
              "隐身术": 1,
            }
            trash_controller.buy_books(item_list)
            adb_controller.screenshot(settings.screenshot_path)
            game_controller.open_bag_and_drink("ji_neng_shu", batch=True)
            globals.skill_invisible_exist = True

    #宝宝是否需要挂等级
    if user_controller.get_character_level() >= 17 and not is_pet_level_max():
        go_to_sheep_yard()
        return

    if not btn_controller.click_npc_meng_zhong_lao_bing():
        raise Exception("RESTART")
    time.sleep(2.0)
    adb_controller.screenshot(settings.screenshot_path)
    if not btn_controller.click_yellow_menu("传送"):
        raise Exception("RESTART")
    time.sleep(1.0)
    adb_controller.screenshot(settings.screenshot_path)
    if user_controller.get_character_level() < 17:
        btn_controller.click_transfer_cave("骷髅洞")
    elif user_controller.get_character_level() < 35:
        btn_controller.click_transfer_cave("废矿入口")
    else:
        btn_controller.click_transfer_cave("死亡山谷")

    btn_controller.click_btn_confirm_transform()
    time.sleep(5.0)
    adb_controller.screenshot(settings.screenshot_path)
    map_name = game_controller.read_map_name()
    if user_controller.get_character_level() < 17:
        if map_name == "骷髅洞1层":
            get_exp_by_random_fly(map_name)
        else:
            start()
    elif user_controller.get_character_level() < 35:
        if map_name == "比奇矿区":
            go_to_east_waste_ore()
        else:
            start()
    else:
        if map_name == "比奇矿区":
            go_to_east_waste_ore()
        # elif "地" in map_name and "层东" in map_name:
        elif map_name == "地牢一层东":
            go_to_dark_area()
        elif map_name == "黑暗地带":
            go_to_between_life_and_dead()
        else:
            start()


def get_exp_by_random_fly(map_name):
    print("get_exp_by_random_fly")

    #吃栗子
    game_controller.eat_li_zi()

    no_more_random_fly = 0
    start_exp = game_controller.read_current_exp()
    start_time = time.time()
    while True:
        if time.time() - start_time > 120:
            current_map_name = game_controller.read_map_name()
            if current_map_name != None and len(current_map_name) >= 2 and map_name != current_map_name:
                print("current_map_name != None and len(current_map_name) >= 2 and map_name != current_map_name")
                print("map_name = ", map_name)
                print("current_map_name = ", current_map_name)
                raise Exception("RESTART")

            current_exp = game_controller.read_current_exp()
            if current_exp != start_exp:
                start_exp = game_controller.read_current_exp()
                start_time = time.time()
            else:
                print("get_exp_by_random_fly,经过180秒经验没增加，重启")
                raise Exception("RESTART")

        game_controller.dismissSureDialog(False)
        adb_controller.screenshot(settings.screenshot_path)
        if not game_controller.template_exist("btn_close_target"):
            # skill_controller.cast_poison()
            skill_controller.cast_talisman()
            adb_controller.screenshot(settings.screenshot_path)
            if not game_controller.template_exist("btn_close_target"):
                pos_before_fly = move_controller.get_current_coordinate()
                skill_controller.cast_random_fly()
                # skill_controller.cast_poison()
                skill_controller.cast_talisman()
                pos_after_fly = move_controller.get_current_coordinate()
                if pos_before_fly == pos_after_fly:
                    no_more_random_fly = no_more_random_fly + 1
                if no_more_random_fly >= 2:
                    game_controller.dismissSureDialog()
                    print("学习召唤骷髅")
                    adb_controller.screenshot(settings.screenshot_path)
                    game_controller.open_bag_and_drink("ji_neng_shu", batch=True)
                    adb_controller.screenshot(settings.screenshot_path)
                    go_back_town_and_restart()
                    break


# 去废矿东部
def go_to_east_waste_ore():
    print("go_to_east_waste_ore")
    # 拜师了，说明有传衣服，到了飞随机，否则有点脆，就不飞随机了
    # 这里在那时只有道士用，所以使用隐身术没判断职业
    if user_controller.get_character_has_master():
        move_controller.navigate_to_point((179,110), start, skill_controller.cast_random_fly, skill_controller.cast_invisible)
    else:
        move_controller.navigate_to_point((179,110), start, skill_controller.cast_invisible)


# 去黑暗地带
def go_to_dark_area():
    print("go_to_dark_area")
    move_controller.navigate_to_point((149,55), go_to_between_life_and_dead, skill_controller.cast_random_fly, skill_controller.cast_invisible)

# 去生死之间
def go_to_between_life_and_dead():
    print("go_to_between_life_and_dead")
    move_controller.navigate_to_point((202,187), start, skill_controller.cast_random_fly, skill_controller.cast_invisible)

def do_some_attack():
    start_exp = game_controller.read_current_exp()
    for index in range(10):
        skill_controller.cast_attack()

    game_controller.dismissSureDialog(directly=False)

    end_exp = game_controller.read_current_exp()
    #防止呆住攻击不生效
    if start_exp == end_exp:
        move_controller.random_move_one_step()

def routine_lvl_one():
    print("routine_lvl_one")

    #记录角色创建时间
    user_controller.set_character_create_time()

    if btn_controller.click_msg_box("如何移动"):
        time.sleep(15)
        adb_controller.screenshot(settings.screenshot_path)
        btn_controller.click_msg_box("开始")

    #设置随机，回城，药水快捷键
    if btn_controller.click_setting():
        time.sleep(1.0)
        adb_controller.screenshot(settings.screenshot_path)
        btn_controller.click_setting_menu("技能")
        time.sleep(0.5)
        #
        adb_controller.click(utils.convert_point((1408, 256), (1664, 936)))
        adb_controller.click(utils.convert_point((192, 78), (1664, 936)))
        #
        adb_controller.click(utils.convert_point((1506, 256), (1664, 936)))
        adb_controller.click(utils.convert_point((192, 184), (1664, 936)))
        #
        adb_controller.click(utils.convert_point((1610, 256), (1664, 936)))
        adb_controller.click(utils.convert_point((192, 290), (1664, 936)))
        #
        adb_controller.click(utils.convert_point((1408, 364), (1664, 936)))
        adb_controller.click(utils.convert_point((192, 390), (1664, 936)))
        #
        adb_controller.click(utils.convert_point((1506, 364), (1664, 936)))
        adb_controller.click(utils.convert_point((192, 500), (1664, 936)))
        #
        adb_controller.click(utils.convert_point((1610, 364), (1664, 936)))
        adb_controller.click(utils.convert_point((192, 602), (1664, 936)))
    btn_controller.click_left_return()

    #穿装备
    game_controller.open_bag()
    time.sleep(1.0)
    game_controller.wipe_up_bag()
    time.sleep(0.5)
    trash_controller.drink_item("bu_yi_nan")
    trash_controller.drink_item("bu_yi_nv")
    trash_controller.drink_item("wu_mu_jian")
    btn_controller.click_left_return()
    btn_controller.click_right_return()
    level = user_controller.get_character_level(refresh=True)
    while level < 7:
        do_some_attack()
        # 等级取原始值
        level = user_controller.get_character_level(refresh = True, use_raw_level = True)
        is_legal_level = utils.is_legal_level(level)
        #以防断线游戏被关闭
        if not is_legal_level:
            print(" not is_legal_level")
            raise Exception("RESTART")

    print("等级7")
    time.sleep(3.0)
    game_controller.dismissSureDialog()

    routine_lvl_seven()


def routine_lvl_seven():
    print("routine_lvl_seven")
    if user_controller.get_character_level() == 7:
        game_controller.open_bag()
        time.sleep(1.0)
        btn_controller.click_btn("right_btn_arrange", (136,770,1532,1642), need_screenshot=True)
        game_controller.wipe_up_bag()
        time.sleep(0.5)
        trash_controller.drink_item("jun_xiang")
        time.sleep(4.0)
        trash_controller.batch_drink_item("ji_neng_shu")
        trash_controller.drink_item("tie_jian")
        trash_controller.batch_drink_item("bo_li_jie_zhi")

        btn_controller.click_left_return()
        btn_controller.click_right_return()

    adb_controller.screenshot(settings.screenshot_path)

    level = user_controller.get_character_level()
    while level < 15:
        if user_controller.get_character_occupation() == enums.Occupation.Taoist:
            do_some_attack()
        elif user_controller.get_character_occupation() == enums.Occupation.Magician:
            skill_controller.cast_fire_ball()
            adb_controller.screenshot(settings.screenshot_path)
        # 等级取原始值
        level = user_controller.get_character_level(refresh = True, use_raw_level = True)
        is_legal_level = utils.is_legal_level(level)
        #以防断线游戏被关闭
        if not is_legal_level:
            print(" not is_legal_level")
            raise Exception("RESTART")

    print("等级15")
    time.sleep(35)

    routine_lvl_fifteen()


def routine_lvl_fifteen():
    print("routine_lvl_fifteen")
    adb_controller.screenshot(settings.screenshot_path)
    btn_controller.click_msg_box("知道了")

    game_controller.dismissSureDialog()

    if user_controller.get_character_level() == 15:
        if game_controller.get_bag_remain_capacity(keep_open = True) > 32:
            # 穿装备，学技能
            # game_controller.open_bag()
            btn_controller.click_btn("right_btn_arrange", (136,770,1532,1642))
            game_controller.wipe_up_bag()
            time.sleep(0.5)
            trash_controller.drink_item("jun_xiang")
            time.sleep(4.0)
            trash_controller.batch_drink_item("ji_neng_shu")
            if user_controller.get_character_occupation() == enums.Occupation.Taoist:
                trash_controller.drink_item("ban_yue_wan_dao")
                trash_controller.drink_item("da_shou_zhuo")
                trash_controller.drink_item("zhen_zhu_jie_zhi")
            #穿衣服
            trash_controller.drink_item("qing_xing_kui_jia_nv")
            trash_controller.drink_item("qing_xing_kui_jia_nan")
            #丢垃圾
            trash_controller.drop_binding_trashes(False)
            btn_controller.click_left_return()
            btn_controller.click_right_return()
            time.sleep(1.0)
        else:
            btn_controller.click_left_return()
            btn_controller.click_right_return()

    go_back_town_and_fly()


# def go_back_town_and_get_subsidy():
#     print("go_back_town_and_get_subsidy")
#     # 回城
#     move_controller.navigate_to_point((338,338), get_subsidy)

#领取低保
def get_subsidy():
    print("get_subsidy")
    game_controller.dismissSureDialog()

    adb_controller.screenshot(settings.screenshot_path)
    btn_controller.click_npc_meng_zhong_lao_bing()
    time.sleep(2.0)
    adb_controller.screenshot(settings.screenshot_path)
    game_controller.wipe_down_npc_dialog_menu()
    adb_controller.screenshot(settings.screenshot_path)
    if btn_controller.click_yellow_menu("领取低保"):
        user_controller.set_subsidy_time()
    btn_controller.click_left_return()

def get_exp_subsidy():
    print("get_yesterday_exp_subsidy")
    game_controller.dismissSureDialog()

    adb_controller.screenshot(settings.screenshot_path)
    btn_controller.click_npc_meng_zhong_lao_bing()
    time.sleep(2.0)
    adb_controller.screenshot(settings.screenshot_path)
    btn_controller.click_yellow_menu("纯手动练级补助")
    time.sleep(1.0)
    adb_controller.screenshot(settings.screenshot_path)
    if btn_controller.click_yellow_menu("马上领取"):
        user_controller.set_exp_subsidy_time()
    btn_controller.click_left_return()

def buy_supplies(bind_gold):
    print("buy_supplies bind_gold = ", bind_gold)
    game_controller.dismissSureDialog()
    adb_controller.screenshot(settings.screenshot_path)

    item_list = {
    }
    buy_li_zi_amount = 0
    if bind_gold > 240000:
        buy_li_zi_amount = 5
    elif bind_gold > 210000:
        buy_li_zi_amount = 4
    elif bind_gold > 180000:
        buy_li_zi_amount = 3
    elif bind_gold > 150000:
        buy_li_zi_amount = 2
    elif bind_gold > 120000:
        buy_li_zi_amount = 1

    character_level = user_controller.get_character_level()
    if character_level >= 35:
        buy_li_zi_amount = 0
    elif character_level < 17 and buy_li_zi_amount > 1:
        buy_li_zi_amount = 1
    elif character_level < 22 and buy_li_zi_amount > 2:
        buy_li_zi_amount = 2

    print("buy_li_zi_amount = ", buy_li_zi_amount)
    if character_level < 17:
        item_list = {
          "超级魔法药": 8,
          "超级金创药": 3,
          "随机传送卷包": 9,
          "地牢逃脱卷": 1,
          "棕色栗子": buy_li_zi_amount,
          # "黄色药粉(中)": 1,
          # "灰色药粉(中)": 1,
          "护身符(大)": 5,
          "技能书": 0,
          "技能书激活": 0,
          "回城卷": 0,
          "魔法药小量": 0,
          "魔法药中包": 0,
          "金创药小量": 0,
          "军饷": 0,
        }
    elif character_level < 22:
        item_list = {
            "护身符(大)": 12,
            "超级魔法药": 12,
            "超级金创药": 3,
            "地牢逃脱卷": 1,
            "随机传送卷": 3,
            "棕色栗子": buy_li_zi_amount,
            "回城卷": 0,
        }
    else:
        item_list = {
            "护身符(大)": 12,
            "超级魔法药": 9,
            "超级金创药": 1,
            "地牢逃脱卷": 1,
            "随机传送卷": 3,
            "棕色栗子": buy_li_zi_amount,
            "回城卷": 0,
        }

    shortage_list = trash_controller.get_supply_shortage_list(item_list)
    trash_controller.buy_items(shortage_list)

    # 刚买完，设置背包里有栗子
    user_controller.set_li_zi_in_bag(True)

def start_get_exp():
    print("开始练级")
    adb_controller.connect()
    #消除省电模式（为什么这里要判断？）
    # if game_controller.is_save_power_mode():
    #     btn_controller.click_center_of_screen()

    adb_controller.screenshot(settings.screenshot_path)
    #地图名称
    map_name = game_controller.read_map_name()

    #获取等级
    count = 0
    while user_controller.get_character_level(refresh=True) <= 0 and count < 3:
        count = count + 1
    if user_controller.get_character_level() <= 0:
        print("user_controller.get_character_level() <= 0")
        raise Exception("RESTART")

    if 1 < user_controller.get_character_level() and user_controller.get_character_level() < 15:
        #检测是否设置随机和回城
        if not skill_controller.cast_random_fly(False):
            for index in range(30):
                print("技能未设置随机和回城快捷键")
            print("not skill_controller.cast_random_fly(False)")
            raise Exception("RESTART")

    #和平模式
    game_controller.set_mode_peace()

    if user_controller.get_character_level() < 7:
        routine_lvl_one()
        return
    elif user_controller.get_character_level() < 15:
        routine_lvl_seven()
        return
    elif user_controller.get_character_level() < 17:
        if map_name == "盟重土城":
            routine_lvl_fifteen()
        elif map_name == "骷髅洞1层": #骷髅两个字不识别
            get_exp_by_random_fly(map_name)
        else:
            print("unknown map_name:", map_name)
            raise Exception("RESTART")
        return
    if not game_controller.active_pet():
        print('当前没有宠物')
        if user_controller.get_character_occupation() == enums.Occupation.Taoist:
            summon_pet()
        elif user_controller.get_character_occupation() == enums.Occupation.Magician:
            print("法师直接下线换道士")
            return
    else:
        if user_controller.get_character_occupation() == enums.Occupation.Taoist:
            print('虽然有宝宝了，再用一下召唤宝宝，为了初始化globals.skill_xxx_pos')
            summon_pet()

    if "盟重" in map_name:
        print("当前位置，盟重土城")

        #判断是否可以押镖
        if user_controller.can_ya_biao():
            ya_biao_controller.start()
            return

        go_back_town_and_fly()

    elif map_name == "骷髅洞1层": #骷髅两个字不识别
        get_exp_by_random_fly(map_name)
        return
    elif map_name == "比奇矿区":
        go_to_east_waste_ore()
        return
    # elif "地" in map_name and "层东" in map_name:
    elif map_name == "地牢一层东":
        go_to_dark_area()
        return
    elif map_name == "黑暗地带":
        go_to_between_life_and_dead()
        return
    elif map_name == "生死之间":
        if user_controller.get_character_occupation() == enums.Occupation.Taoist:
            settings.one_time_move_distance = 4

    cave_path = game_controller.get_map_path(map_name)
    if len(cave_path) == 0:
        print("地图数据为空，回城重来")
        skill_controller.cast_back_town()
        time.sleep(3.0)
        start()
        return

    path_controller.set_map_data()

    # 转换为单步路径
    cave_path = path_controller.to_each_step_path(cave_path)

    nearest_pos = move_controller.get_nearest_pos(cave_path)
    globals.current_path_index = cave_path.index(nearest_pos)
    last_move_time = 0
    last_go_back_time = 0

    # 吃栗子，保护一下
    game_controller.do_self_protect()
    game_controller.eat_li_zi()

    while(True):
        game_controller.do_self_protect()
        #检查血量
        my_lose_HP = game_controller.get_my_lose_HP()
        # 道士，移动完，先判断血量隐身
        if user_controller.get_character_occupation() == enums.Occupation.Taoist:
            if 20 < my_lose_HP:
                skill_controller.cast_heal()
                skill_controller.cast_invisible()
                if game_controller.got_MP_Insufficient_text():
                    trash_controller.try_get_bag_space(1)
        # 法师血量低，可能背包满了，红喝不出来
        elif user_controller.get_character_occupation() == enums.Occupation.Magician:
            if 90 < my_lose_HP:
                trash_controller.try_get_bag_space(1)

        game_controller.dismissSureDialog(False)
        #检测断开消息框
        if match_controller.match_template("text_lost_connection"):
            print("lost_connection, 断开")
            raise Exception("RESTART")

        game_controller.do_self_protect()
        if not game_controller.check_level():
            raise Exception("NeedGetMaster")

        game_controller.do_self_protect()
        # 法师安全，先捡东西
        if user_controller.get_character_occupation() == enums.Occupation.Magician:
            if trash_controller.collect_ground_treasures() > 0:
                continue

        game_controller.do_self_protect()
        #判断是否可以领取经验
        if user_controller.can_get_exp_subsidy():
            go_back_town_and_restart()

        #判断是否可以押镖
        if user_controller.can_ya_biao():
            go_back_town_and_restart()

        game_controller.update_last_exp()
        #检查宝宝血量是否健康
        if not game_controller.is_pet_healthy():
            if game_controller.select_boss():
                # 攻击boss
                if user_controller.get_character_occupation() == enums.Occupation.Taoist:
                    # skill_controller.cast_poison()
                    skill_controller.cast_defence()
                    skill_controller.cast_heal()
                    skill_controller.cast_talisman()
                elif user_controller.get_character_occupation() == enums.Occupation.Magician:
                    skill_controller.cast_shield()
                    skill_controller.cast_lighting()
            else:
                if time.time() - last_go_back_time > settings.go_back_check_time:
                    # 往回跑，试图召回宠物
                    game_controller.reactive_pet()
                    if user_controller.get_character_occupation() == enums.Occupation.Taoist:
                        skill_controller.cast_invisible()
                    elif user_controller.get_character_occupation() == enums.Occupation.Magician:
                        skill_controller.cast_shield()
                    move_controller.go_to_previous_point(cave_path, user_controller.get_character_level() < 35)
                    # 移动结束接隐身
                    if user_controller.get_character_occupation() == enums.Occupation.Taoist:
                        skill_controller.cast_invisible()
                    game_controller.reactive_pet()
                    last_go_back_time = time.time()

            time.sleep(5.0)
            continue

        game_controller.do_self_protect()
        if game_controller.check_exp_getting():
            print("经验有增加")
            if time.time() - last_move_time > settings.move_check_time:
                while not game_controller.is_monster_nearby():
                    print("距离上次移动已达{}s，检查当前屏幕无怪，去下一个点".format(str(settings.move_check_time)))
                    move_controller.go_to_next_point(cave_path, user_controller.get_character_level() < 35)
                    # 移动结束接隐身
                    if user_controller.get_character_occupation() == enums.Occupation.Taoist:
                        skill_controller.cast_invisible()
                    last_move_time = time.time()
        else:
            print("经验没增加")
            # 道士不安全，没怪再捡东西
            if user_controller.get_character_occupation() == enums.Occupation.Taoist:
                if trash_controller.collect_ground_treasures() > 0:
                    continue

            #移动到下一个点
            move_controller.go_to_next_point(cave_path, user_controller.get_character_level() < 35)
            # 移动结束接隐身
            if user_controller.get_character_occupation() == enums.Occupation.Taoist:
                skill_controller.cast_invisible()
            last_move_time = time.time()
            while not game_controller.is_monster_nearby():
                move_controller.go_to_next_point(cave_path, user_controller.get_character_level() < 35)
                # 移动结束接隐身
                if user_controller.get_character_occupation() == enums.Occupation.Taoist:
                    skill_controller.cast_invisible()
                last_move_time = time.time()

def is_pet_level_max():
    if user_controller.get_character_occupation() == enums.Occupation.Taoist:
        # 当前等级最大血量
        current_pet_max_HP = game_controller.get_pet_current_max_HP()
        # 可以达到的最大血量
        pet_max_HP = game_controller.get_pet_max_HP()
        print("current_pet_max_HP: {}".format(str(current_pet_max_HP)))
        if current_pet_max_HP == 0:
            raise Exception("TEST")
        print("pet_max_HP: {}".format(str(pet_max_HP)))
        if current_pet_max_HP != pet_max_HP:
            print("current_pet_max_HP != pet_max_HP")
            return False
        else:
            return True
    return True

def go_to_sheep_yard():
    print("go_to_sheep_yard")
    sheep_yard_pos = (random.randint(186,228),random.randint(255,280))
    print("sheep_yard_pos: {}".format(str(sheep_yard_pos)))
    move_controller.navigate_to_point(sheep_yard_pos, wait_till_max_lvl_max, unreachable_callback=go_to_sheep_yard)

def restart_routine(restart_emulator_adb = False):
    try:
        print("重启游戏")

        game_controller.restart_game()
        success = game_controller.wait_till_finish_login(240, 1)
        if success:
            print("click login btn success")
            start()
        else:
            print("click login btn failed")
            restart_routine()
    except Exception as e:
        print('exception:', e)
        reason = e.args[0]
        if reason == "RESTART":
            restart_routine()
        elif "NoneType" in reason:
            print("adb 可能断开")
            restart_routine(True)
        else:
            restart_routine()


def start():
    try:
        start_get_exp()
    except Exception as e:
        print('exception:', e)
        reason = e.args[0]
        if reason == "RESTART":
            restart_routine()
        elif reason == "RESTART_GET_EXP":
            start()
        elif reason == "NeedGetMaster":
            print("到达必须拜师等级，停止程序")
            # 回城站着
            move_controller.go_back_town_and_stay()
        elif "NoneType" in reason:
            print("adb 可能断开")
            restart_routine(True)
        elif reason == "TEST":
            print("TEST")
            restart_routine()
        else:
            restart_routine()
