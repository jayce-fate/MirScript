import os
import time
import re
import cv2
import random
import numpy
import _thread
import enums
from datetime import datetime

import map_controller
import pet_controller
import utils
import globals
import settings
import image_processor
import adb_controller
import game_controller
import path_controller
import skill_controller
import btn_controller
import user_controller
import match_controller

walk_swip_time = 200
run_swip_time = 550

block_point_cache = []

def get_joystick_pos():
    return utils.convert_point((275, 500), (1664, 936))

def one_step_walk_left():
    print("往左走一步....")
    joystick_pos = get_joystick_pos()
    adb_controller.swipe((joystick_pos[0] + 25, joystick_pos[1]), (joystick_pos[0] - 25, joystick_pos[1]), walk_swip_time)

def one_step_walk_right():
    print("往右走一步....")
    joystick_pos = get_joystick_pos()
    adb_controller.swipe((joystick_pos[0] - 25, joystick_pos[1]), (joystick_pos[0] + 25, joystick_pos[1]), walk_swip_time)

def one_step_walk_up():
    print("往上走一步....")
    joystick_pos = get_joystick_pos()
    adb_controller.swipe((joystick_pos[0], joystick_pos[1] + 25), (joystick_pos[0], joystick_pos[1] - 25), walk_swip_time)

def one_step_walk_down():
    print("往下走一步....")
    joystick_pos = get_joystick_pos()
    adb_controller.swipe((joystick_pos[0], joystick_pos[1] - 25), (joystick_pos[0], joystick_pos[1] + 25), walk_swip_time)

def one_step_walk_left_up():
    print("往左上走一步....")
    joystick_pos = get_joystick_pos()
    adb_controller.swipe((joystick_pos[0] + 25, joystick_pos[1] + 25), (joystick_pos[0] - 25, joystick_pos[1] - 25), walk_swip_time)

def one_step_walk_right_up():
    print("往右上走一步....")
    joystick_pos = get_joystick_pos()
    adb_controller.swipe((joystick_pos[0] - 25, joystick_pos[1] + 25), (joystick_pos[0] + 25, joystick_pos[1] - 25), walk_swip_time)

def one_step_walk_left_down():
    print("往左下走一步....")
    joystick_pos = get_joystick_pos()
    adb_controller.swipe((joystick_pos[0] + 25, joystick_pos[1] - 25), (joystick_pos[0] - 25, joystick_pos[1] + 25), walk_swip_time)

def one_step_walk_right_down():
    print("往右下走一步....")
    joystick_pos = get_joystick_pos()
    adb_controller.swipe((joystick_pos[0] - 25, joystick_pos[1] - 25), (joystick_pos[0] + 25, joystick_pos[1] + 25), walk_swip_time)


def move_by_path(path):
    # print("move_by_path:{}".format(str(path)))
    move_path = path.copy()
    if move_path == None:
        return

    path_length = len(move_path)
    if path_length < 2:
        return

    from_pos = move_path[0]
    to_pos = move_path[1]

    print("初始位置: {}".format(str(from_pos)))
    print("目标位置: {}".format(str(to_pos)))

    move_x = to_pos[0] - from_pos[0]
    move_y = to_pos[1] - from_pos[1]

    print("to_pos: {}".format(str(to_pos)))
    print("move_path[1]: {}".format(str(move_path[1])))
    if move_x > 0 and move_y > 0:
        one_step_walk_right_down()
    elif move_x > 0 and move_y < 0:
        one_step_walk_right_up()
    elif move_x < 0 and move_y > 0:
        one_step_walk_left_down()
    elif move_x < 0 and move_y < 0:
        one_step_walk_left_up()
    elif move_x > 0 and move_y == 0:
        one_step_walk_right()
    elif move_x < 0 and move_y == 0:
        one_step_walk_left()
    elif move_x == 0 and move_y > 0:
        one_step_walk_down()
    elif move_x == 0 and move_y < 0:
        one_step_walk_up()

    del(move_path[0])

    if len(move_path) >= 2:
        move_by_path(move_path)
    else:
        globals.expect_current_pos = (to_pos[0], to_pos[1])


def random_move_one_step():
    move_x = random.randint(-1, 1)
    move_y = random.randint(-1, 1)
    if move_x > 0 and move_y > 0:
        one_step_walk_right_down()
    elif move_x > 0 and move_y < 0:
        one_step_walk_right_up()
    elif move_x < 0 and move_y > 0:
        one_step_walk_left_down()
    elif move_x < 0 and move_y < 0:
        one_step_walk_left_up()
    elif move_x > 0 and move_y == 0:
        one_step_walk_right()
    elif move_x < 0 and move_y == 0:
        one_step_walk_left()
    elif move_x == 0 and move_y > 0:
        one_step_walk_down()
    elif move_x == 0 and move_y < 0:
        one_step_walk_up()

# 单步路径移动
def step_go_by_path(step_path, check_exp = False):
    if len(step_path) == 0:
        print("len(step_path) == 0")
        return
    print("step_go_by_path: {}".format(str(step_path)))
    # 目标坐标
    target_pos = step_path[len(step_path) - 1]
    # 刷新当前坐标
    get_current_coordinate()
    start_exp = 0
    if check_exp:
        start_exp = game_controller.read_current_exp(need_screenshot = False)
    # 最大尝试次数
    move_try_limit = settings.move_try_limit
    last_step_path = []
    while globals.current_pos[0] != target_pos[0] or globals.current_pos[1] != target_pos[1]:
        if move_try_limit > 0:
            move_try_limit = move_try_limit - 1

            if (globals.current_pos in step_path):
                index_of_current_pos = step_path.index(globals.current_pos)
                step_path = step_path[index_of_current_pos:]
            else:
                step_path = path_controller.find_path(globals.current_pos, target_pos)
                if len(step_path) > 2 * settings.one_time_move_distance:
                    break

            # print("step_path:{}".format(str(step_path)))
            if len(last_step_path) >= 2 and len(step_path) > 0 and last_step_path[0] == step_path[0]:
                next_pos = step_path[1]
                target_pos = step_path[-1]
                global block_point_cache
                if next_pos in block_point_cache:
                    # 目标位置被堵住，直接返回
                    if next_pos == target_pos:
                        return
                    print("set_block:{}".format(str(next_pos)))
                    block_point_cache.remove(next_pos)
                    path_controller.set_block(next_pos)
                    print("step_path[-1]:{}".format(str(target_pos)))
                    step_path = path_controller.find_path(globals.current_pos, target_pos)
                    if len(step_path) == 0:
                        path_not_find(target_pos)
                else:
                    block_point_cache.append(next_pos)

            move_by_path(step_path)

            last_step_path = step_path

            if check_exp:
                end_exp = game_controller.read_current_exp(need_screenshot = True)
                if start_exp != end_exp:
                    print("step_go_by_path过程中经验有增加，停止移动")
                    break
            else:
                time.sleep(1.0)
            get_current_coordinate()
        else:
            #检测断开消息框
            if match_controller.match_template("text_lost_connection") != None:
                print("lost_connection, 断开")
                raise Exception("RESTART")

            # 达到最大尝试次数，放弃，返回
            return


def go_to_next_point(cave_path, check_exp = False):
    # print("go_to_next_point")
    globals.current_pos = get_current_coordinate()

    path_len = len(cave_path)

    globals.current_path_index = (globals.current_path_index + settings.one_time_move_distance) % path_len
    target_pos = cave_path[globals.current_path_index]
    # print("globals.current_pos:{}".format(str(globals.current_pos)))
    # print("target_pos:{}".format(str(target_pos)))
    if globals.current_pos == target_pos:
        return
    path = path_controller.find_path(globals.current_pos, target_pos)
    # 允许 distance在范围内的路径移动（为了绕过障碍物）：settings.one_time_move_distance < distance < 2 * settings.one_time_move_distance
    if len(path) > 2 * settings.one_time_move_distance:
        target_pos = get_nearest_pos(cave_path)
        globals.current_path_index = cave_path.index(target_pos)
        path = path_controller.find_path(globals.current_pos, target_pos)

    if len(path) == 0:
        path_not_find(target_pos)

    step_go_by_path(path, check_exp)

def path_not_find(target_pos):
    print("未找到{}到{}的路径, 飞个随机+重启".format(str(globals.current_pos), str(target_pos)))
    skill_controller.cast_random_fly()
    raise Exception("RESTART_GET_EXP")

def go_to_previous_point(cave_path, check_exp = False):
    # print("go_to_previous_point")
    if globals.current_pos == (0, 0):
        get_current_coordinate()

    path_len = len(cave_path)

    globals.current_path_index = (path_len + globals.current_path_index - 2 * settings.one_time_move_distance) % path_len
    target_pos = cave_path[globals.current_path_index]
    # print("globals.current_pos:{}".format(str(globals.current_pos)))
    # print("target_pos:{}".format(str(target_pos)))
    if globals.current_pos == target_pos:
        return
    path = path_controller.find_path(globals.current_pos, target_pos)
    # 允许 distance在范围内的路径移动（为了绕过障碍物）：settings.one_time_move_distance < distance < 2 * settings.one_time_move_distance
    if len(path) > 3 * settings.one_time_move_distance:
        target_pos = get_nearest_pos(cave_path)
        globals.current_path_index = cave_path.index(target_pos)
        path = path_controller.find_path(globals.current_pos, target_pos)

    if len(path) == 0:
        path_not_find(target_pos)

    step_go_by_path(path, check_exp)


def get_nearest_pos(cave_path):
    current_pos = get_current_coordinate()
    print("current_pos: {}".format(str(current_pos)))
    path_len = len(cave_path)
    nearest_pos = cave_path[0]

    # 期望寻路范围
    min_index = globals.current_path_index - 3 * settings.one_time_move_distance
    max_index = globals.current_path_index + 3 * settings.one_time_move_distance + 1
    for index in range(min_index, max_index):
        path_index = (index + path_len) % path_len
        position = cave_path[path_index]
        current_pow = pow((position[0] - current_pos[0]), 2) + pow((position[1] - current_pos[1]), 2)
        nearest_pow = pow((nearest_pos[0] - current_pos[0]), 2) + pow((nearest_pos[1] - current_pos[1]), 2)
        if current_pow < nearest_pow:
            nearest_pos = position

    # 如果超出期望，则重新搜索全路径中最近的点
    path = path_controller.find_path(current_pos, nearest_pos)
    if len(path) > 3 * settings.one_time_move_distance:
        for index in range(1, path_len):
            position = cave_path[index]
            # print("position: {}".format(str(position)))
            current_pow = pow((position[0] - current_pos[0]), 2) + pow((position[1] - current_pos[1]), 2)
            # print("current_pow: {}".format(str(current_pow)))
            nearest_pow = pow((nearest_pos[0] - current_pos[0]), 2) + pow((nearest_pos[1] - current_pos[1]), 2)
            # print("nearest_pow: {}".format(str(nearest_pow)))
            if current_pow < nearest_pow:
                nearest_pos = position

    print("nearest_pos: {}".format(str(nearest_pos)))
    return nearest_pos


def get_current_coordinate():
    coordinate = game_controller.read_coordinate_text()
    if coordinate == None:
         print("当前坐标获取失败，可能地图被收起，尝试再次开关地图")
         # 尝试点击地图开关
         game_controller.open_or_close_map()
         time.sleep(0.2)
         #再次读取坐标
         coordinate = game_controller.read_coordinate_text()

    if coordinate == None:
        print("当前坐标获取失败，可能背包被打开，小地图被遮挡，或者游戏中断")
        if globals.read_coordinate_fail_remain > 0:
            globals.read_coordinate_fail_remain = globals.read_coordinate_fail_remain - 1
            print("尝试重新读取坐标，剩余次数:{}".format(str(globals.read_coordinate_fail_remain)))
            time.sleep(1.0)
            return get_current_coordinate()
        else:
            print("globals.read_coordinate_fail_remain<=0, 已达最大重试次数，尝试重启游戏")
            raise Exception("RESTART")

    if len(coordinate) != 2:
        print("len(coordinate) != 2")
        return get_current_coordinate_after_adjust()
    else:
        current_pos = (int(coordinate[0].replace(".","")), int(coordinate[1]))
        print("当前坐标: {}".format(str(current_pos)))
        if current_pos[0] != 0 and current_pos[1] != 0:
            # 重置最大失败重试次数
            globals.read_coordinate_fail_remain = settings.read_coordinate_fail_limit
            globals.current_pos = current_pos
            return current_pos
        else:
            if globals.read_coordinate_fail_remain > 0:
                globals.read_coordinate_fail_remain = globals.read_coordinate_fail_remain - 1
                print("尝试重新读取坐标，剩余次数:{}".format(str(globals.read_coordinate_fail_remain)))
                time.sleep(1.0)
                return get_current_coordinate()
            else:
                print("globals.read_coordinate_fail_remain<=0, 已达最大重试次数，尝试重启游戏")
                raise Exception("RESTART")


def get_current_coordinate_after_adjust():
    if globals.expect_current_pos[0] == 0 and globals.expect_current_pos[1] == 0:
        adjust_count = globals.adjust_count % 16
        if adjust_count == 0:
            one_step_walk_left()
        elif adjust_count == 1:
            one_step_walk_left_up()
        elif adjust_count == 2:
            one_step_walk_up()
        elif adjust_count == 3:
            one_step_walk_right_up()
        elif adjust_count == 4:
            one_step_walk_right()
        elif adjust_count == 5:
            one_step_walk_right_down()
        elif adjust_count == 6:
            one_step_walk_down()
        elif adjust_count == 7:
            one_step_walk_left_down()
        elif adjust_count == 8:
            one_step_walk_left()
            one_step_walk_left()
        elif adjust_count == 9:
            one_step_walk_left_up()
            one_step_walk_left_up()
        elif adjust_count == 10:
            one_step_walk_up()
            one_step_walk_up()
        elif adjust_count == 11:
            one_step_walk_right_up()
            one_step_walk_right_up()
        elif adjust_count == 12:
            one_step_walk_right()
            one_step_walk_right()
        elif adjust_count == 13:
            one_step_walk_right_down()
            one_step_walk_right_down()
        elif adjust_count == 14:
            one_step_walk_down()
            one_step_walk_down()
        elif adjust_count == 15:
            one_step_walk_left_down()
            one_step_walk_left_down()
        elif adjust_count == 16:
            one_step_walk_left()
            one_step_walk_left()
            one_step_walk_left()
        elif adjust_count == 17:
            one_step_walk_left_up()
            one_step_walk_left_up()
            one_step_walk_left_up()
        elif adjust_count == 18:
            one_step_walk_up()
            one_step_walk_up()
            one_step_walk_up()
        elif adjust_count == 19:
            one_step_walk_right_up()
            one_step_walk_right_up()
            one_step_walk_right_up()
        elif adjust_count == 20:
            one_step_walk_right()
            one_step_walk_right()
            one_step_walk_right()
        elif adjust_count == 21:
            one_step_walk_right_down()
            one_step_walk_right_down()
            one_step_walk_right_down()
        elif adjust_count == 22:
            one_step_walk_down()
            one_step_walk_down()
            one_step_walk_down()
        elif adjust_count == 23:
            one_step_walk_left_down()
            one_step_walk_left_down()
            one_step_walk_left_down()

        globals.adjust_count = adjust_count + 1
        return get_current_coordinate()
    else:
        print("use expect current coordinate: {}".format(str(globals.expect_current_pos)))
        return globals.expect_current_pos

def protect_routine():
    if user_controller.get_character_level() >= 23:
        if user_controller.get_character_occupation() == enums.Occupation.Taoist:
            # 自动寻路卡死使用技能无效，走两步来破解
            # one_step_walk_down()
            # one_step_walk_up()
            skill_controller.cast_invisible()
            invisible_time = time.time()
            skill_controller.cast_heal()
            pet_controller.reactive_pet()
            while game_controller.check_exp_getting():
                print("经验有增加")
                if time.time() - invisible_time > 12:
                    skill_controller.cast_invisible()
                    invisible_time = time.time()
                    skill_controller.cast_heal()

# 使用地图寻路
def navigate_to_point(target_pos, callback = None, callback1 = None, callback2 = None, callback3 = None, input_coordinate = True, unreachable_callback = None):
    #消除系统确定消息框
    game_controller.dismissSureDialog()

    current_pos = get_current_coordinate()
    far_from_target = abs(current_pos[0] - target_pos[0]) > 5 or abs(current_pos[1] - target_pos[1]) > 5
    if not far_from_target:
        path = [current_pos, target_pos]
        step_path = path_controller.to_each_step_path(path, False)
        move_by_path(step_path)
        if callback3 != None:
            callback3()
        if callback2 != None:
            callback2()
        if callback1 != None:
            callback1()
        if callback != None:
            callback()
        return

    map_name = game_controller.read_map_name()
    map_controller.open_map()
    # TODO:如果是盟重土城，则先关闭左下角npc列表

    if input_coordinate:
        point_str = "{},{}".format(target_pos[0], target_pos[1])
        map_controller.input_text(point_str)

    #判断目标是否可达
    # time.sleep(0.2)
    # adb_controller.screenshot(settings.screenshot_path)

    #不可达检测
    match_loc = image_processor.match_template(
        settings.screenshot_path,r"template_images/map_point_indicate_unreachable.png",0.05)
    if match_loc != None:
        print("找到map_point_indicate_unreachable，位置不可达")
        if unreachable_callback != None:
            unreachable_callback()
        else:
            print("重启")
            raise Exception("RESTART")

    btn_controller.click_btn("btn_xun_lu")
    game_controller.close_map()

    while True:
        current_pos1 = get_current_coordinate()
        print("current_pos1 {}".format(str(current_pos1)))
        current_map_name = game_controller.read_map_name()
        current_pos2 = get_current_coordinate()
        print("current_pos2 {}".format(str(current_pos2)))
        far_from_target = abs(current_pos2[0] - target_pos[0]) > 5 or abs(current_pos2[1] - target_pos[1]) > 5
        if current_map_name != None and len(current_map_name) >= 2 and map_name != current_map_name:
            print("current_map_name != None and len(current_map_name) >= 2 and map_name != current_map_name")
            if callback3 != None:
                callback3()
            if callback2 != None:
                callback2()
            if callback1 != None:
                callback1()
            if callback != None:
                callback()
            break
        elif far_from_target and current_pos1 == current_pos2:
            print("far_from_target and current_pos1 == current_pos2")
            # if not "盟重" in map_name:
            #     protect_routine()
            navigate_to_point(target_pos, callback, callback1, callback2, callback3, False)
            break
        elif not far_from_target and current_pos1 == current_pos2 and target_pos != current_pos2:
            print("not far_from_target and current_pos1 == current_pos2 and target_pos != current_pos2")
            if not "盟重" in map_name:
                protect_routine()
                current_pos2 = get_current_coordinate()
            path = [current_pos2, target_pos]
            step_path = path_controller.to_each_step_path(path, False)
            move_by_path(step_path)
            # if callback3 != None:
            #     callback3()
            # if callback2 != None:
            #     callback2()
            # if callback1 != None:
            #     callback1()
            # if callback != None:
            #     callback()
            # break
            continue
        elif target_pos == current_pos2:
            print("target_pos == current_pos2")
            game_controller.dismissSureDialog()
            adb_controller.screenshot(settings.screenshot_path)
            if callback3 != None:
                callback3()
            if callback2 != None:
                callback2()
            if callback1 != None:
                callback1()
            if callback != None:
                callback()
            break


def go_back_town_and_stay():
    skill_controller.cast_back_town()
    time.sleep(3.0)
    adb_controller.screenshot(settings.screenshot_path)
    navigate_to_point((338,338))
