import os
import time
import re
import cv2
import random
import numpy
import datetime

import globals
import settings
import utils
import image_processor
import adb_controller
import game_controller
import path_controller
import move_controller
import btn_controller


def start_ya_biao():
    print("开始押镖")
    adb_controller.connect()

    path_controller.set_map_data("盟重土城")
    go_to_wen_biao_tou()
    go_to_lu_lao_ban()


def go_to_wen_biao_tou():
    game_controller.dismissSureDialog()

    target_pos = (439, 206)
    btn_controller.click_map()
    time.sleep(1.0)
    adb_controller.screenshot(settings.screenshot_path)
    btn_controller.click_map_aim()
    btn_controller.click_map_input()
    btn_controller.click_map_input()
    btn_controller.click_map_clear()
    point_str = "{},{}".format(target_pos[0], target_pos[1])
    adb_controller.input_text(point_str)
    btn_controller.click_map_edit_confirm()
    btn_controller.click_map_input_confirm()
    btn_controller.click_xun_lu()
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

def go_to_lu_lao_ban():
    cave_path = settings.ya_biao_full_path
    cave_path_length = len(cave_path)
    if cave_path_length == 0:
        print("程序结束")
        return

    move_controller.get_current_coordinate()
    # # 先去路径开始点
    # path = path_controller.find_path(globals.current_pos, cave_path[0])
    # move_controller.step_go_by_path(path)
    # # 再沿固定路径去陆老板
    # move_controller.step_go_by_path(cave_path)


    # 直接搜索寻路去陆老板
    # for idx in range(1, 5):
    #     index = int(cave_path_length / 4 * idx)
    #     if index >= cave_path_length:
    #         index = cave_path_length - 1
    #     path = path_controller.find_path(globals.current_pos, cave_path[index])
    #     move_controller.step_go_by_path(path)

    # 先去最近点
    next_pos = move_controller.get_nearest_pos(cave_path)
    current_path_index = cave_path.index(next_pos)

    while True:
        game_controller.dismissSureDialog(False)

        path = path_controller.find_path(globals.current_pos, next_pos)
        move_controller.step_go_by_path(path)

        if current_path_index == cave_path_length - 1:
            break

        current_path_index = current_path_index + int(cave_path_length / 4)
        if current_path_index >= cave_path_length:
            current_path_index = cave_path_length - 1
        next_pos = cave_path[current_path_index]


    # 等双倍时间
    while should_wait_until_double_time():
        time.sleep(10)

    #交付
    adb_controller.screenshot(settings.screenshot_path)
    btn_controller.click_npc_lu_lao_ban()
    time.sleep(1.0)
    btn_controller.click_finish_ya_biao()


def should_wait_until_double_time():
    # 范围时间
    time_min = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '19:00', '%Y-%m-%d%H:%M')
    time_max = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '20:01', '%Y-%m-%d%H:%M')

    # 当前时间
    current_time = datetime.datetime.now()

    # 判断当前时间是否在范围时间内
    if current_time > time_min and current_time < time_max:
        return True
    else:
        return False


def start():
    start_ya_biao()
