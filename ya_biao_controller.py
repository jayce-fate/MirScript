import os
import time
import re
import cv2
import random
import numpy
from datetime import datetime

import globals
import map_controller
import settings
import utils
import image_processor
import adb_controller
import game_controller
import path_controller
import move_controller
import btn_controller
import exp_controller
import user_controller


def start_ya_biao():
    print("开始押镖")
    adb_controller.connect()

    path_controller.set_map_data("盟重土城")
    go_to_wen_biao_tou()
    # go_to_lu_lao_ban()

def go_to_wen_biao_tou():
    game_controller.dismissSureDialog()

    target_pos = (441, 206)
    map_controller.open_map()
    point_str = "{},{}".format(target_pos[0], target_pos[1])
    map_controller.input_text(point_str)
    btn_controller.click_btn("btn_xun_lu")
    game_controller.close_map()

    while True:
        time.sleep(1.0)
        current_pos1 = move_controller.get_current_coordinate()
        print("current_pos1 {}".format(str(current_pos1)))
        time.sleep(1.0)
        current_pos2 = move_controller.get_current_coordinate()
        print("current_pos2 {}".format(str(current_pos2)))
        far_from_target = abs(current_pos1[0] - target_pos[0]) > 5 or abs(current_pos1[1] - target_pos[1]) > 5
        if far_from_target and current_pos1 == current_pos2:
            print("far_from_target and current_pos1 == current_pos2")
            go_to_wen_biao_tou()
            break
        elif not far_from_target and current_pos1 == current_pos2:
            print("not far_from_target and current_pos1 == current_pos2")
            game_controller.dismissSureDialog(False)
            adb_controller.screenshot(settings.screenshot_path)
            if btn_controller.click_npc_wen_biao_tou():
                break
            time.sleep(0.1)

    #改为点击固定点
    adb_controller.screenshot(settings.screenshot_path)
    btn_controller.click_accept_ya_biao()
    time.sleep(0.5)
    if game_controller.get_already_ya_biao_text():
        print("already ya biao")
        user_controller.set_ya_biao_time()
        print("开始练级")
        exp_controller.start()
    else:
        print("not yet ya biao")
        go_to_lu_lao_ban()

def go_to_lu_lao_ban():
    cave_path = settings.ya_biao_full_path
    cave_path_length = len(cave_path)
    if cave_path_length == 0:
        print("cave_path_length == 0, 程序结束")
        return

    # 转换为单步路径
    step_path = path_controller.to_each_step_path(cave_path, False)
    step_path_len = len(step_path)

    # 刷新globals.current_pos
    move_controller.get_current_coordinate()

    # 先去最近点
    next_pos = move_controller.get_nearest_pos(cave_path)
    print("next_pos: {}".format(str(next_pos)))
    current_path_index = cave_path.index(next_pos)
    print("current_path_index: {}".format(str(current_path_index)))

    fail_count = 0
    while True:
        game_controller.dismissSureDialog(False)

        path = path_controller.find_path(globals.current_pos, next_pos)
        if len(path) == 0:
            print("len(path) == 0")
            fail_count = fail_count + 1
            current_pos = move_controller.get_current_coordinate()
            print("current_pos: {}".format(str(current_pos)))
            # 最近点
            nearest_pos = step_path[0]
            for index in range(0, step_path_len):
                position = step_path[index]
                current_pow = pow((position[0] - current_pos[0]), 2) + pow((position[1] - current_pos[1]), 2)
                nearest_pow = pow((nearest_pos[0] - current_pos[0]), 2) + pow((nearest_pos[1] - current_pos[1]), 2)
                if current_pow < nearest_pow:
                    nearest_pos = position

            print("nearest_pos: {}".format(str(nearest_pos)))
            path = path_controller.to_each_step_path([current_pos, nearest_pos], False)
            move_controller.move_by_path(path)

            current_pos = move_controller.get_current_coordinate()
            if nearest_pos[0] != current_pos[0] or nearest_pos[1] != current_pos[1]:
                if abs(nearest_pos[0] - current_pos[0]) >= 3 or abs(nearest_pos[1] - current_pos[1]) >= 3:
                    move_controller.navigate_to_point(nearest_pos)

            if fail_count > 10:
                print("开始练级")
                exp_controller.start()
                return
        else:
            move_controller.step_go_by_path(path)

        if current_path_index == cave_path_length - 1:
            print("current_path_index == cave_path_length - 1")
            break

        current_path_index = current_path_index + int(cave_path_length / 8)
        if current_path_index >= cave_path_length:
            print("current_path_index >= cave_path_length")
            current_path_index = cave_path_length - 1
            print("current_path_index: {}".format(str(current_path_index)))
        next_pos = cave_path[current_path_index]
        print("next_pos: {}".format(str(next_pos)))


    # 等双倍时间
    print("等双倍时间")
    while should_wait_until_double_time():
        time.sleep(10)

    #交付
    print("交付")
    adb_controller.screenshot(settings.screenshot_path)
    if not btn_controller.click_npc_lu_lao_ban():
        print("not btn_controller.click_npc_lu_lao_ban()")
        go_to_lu_lao_ban()
    else:
        time.sleep(1.0)
        btn_controller.click_finish_ya_biao()

        user_controller.set_ya_biao_time()
        print("开始练级")
        exp_controller.start()

def should_wait_until_double_time():
    # 范围时间
    time_min = datetime.strptime(str(datetime.now().date()) + '19:00', '%Y-%m-%d%H:%M')
    time_max = datetime.strptime(str(datetime.now().date()) + '20:01', '%Y-%m-%d%H:%M')

    # 当前时间
    current_time = datetime.now()

    # 判断当前时间是否在范围时间内
    if current_time > time_min and current_time < time_max:
        return True
    else:
        return False


def restart_routine():
    try:
        print("重启游戏")
        game_controller.restart_game()
        success = game_controller.wait_till_finish_login(120, 1)
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
            restart_routine()
        else:
            restart_routine()

def start():
    try:
        start_ya_biao()
    except Exception as e:
        print('exception:', e)
        reason = e.args[0]
        if reason == "RESTART":
            restart_routine()
        elif "NoneType" in reason:
            restart_routine()
        else:
            restart_routine()
