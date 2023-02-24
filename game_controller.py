import os
import time
import re
import cv2
import random

import adb_controller
import image_processor
import settings
import globals
import utils

walk_swip_time = 200
run_swip_time = 550

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

def get_first_result(resultss):
    for idx in range(len(resultss)):
        results = resultss[idx]
        for result in results:
            rec = result[1] #('43', 0.99934321641922)
            # print("rec: {}".format(str(rec)))
            res = rec[0] #'43'
            # print("res: {}".format(str(res)))
            return res
    return None

def get_monster_list():
    print("获取怪物列表:")
    #打开目标列表
    open_target_list()
    time.sleep(0.2)

    #切换到怪物列表
    adb_controller.screenshot(settings.screenshot_path)
    open_monster_list()
    time.sleep(0.1)

    #识别怪物名称
    adb_controller.screenshot(settings.screenshot_path)
    lower_color = [0,0,118]
    upper_color = [179,255,255]

    match_scope = (24,870,948,1512)
    match_scope = utils.convert_scope(match_scope, (1664, 936))

    monster_list = []
    resultss = image_processor.paddleocr_read(settings.screenshot_path, match_scope, lower_color, upper_color)
    for idx in range(len(resultss)):
        results = resultss[idx]
        for result in results:
            rec = result[1] #('43', 0.99934321641922)
            # print("rec: {}".format(str(rec)))
            res = rec[0] #'43'
            # print("res: {}".format(str(res)))
            print("怪物名: {}".format(str(res)))
        monster_list = results
        break

    if len(monster_list) == 0:
        print("怪物列表为空")
    #关闭目标列表
    close_target_list()
    return monster_list


# 关闭怪物信息面板（等级、名称、血量）
def close_target_panel():
    print("关闭怪物信息....")
    match_loc = image_processor.match_template(
        settings.screenshot_path,r"template_images/btn_target_close.png",0.05)
    if(match_loc != None):
        adb_controller.click(match_loc)
        return True
    else:
        return False

def open_target_list():
    # print("open_target_list....")
    point = utils.convert_point((1185, 584), (1664, 936))
    adb_controller.click(point)

def open_monster_list():
    # print("open_monster_list....")
    match_scope = (561,627,1525,1632)
    match_scope = utils.convert_scope(match_scope, (1664, 936))

    match_loc = image_processor.match_template(
        settings.screenshot_path, r"template_images/btn_monster.png", 0.02, match_scope)
    if(match_loc != None):
        adb_controller.click(match_loc)

def close_target_list():
    # print("close_target_list....")
    match_scope = (850,892,1576,1628)
    match_scope = utils.convert_scope(match_scope, (1664, 936))

    match_loc = image_processor.match_template(
        settings.screenshot_path,r"template_images/btn_return.png",0.05,match_scope)
    if(match_loc != None):
        adb_controller.click(match_loc)

def open_or_close_map():
    # print("open_or_close_map....")
    match_scope = (0,41,1636,1664)
    match_scope = utils.convert_scope(match_scope, (1664, 936))

    match_loc = image_processor.match_template(
        settings.screenshot_path,r"template_images/map_bar.png",0.05,match_scope)
    if(match_loc != None):
        adb_controller.click(match_loc)

def read_coordinate_text(need_screenshot = True):
    if need_screenshot:
        adb_controller.screenshot(settings.screenshot_path)

    # 坐标颜色绿色参数
    lower_color = [35,43,46]
    upper_color = [75,255,255]

    match_scope = (42,82,1540,1664)
    match_scope = utils.convert_scope(match_scope, (1664, 936))

    resultss = image_processor.paddleocr_read(settings.screenshot_path, match_scope, lower_color, upper_color)
    result = get_first_result(resultss)
    if result != None:
        result = re.findall(r'\d+', result)
        # print("当前坐标: {}".format(str(result)))
        return result
    return None

def read_lv_text():
    # 等级颜色米色参数
    lower_color = [0,0,212]
    upper_color = [179,255,255]

    match_scope = (56,100,58,104)
    match_scope = utils.convert_scope(match_scope, (1664, 936))

    resultss = image_processor.paddleocr_read(settings.screenshot_path, match_scope, lower_color, upper_color)
    result = get_first_result(resultss)
    if result != None:
        print("当前等级1: {}".format(str(result)))
        result = result.replace('.', ''); # 去掉小数点
        digit_array = re.findall(r'\d+', result)
        globals.current_lvl = int(digit_array[0])
        print("globals.current_lvl: {}".format(str(globals.current_lvl)))
        return globals.current_lvl
    return -1

# Lv.xx
def read_lv_area_text():
    # 等级颜色米色参数
    lower_color = [0,0,212]
    upper_color = [179,255,255]

    match_scope = (56,100,0,104)
    match_scope = utils.convert_scope(match_scope, (1664, 936))

    resultss = image_processor.paddleocr_read(settings.screenshot_path, match_scope, lower_color, upper_color)
    result = get_first_result(resultss)
    if result != None:
        print("等级区域文字: {}".format(str(result)))
        return result
    return ""


def connection_lose():
    # adb_controller.screenshot(settings.screenshot_path)
    # 等级颜色米色参数
    lower_color = [0,0,212]
    upper_color = [179,255,255]

    match_scope = (390,462,620,1023)
    match_scope = utils.convert_scope(match_scope, (1664, 936))

    resultss = image_processor.paddleocr_read(settings.screenshot_path, match_scope, lower_color, upper_color)
    result = get_first_result(resultss)
    if result != None:
        print("当前提示文字: {}".format(str(result)))
        if "断开" in result:
            return True
    return False

def already_has_master():
    print("检查是否已拜师....")
    lower_color = [0,0,0]
    upper_color = [0,0,255]

    match_scope = (450,482,722,938)
    match_scope = utils.convert_scope(match_scope, (1664, 936))

    resultss = image_processor.paddleocr_read(settings.screenshot_path, match_scope, lower_color, upper_color)
    result = get_first_result(resultss)
    if result != None:
        print("我的名字: {}".format(str(result)))
        if "徒" in result or "弟" in result or "[" in result or "]" in result:
            print("当前已拜师")
            return True
    print("当前未拜师")
    return False

def read_current_exp():
    adb_controller.screenshot(settings.screenshot_path)
    # 经验颜色米色参数
    lower_color = [0,0,212]
    upper_color = [179,255,255]

    match_scope = (56,100,181,316)
    match_scope = utils.convert_scope(match_scope, (1664, 936))

    resultss = image_processor.paddleocr_read(settings.screenshot_path, match_scope, lower_color, upper_color)
    result = get_first_result(resultss)
    if result != None:
        digit_array = re.findall(r'\d+\.?\d*', result)
        for index in range(0,len(digit_array)):
            current_exp = digit_array[index]
            # print("当前经验: {}".format(str(current_exp)))
            return float(current_exp)
    return None


def read_tip_text():
    adb_controller.screenshot(settings.screenshot_path)
    # 颜色参数
    lower_color = [14,255,255]
    upper_color = [30,255,255]

    match_scope = (100,350,675,1000)
    match_scope = utils.convert_scope(match_scope, (1664, 936))

    resultss = image_processor.paddleocr_read(settings.screenshot_path, match_scope, lower_color, upper_color)
    return resultss


def tip_text_contains(key):
    resultss = read_tip_text()
    for idx in range(len(resultss)):
        results = resultss[idx]
        for result in results:
            rec = result[1] #('43', 0.99934321641922)
            res = rec[0] #'43'
            print("text: {}".format(str(res)))
            if key in res:
                return True
    return False


def got_exp_add_text():
    return tip_text_contains("+")


def got_bag_full_text():
    return tip_text_contains("满")


def got_MP_Insufficient_text():
    return tip_text_contains("MP不足")


def read_map_name():
    # 等级颜色米色参数
    lower_color = [0,0,130]
    upper_color = [179,169,255]

    match_scope = (4,41,1355,1662)
    match_scope = utils.convert_scope(match_scope, (1664, 936))

    resultss = image_processor.paddleocr_read(settings.screenshot_path, match_scope, lower_color, upper_color)
    result = get_first_result(resultss)
    if result != None:
        print("地图名称: {}".format(str(result)))
        return result
    return None

def read_quality_text():
    adb_controller.screenshot(settings.screenshot_path)
    # 等级颜色米色参数
    lower_color = [0,0,212]
    upper_color = [179,255,255]

    match_scope = (370,412,865,973)
    match_scope = utils.convert_scope(match_scope, (1664, 936))

    resultss = image_processor.paddleocr_read(settings.screenshot_path, match_scope, lower_color, upper_color)
    result = get_first_result(resultss)
    if result != None:
        print("当前极品文字: {}".format(str(result)))
        return result
    return None

def read_bag_remain_capacity():
    adb_controller.screenshot(settings.screenshot_path)
    # 等级颜色米色参数
    lower_color = [0,0,212]
    upper_color = [179,255,255]

    match_scope = (881,915,1011,1192)
    match_scope = utils.convert_scope(match_scope, (1664, 936))

    resultss = image_processor.paddleocr_read(settings.screenshot_path, match_scope, lower_color, upper_color)
    result = get_first_result(resultss)
    if result != None:
        print("背包容量: {}".format(str(result)))
        digit_array = re.findall(r'\d+\.?\d*', result)
        print("digit_array: {}".format(str(digit_array)))
        capacity = int(digit_array[0])
        return capacity
    return -1

def is_ji_pin():
    result = read_quality_text()
    if result != None:
        if "极" in result:
            return True
    return False

def is_zhen_xi():
    result = read_quality_text()
    if result != None:
        if "稀" in result:
            return True
    return False

def get_map_path(map_name=None):
    adb_controller.screenshot(settings.screenshot_path)
    if map_name == None:
        map_name = read_map_name()
    cave_path = []
    if map_name == "废矿东部":
        cave_path = settings.zombie_cave_path
    elif map_name == "生死之间":
        cave_path = settings.centipede_cave_path
    elif map_name == "盟重土城":
        cave_path = settings.ya_biao_path
    else:
        print("当前地图:{} 未设置挂机路径".format(map_name))

    # 一半概率反向
    if random.randint(0, 1) == 1:
        cave_path.reverse()
    return cave_path


# 如有弹出公告，则点击确定
def click_sure_btn():
    adb_controller.screenshot(settings.screenshot_path)

    match_scope = (529,702,623,1039)
    match_scope = utils.convert_scope(match_scope, (1664, 936))

    match_loc = image_processor.match_template(
        settings.screenshot_path, r"template_images/btn_sure.png", 0.05, match_scope)
    if(match_loc != None):
        print("检测到弹框确定按钮，自动关闭...." + str(match_loc))
        adb_controller.click(match_loc)
        return True
    return False


def click_scope(scope):
    point = ((scope[3] - scope[2]) / 2 + scope[2], (scope[1] - scope[0]) / 2 + scope[0])
    adb_controller.click(point)

def click_map():
    point = utils.convert_point((1645, 100), (1664, 936))
    adb_controller.click(point)

def click_map_aim():
    match_scope = utils.convert_scope((712,781,1556,1619), (1664, 936))
    click_scope(match_scope)

def click_map_input():
    match_scope = utils.convert_scope((420,501,562,1084), (1664, 936))
    click_scope(match_scope)

def click_map_clear():
    match_scope = utils.convert_scope((37,101,1398,1528), (1664, 936))
    click_scope(match_scope)

def click_map_edit_confirm():
    match_scope = utils.convert_scope((229,289,1405,1520), (1664, 936))
    click_scope(match_scope)

def click_map_input_confirm():
    match_scope = utils.convert_scope((586,647,912,1166), (1664, 936))
    click_scope(match_scope)

def click_map_npc_wen_biao_tou():
    match_loc = image_processor.match_template(
        settings.screenshot_path,r"template_images/npc_wen_biao_tou.png",0.05)
    if(match_loc != None):
        adb_controller.click(match_loc)

def click_xun_lu():
    match_loc = image_processor.match_template(
        settings.screenshot_path,r"template_images/btn_xun_lu.png",0.05)
    if(match_loc != None):
        adb_controller.click(match_loc)

def close_map():
    match_loc = image_processor.match_template(
        settings.screenshot_path,r"template_images/btn_close_map.png",0.05)
    if(match_loc != None):
        adb_controller.click(match_loc)

def click_npc_wen_biao_tou():
    # 坐标颜色绿色参数
    lower_color = [35,43,46]
    upper_color = [75,255,255]

    match_scope = (0,936,0,1664)
    match_scope = utils.convert_scope(match_scope, (1664, 936))

    resultss = image_processor.paddleocr_read(settings.screenshot_path, match_scope, lower_color, upper_color)
    for idx in range(len(resultss)):
        results = resultss[idx]
        for result in results:
            name_rate = result[1] #('43', 0.99934321641922)
            name = name_rate[0] #'43'
            if "温镖头" in name:
                print("result: {}".format(str(result)))
                corners = result[0]
                center = utils.get_center_of_corners(corners)
                adb_controller.click(center)
                return True
    return False

def click_accept_ya_biao():
    point = utils.convert_point((145, 450), (1664, 936))
    adb_controller.click(point)

def click_npc_lu_lao_ban():
    # 坐标颜色绿色参数
    lower_color = [35,43,46]
    upper_color = [75,255,255]

    match_scope = (0,936,0,1664)
    match_scope = utils.convert_scope(match_scope, (1664, 936))

    masks = []
    masks.append((0,34,440,1234)) #顶部滚动通知
    masks.append((42,198,1354,1664)) #右上角地图
    masks.append((796,936,625,1196)) #底部聊天窗口
    masks = utils.convert_masks(masks, (1664, 936))

    resultss = image_processor.paddleocr_read(settings.screenshot_path, match_scope, lower_color, upper_color, masks = masks)
    for idx in range(len(resultss)):
        results = resultss[idx]
        for result in results:
            name_rate = result[1] #('43', 0.99934321641922)
            name = name_rate[0] #'43'
            if "陆老板" in name:
                # print("result: {}".format(str(result)))
                corners = result[0]
                center = utils.get_center_of_corners(corners)
                adb_controller.click(center)
                return True
    return False

def click_finish_ya_biao():
    point = utils.convert_point((185, 175), (1664, 936))
    adb_controller.click(point)

# 计算间距为一步的路径
def to_each_step_path(path, round_path = True):
    if len(path) < 1:
        return path

    #使得头尾相连
    if round_path and path[-1] != path[0]:
        path.append(path[0])

    path_len = len(path)
    step_path = []
    step_path.append(path[0])
    for index in range(1, path_len):
        from_pos =  path[index - 1]
        to_pos =  path[index]
        # print(from_point)
        move_x = to_pos[0] - from_pos[0]
        move_y = to_pos[1] - from_pos[1]

        abs_move_x = abs(move_x)
        abs_move_y = abs(move_y)

        # 斜方向移动步数
        oblique_move_count = abs_move_x
        # 总移动步数
        total_move_count = abs_move_y
        if abs_move_x != 0 and abs_move_y != 0:
            if abs_move_y < abs_move_x:
                oblique_move_count = abs_move_y
                total_move_count = abs_move_x
        elif abs_move_x == 0:
            oblique_move_count = abs_move_y
            total_move_count = abs_move_y
        elif abs_move_y == 0:
            oblique_move_count = abs_move_x
            total_move_count = abs_move_x

        one_step_x = 0
        if abs_move_x != 0:
            one_step_x = (int)(move_x / abs_move_x)
        one_step_y = 0
        if abs_move_y != 0:
            one_step_y = (int)(move_y / abs_move_y)
        for i in range(0, total_move_count):
            if i < oblique_move_count:
                mid_pos = (from_pos[0] + one_step_x * (i + 1), from_pos[1] + one_step_y * (i + 1))
                step_path.append(mid_pos)
            elif abs_move_y < abs_move_x:
                mid_pos = (from_pos[0] + one_step_x * (i + 1), from_pos[1] + one_step_y * oblique_move_count)
                step_path.append(mid_pos)
            elif abs_move_y > abs_move_x:
                mid_pos = (from_pos[0] + one_step_x * oblique_move_count, from_pos[1] + one_step_y * (i + 1))
                step_path.append(mid_pos)

    # for index in range(0, len(step_path)):
    #     print(step_path[index])
    return step_path


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


def wait_to_match_and_click(match_text,threshold,max_time,step_time,match_scope = None):
    print("Start to wait till match text by "+str(match_text)+" for up to "+str(max_time)+" seconds  ....")
    time_start = time.time()
    click_success = False
    while(True):
        if click_menu(match_text, match_scope):
            click_success = True
            break
        if(time.time() - time_start > max_time):
            print("Reach max_time but failed to match")
            break
        time.sleep(step_time)
    return click_success


def restart_game():
    print("restart_game")
    adb_controller.stop_app()
    adb_controller.start_app()

    #消除系统确定消息框
    click_sure_btn()

    match_scope = (694,788,724,940)
    success = wait_to_match_and_click("登录",0.05,60,1,match_scope)
    if not success:
        if settings.device_address == "127.0.0.1:62001":
            exp_controller.restart_routine(True)
        else:
            restart_game()
    else:
        print("重启成功")

def reactive_pet():
    adb_controller.screenshot(settings.screenshot_path)

    collapse_pet_list()

    match_scope = (38,88,448,521)
    match_scope = utils.convert_scope(match_scope, (1664, 936))
    match_loc = image_processor.match_template(
        settings.screenshot_path,r"template_images/btn_rest_pet.png",0.05,match_scope)
    if(match_loc != None):
        adb_controller.click(match_loc)

    time.sleep(0.5)
    adb_controller.screenshot(settings.screenshot_path)

    match_scope = (43,83,453,516)
    match_scope = utils.convert_scope(match_scope, (1664, 936))

    match_loc = image_processor.match_template(
        settings.screenshot_path,r"template_images/btn_active_pet.png",0.05,match_scope)
    if(match_loc != None):
        adb_controller.click(match_loc)


def collapse_pet_list():
    # 法师收起宠物列表（如有）
    if globals.occupation == globals.Occupation.Magician:
        match_scope = (144,175,359,386)
        match_scope = utils.convert_scope(match_scope, (1664, 936))
        match_loc = image_processor.match_template(settings.screenshot_path, r"template_images/btn_close_pet_list.png",0.05,match_scope)
        if(match_loc != None):
            adb_controller.click(match_loc)
            time.sleep(1.0)
            adb_controller.screenshot(settings.screenshot_path)


def active_pet():
    collapse_pet_list()

    #是否已激活
    match_scope = (38,88,448,521)
    match_scope = utils.convert_scope(match_scope, (1664, 936))
    match_loc = image_processor.match_template(
        settings.screenshot_path,r"template_images/btn_rest_pet.png",0.05,match_scope)
    if(match_loc != None):
        return True

    # 激活宠物
    match_scope = (43,83,453,516)
    match_scope = utils.convert_scope(match_scope, (1664, 936))
    match_loc = image_processor.match_template(settings.screenshot_path, r"template_images/btn_active_pet.png",0.05,match_scope)
    if(match_loc != None):
        adb_controller.click(match_loc)
        return True

    return False


def wait_till_finish_login(max_time, step_time):
    time_start = time.time()
    finish_login = False
    while(True):
        adb_controller.screenshot(settings.screenshot_path)
        lv_area_text = read_lv_area_text()
        if "Lv" in lv_area_text or "LV" in lv_area_text or "v." in lv_area_text:
            finish_login = True
            break

        if(time.time() - time_start > max_time):
            print("Reach max_time but failed to get Lv (finish login)")
            break

        time.sleep(step_time)

    return finish_login


def open_bag():
    print("open_bag")
    point = utils.convert_point((560, 860), (1664, 936))
    adb_controller.click(point)

def wipe_down_bag():
    pos = (1000, 500)
    adb_controller.swipe((pos[0], pos[1] + 50), (pos[0], pos[1] - 50), 200)

def click_drop():
    point = utils.convert_point((1310, 840), (1664, 936))
    adb_controller.click(point)

def click_cancel_drop():
    point = utils.convert_point((622, 616), (1664, 936))
    adb_controller.click(point)

def click_confirm_drop():
    point = utils.convert_point((938, 616), (1664, 936))
    adb_controller.click(point)


def click_cancel_select():
    point = utils.convert_point((1080, 840), (1664, 936))
    adb_controller.click(point)

def click_left_return():
    print("click_left_return")
    point = utils.convert_point((59, 872), (1664, 936))
    adb_controller.click(point)

def click_right_return():
    print("click_right_return")
    point = utils.convert_point((1604, 872), (1664, 936))
    adb_controller.click(point)


def show_scope():
    item_template = "template_images/screenshot.png"
    match_loc = image_processor.match_template(
        settings.screenshot_path,item_template,0.05)

def select_item(item_name):
    item_template = "template_images/items/{}.png".format(str(item_name))

    match_scope = (125,807,939,1525)
    match_scope = utils.convert_scope(match_scope, (1664, 936))

    match_loc = image_processor.match_template(
        settings.screenshot_path,item_template,0.05,match_scope)
    if(match_loc != None):
        adb_controller.click(match_loc)
        return True
    return False

def map_point_to_coordination(map_point):
    my_coordinate = read_coordinate_text(need_screenshot = False)
    center = utils.convert_point((841.5, 504.5), (1664, 936))
    cell_size = utils.convert_point((86, 58), (1664, 936))
    offset_x = (map_point[0] - center[0]) / cell_size[0]
    offset_y = (map_point[1] - center[1]) / cell_size[1]
    offset_x = round(offset_x)
    offset_y = round(offset_y)
    target_coord = (int(my_coordinate[0]) + offset_x, int(my_coordinate[1]) + offset_y)
    print("target_coord: {}".format(str(target_coord)))
    # print("offset_x: {}".format(str(offset_x)))
    # print("offset_y: {}".format(str(offset_y)))
    return target_coord


def filter_trash_name(trash_name):
    trash_list = settings.ground_green_trash_list

    if len(trash_name) <= 4:
        return trash_name

    for idx in range(len(trash_list)):
        name = trash_list[idx]
        for i in range(0, len(name) - 2):
            sub_name = name[i:]
            trash_name = trash_name.replace(sub_name, "")
            sub_name = name[:-i]
            trash_name = trash_name.replace(sub_name, "")

    return trash_name

#检验是否全是中文字符
def is_all_chinese(strs):
    for _char in strs:
        if not '\u4e00' <= _char <= '\u9fa5':
            return False
    return True


#检验是否含有中文字符
def is_contains_chinese(strs):
    for _char in strs:
        if '\u4e00' <= _char <= '\u9fa5':
            return True
    return False


def check_ground_items(need_screenshot = True):
    if need_screenshot:
        adb_controller.screenshot(settings.screenshot_path)
    coords = []
    # 底色绿色文字物品
    lower_color = [35,43,46]
    upper_color = [75,255,255]

    match_scope = (0,936,0,1664)
    match_scope = utils.convert_scope(match_scope, (1664, 936))

    masks = []
    masks.append((0,34,440,1234)) #顶部滚动通知
    masks.append((42,198,1354,1664)) #右上角地图
    masks.append((796,936,625,1196)) #底部聊天窗口
    # masks.append((358,600,710,980)) #我自己
    # masks.append((152,274,756,910)) #经验提示框1
    # masks.append((796,936,470,610)) #血、魔球
    masks = utils.convert_masks(masks, (1664, 936))

    resultss = image_processor.paddleocr_read(settings.screenshot_path, match_scope, lower_color, upper_color, masks = masks)
    for idx in range(len(resultss)):
        results = resultss[idx]
        for result in results:
            # print("result: {}".format(str(result)))
            name_rate = result[1] #('43', 0.99934321641922)
            name = name_rate[0] #'43'
            if is_contains_chinese(name):
                filtered_name = filter_trash_name(name)
                if len(filtered_name) > 0:
                    print("found ground treasure: {}".format(str(filtered_name)))
                    corners = result[0]
                    left_top_point = corners[0]
                    right_top_point = corners[1]
                    right_bottom_point = corners[2]
                    left_bottom_point = corners[3]

                    total_width = right_bottom_point[0] - left_top_point[0]
                    total_height = right_bottom_point[1] - left_top_point[1]

                    name_length = len(name)
                    each_width = total_width / name_length

                    index = name.index(filtered_name)

                    center_x = left_top_point[0] + each_width * (index + len(filtered_name) / 2)
                    center_y = left_top_point[1] + total_height / 2
                    center = (center_x, center_y)
                    # print("center: {}".format(str(center)))
                    target_coord = map_point_to_coordination(center)
                    coords.append(target_coord)

    return coords


def check_ground_golds(need_screenshot = True):
    if need_screenshot:
        adb_controller.screenshot(settings.screenshot_path)
    coords = []

    dir = "template_images/ground_treasures/"
    entries = os.listdir(dir)
    for entry in entries:
        if not "DS_Store" in entry:
            path = "{}{}".format(dir, entry)
            print("path: {}".format(str(path)))
            match_locs = image_processor.multiple_match_template(
                settings.screenshot_path, path, 0.01)
            for idx in range(0, len(match_locs)):
                match_loc = match_locs[idx]
                # print("find match_loc: {}".format(str(match_loc)))
                target_coord = map_point_to_coordination(match_loc)
                if not target_coord in coords:
                    coords.append(target_coord)

    print("find gold coords: {}".format(str(coords)))
    return coords


def drink_item(item_name):
    print("drink:", item_name)
    adb_controller.screenshot(settings.screenshot_path)
    item_template = "template_images/items/{}.png".format(str(item_name))
    match_loc = image_processor.match_template(
        settings.screenshot_path,item_template,0.05)
    if(match_loc != None):
        adb_controller.double_click(match_loc)
        click_cancel_select()
        return True
    return False


def batch_drink_item(item_name):
    print("batch_drink:", item_name)
    adb_controller.screenshot(settings.screenshot_path)
    item_template = "template_images/items/{}.png".format(str(item_name))
    match_locs = image_processor.multiple_match_template(
        settings.screenshot_path,item_template,0.05)
    for idx in range(0, len(match_locs)):
        match_loc = match_locs[idx]
        adb_controller.double_click(match_loc)
    if(len(match_locs) != 0):
        click_cancel_select()
        return True
    return False


def check_monster_reachable():
    monster_list = get_monster_list()
    # print("monster_list: {}".format(str(monster_list)))
    if len(monster_list) > 0:
        return True
    else:
        return False

def check_exp_getting():
    check_times = 5;
    if globals.occupation == globals.Occupation.Taoist:
        check_times = 5
    for index in range(0, check_times):
        if got_exp_add_text():
            print("exp adding")
            return True
        else:
            print("exp cheking")

    print("exp not adding")
    return False


def check_level():
    #检查等级，等级等于29且未拜师，停止练级
    if globals.current_lvl < 29:
        globals.current_lvl = read_lv_text()

    # 首次读取是否已拜师
    if globals.already_has_master == None:
        if globals.current_lvl <= 29:
            globals.already_has_master = already_has_master()
        else:
            globals.already_has_master = True

    if (globals.current_lvl >= 26 and globals.current_lvl <= 29) and (not globals.already_has_master):
        for index in range(0, 20):
            print("等级已达到{}级，请先去拜师!!!".format(str(globals.current_lvl)))
        if (globals.current_lvl == 29):
            # 增加判断次数（容错）
            if globals.check_has_master_fail_remain > 0:
                globals.check_has_master_fail_remain = globals.check_has_master_fail_remain - 1
                print("达到29级，请先去拜师，再提示{}次将结束本程序".format(str(globals.read_coordinate_fail_remain)))
                # 重新检测是否已拜师
                globals.already_has_master = already_has_master()
            else:
                print("达到29级，请先去拜师，练级结束")
                return False
    return True


def is_monster_nearby():
    adb_controller.screenshot(settings.screenshot_path1)
    adb_controller.screenshot(settings.screenshot_path2)

    masks = []
    masks.append((0,34,440,1234)) #顶部滚动通知
    masks.append((42,198,1354,1664)) #右上角地图
    masks.append((796,936,625,1196)) #底部聊天窗口
    masks.append((358,600,710,980)) #我自己
    masks.append((152,274,756,910)) #经验提示框1
    masks.append((796,936,470,610)) #血、魔球
    masks = utils.convert_masks(masks, (1664, 936))

    match_loc = image_processor.match_template(
        settings.screenshot_path1, settings.screenshot_path2, 0.0001, masks = masks)
    if(match_loc != None):
        print("monster not nearby")
        return False
    else:
        print("monster nearby")
        return True


def get_bag_remain_capacity():
    open_bag()
    time.sleep(0.5)
    result = read_bag_remain_capacity()
    click_left_return()
    click_right_return()
    return result


def read_pet_HP():
    adb_controller.screenshot(settings.screenshot_path)

    collapse_pet_list()

    # 获取宝宝血量
    match_scope = (132,160,400,580)
    match_scope = utils.convert_scope(match_scope, (1664, 936))
    resultss = image_processor.paddleocr_read(settings.screenshot_path, match_scope)
    for idx in range(len(resultss)):
        results = resultss[idx]
        for result in results:
            rec = result[1] #('43', 0.99934321641922)
            res = rec[0] #'43'
            res = re.sub(u"([^\u0030-\u0039\u002f])", "", res)
            print("宝宝血量原始: {}".format(str(res)))
            if "2400" in res:
                tmp = res.replace("2400", "", 1)
                if "2400" in tmp:
                    res = "2400/2400"
            elif "480" in res:
                tmp = res.replace("480", "", 1)
                if "480" in tmp:
                    res = "480/480"
            print("宝宝血量修正后: {}".format(str(res)))
            if "/" in res:
                splits = res.split('/')
                if len(splits) == 2:
                    return splits
    return None


def get_pet_current_max_HP():
    pet_HP = read_pet_HP()
    if pet_HP != None:
        current_hp = int(pet_HP[0])
        max_hp = int(pet_HP[1])
        return max_hp
    return 0


def get_pet_max_HP():
    # 骷髅最大血量
    pet_max_HP = 2400
    if globals.occupation == globals.Occupation.Taoist:
        if globals.current_lvl < 35:
            pet_max_HP = 480
        elif globals.current_lvl >= 35:
            if globals.skill_dog_pos == None:
                pet_max_HP = 480
    else:
        pet_max_HP = 625

    return pet_max_HP

def is_pet_healthy():
    pet_HP = read_pet_HP()
    if pet_HP != None:
        current_hp = int(pet_HP[0])
        max_hp = int(pet_HP[1])
        if max_hp < 1500 and current_hp < max_hp * 5 / 6:
            return False
    return True


def select_boss():
    print("选择boss:")
    #打开目标列表
    open_target_list()
    time.sleep(0.2)

    #切换到怪物列表
    adb_controller.screenshot(settings.screenshot_path)
    open_monster_list()
    time.sleep(0.1)

    #识别怪物名称
    adb_controller.screenshot(settings.screenshot_path)
    lower_color = [0,0,118]
    upper_color = [179,255,255]

    boss_selected = False

    match_scope = (24,870,948,1512)
    match_scope = utils.convert_scope(match_scope, (1664, 936))

    resultss = image_processor.paddleocr_read(settings.screenshot_path, match_scope, lower_color, upper_color)
    for idx in range(len(resultss)):
        if boss_selected:
            break

        results = resultss[idx]
        for result in results:
            rec = result[1] #('43', 0.99934321641922)
            # print("rec: {}".format(str(rec)))
            res = rec[0] #'43'
            # print("res: {}".format(str(res)))
            print("怪物名: {}".format(str(res)))
            if "邪恶" in res or "尸王" in res or "经验宝箱" in res:
                boss_selected = True
                corners = result[0]
                center = utils.get_center_of_corners(corners)
                adb_controller.click(center)
                break

    #关闭目标列表
    close_target_list()
    return boss_selected

def set_occupation():
    match_loc = get_fire_ball_pos()
    if(match_loc != None):
        globals.occupation = globals.Occupation.Magician
    else:
        globals.occupation = globals.Occupation.Taoist


def get_skill_scope():
    match_scope = (200,936,1355,1662)
    match_scope = utils.convert_scope(match_scope, (1664, 936))
    return match_scope


def get_fire_ball_pos():
    match_loc = image_processor.match_template(
        settings.screenshot_path,r"template_images/skill_fire_ball.png",0.05,get_skill_scope())
    return match_loc


def cast_attack():
    print("cast_attack....")
    if globals.skill_attack_pos == None:
        match_loc = image_processor.match_template(
            settings.screenshot_path,r"template_images/skill_attack.png",0.05,get_skill_scope())
        if(match_loc != None):
            globals.skill_attack_pos = match_loc
    if globals.skill_attack_pos != None:
        adb_controller.click(globals.skill_attack_pos)


def cast_fire_ball():
    print("cast_fire_ball....")
    if globals.skill_fire_ball_pos == None:
        match_loc = get_fire_ball_pos()
        if(match_loc != None):
            globals.skill_fire_ball_pos = match_loc
    if globals.skill_fire_ball_pos != None:
        adb_controller.click(globals.skill_fire_ball_pos)


def cast_lighting():
    print("cast_lighting....")
    if globals.skill_lighting_pos == None:
        match_loc = image_processor.match_template(
            settings.screenshot_path,r"template_images/skill_lighting.png",0.05,get_skill_scope())
        if(match_loc != None):
            globals.skill_lighting_pos = match_loc
    if globals.skill_lighting_pos != None:
        adb_controller.click(globals.skill_lighting_pos)


def cast_shield():
    if globals.skill_shield_pos == None:
        match_loc = image_processor.match_template(
            settings.screenshot_path,r"template_images/skill_shield.png",0.05,get_skill_scope())
        if(match_loc != None):
            globals.skill_shield_pos = match_loc
    if globals.skill_shield_pos != None:
        adb_controller.click(globals.skill_shield_pos)


def cast_heal():
    if globals.skill_heal_pos == None:
        match_loc = image_processor.match_template(
            settings.screenshot_path,r"template_images/skill_heal.png",0.05,get_skill_scope())
        if(match_loc != None):
            globals.skill_heal_pos = match_loc
    if globals.skill_heal_pos != None:
        adb_controller.click(globals.skill_heal_pos)

    # 技能后摇1秒
    time.sleep(1)


def cast_defence():
    if globals.skill_defence_pos == None:
        match_loc = image_processor.match_template(
            settings.screenshot_path,r"template_images/skill_defence.png",0.05,get_skill_scope())
        if(match_loc != None):
            globals.skill_defence_pos = match_loc
    if globals.skill_defence_pos != None:
        adb_controller.click(globals.skill_defence_pos)

    # 技能后摇1秒
    time.sleep(1)


def cast_invisible():
    if globals.skill_invisible_pos == None:
        match_loc = image_processor.match_template(
            settings.screenshot_path,r"template_images/skill_invisible.png",0.05,get_skill_scope())
        if(match_loc != None):
            globals.skill_invisible_pos = match_loc
    if globals.skill_invisible_pos != None:
        adb_controller.click(globals.skill_invisible_pos)
        return True
    return False

def cast_poison():
    if globals.skill_poison_pos == None:
        match_loc = image_processor.match_template(
            settings.screenshot_path,r"template_images/skill_poison.png",0.05,get_skill_scope())
        if(match_loc != None):
            globals.skill_poison_pos = match_loc
    if globals.skill_poison_pos != None:
        adb_controller.click(globals.skill_poison_pos)

    # 技能后摇1秒
    time.sleep(1)


def cast_talisman():
    if globals.skill_talisman_pos == None:
        match_loc = image_processor.match_template(
            settings.screenshot_path,r"template_images/skill_talisman.png",0.05,get_skill_scope())
        if(match_loc != None):
            globals.skill_talisman_pos = match_loc
    if globals.skill_talisman_pos != None:
        adb_controller.click(globals.skill_talisman_pos)


def cast_skeleton():
    if globals.skill_skeleton_pos == None:
        match_loc = image_processor.match_template(
            settings.screenshot_path,r"template_images/skill_skeleton.png",0.05,get_skill_scope())
        if(match_loc != None):
            globals.skill_skeleton_pos = match_loc
    if globals.skill_skeleton_pos != None:
        adb_controller.click(globals.skill_skeleton_pos)


def cast_dog():
    if globals.skill_dog_pos == None:
        match_loc = image_processor.match_template(
            settings.screenshot_path,r"template_images/skill_dog.png",0.05,get_skill_scope())
        if(match_loc != None):
            globals.skill_dog_pos = match_loc
    if globals.skill_dog_pos != None:
        adb_controller.click(globals.skill_dog_pos)
        return True
    return False


def get_my_health():
    # adb_controller.screenshot(settings.screenshot_path)
    # 颜色参数
    lower_color = [0,0,0]
    upper_color = [179,0,255]

    match_scope = (330,410,675,1000)
    match_scope = utils.convert_scope(match_scope, (1664, 936))

    resultss = image_processor.paddleocr_read(settings.screenshot_path, match_scope, lower_color, upper_color)
    for idx in range(len(resultss)):
        results = resultss[idx]
        for result in results:
            rec = result[1] #('43', 0.99934321641922)
            res = rec[0] #'43'
            print("我的血量1: {}".format(str(res)))
            res = re.sub(u"([^\u0030-\u0039\u002f])", "", res)
            print("我的血量2: {}".format(str(res)))
            if "/" in res:
                splits = res.split('/')
                if len(splits) == 2:
                    return splits
    return None


def get_my_lose_HP():
    my_HP = get_my_health()
    if my_HP != None and len(my_HP) == 2:
        current_hp = int(my_HP[0])
        max_hp = int(my_HP[1])
        return max_hp - current_hp
    return 0


def click_menu_batch_use():
    adb_controller.screenshot(settings.screenshot_path)

    lower_color = [0,0,212]
    upper_color = [179,255,255]

    match_scope = (876,924,754,910)
    match_scope = utils.convert_scope(match_scope, (1664, 936))

    resultss = image_processor.paddleocr_read(settings.screenshot_path, match_scope, lower_color, upper_color)
    for idx in range(len(resultss)):
        results = resultss[idx]
        for result in results:
            name_rate = result[1] #('43', 0.99934321641922)
            name = name_rate[0] #'43'
            if "批量使用" in name:
                print("result: {}".format(str(result)))
                corners = result[0]
                center = utils.get_center_of_corners(corners)
                adb_controller.click(center)
                return True
    return False


def click_confirm_batch_use():
    adb_controller.screenshot(settings.screenshot_path)

    lower_color = [0,0,212]
    upper_color = [179,255,255]

    match_scope = (584,646,915,1167)
    match_scope = utils.convert_scope(match_scope, (1664, 936))

    resultss = image_processor.paddleocr_read(settings.screenshot_path, match_scope, lower_color, upper_color)
    for idx in range(len(resultss)):
        results = resultss[idx]
        for result in results:
            name_rate = result[1] #('43', 0.99934321641922)
            name = name_rate[0] #'43'
            if "批量使用" in name:
                print("result: {}".format(str(result)))
                corners = result[0]
                center = utils.get_center_of_corners(corners)
                adb_controller.click(center)
                return True
    return False


def cast_back_town():
    if globals.skill_back_town == None:
        match_loc = image_processor.match_template(
            settings.screenshot_path,r"template_images/btn_back_town.png",0.05,get_skill_scope())
        if(match_loc != None):
            globals.skill_back_town = match_loc
    if globals.skill_back_town != None:
        adb_controller.click(globals.skill_back_town)


# do_click==False,只检测存在，不点击
def cast_random_fly(do_click=True):
    if globals.skill_random_fly == None:
        match_loc = image_processor.match_template(
            settings.screenshot_path,r"template_images/btn_random_fly.png",0.05,get_skill_scope())
        if(match_loc != None):
            globals.skill_random_fly = match_loc
    if globals.skill_random_fly != None:
        if do_click:
            adb_controller.click(globals.skill_random_fly)
        return True
    return False



#点击屏幕，消除省电模式（不管有没有）
def click_center_of_screen():
    point = utils.convert_point((832, 468), (1664, 936))
    adb_controller.click(point, 0.1)


#点击盟重老兵
def click_npc_meng_zhong_lao_bing():
    print("click_npc_meng_zhong_lao_bing")
    adb_controller.screenshot(settings.screenshot_path)
    # 坐标颜色绿色参数
    lower_color = [35,43,46]
    upper_color = [75,255,255]

    match_scope = (0,936,0,1664)
    match_scope = utils.convert_scope(match_scope, (1664, 936))

    masks = []
    masks.append((0,34,440,1234)) #顶部滚动通知
    masks.append((42,198,1354,1664)) #右上角地图
    masks.append((796,936,625,1196)) #底部聊天窗口
    masks = utils.convert_masks(masks, (1664, 936))

    resultss = image_processor.paddleocr_read(settings.screenshot_path, match_scope, lower_color, upper_color, masks = masks)
    for idx in range(len(resultss)):
        results = resultss[idx]
        for result in results:
            name_rate = result[1] #('43', 0.99934321641922)
            name = name_rate[0] #'43'
            print("name: {}".format(str(name)))
            if "老兵" in name:
                print("result: {}".format(str(result)))
                corners = result[0]
                center = utils.get_center_of_corners(corners)
                adb_controller.click(center)
                return True
    return False


def click_yellow_menu(text):
    print("click_yellow_menu: {}".format(str(text)))
    # 坐标颜色黄色参数
    lower_color = [0,102,185]
    upper_color = [29,253,255]

    match_scope = (62,788,72,718)
    match_scope = utils.convert_scope(match_scope, (1664, 936))

    resultss = image_processor.paddleocr_read(settings.screenshot_path, match_scope, lower_color, upper_color)
    for idx in range(len(resultss)):
        results = resultss[idx]
        for result in results:
            name_rate = result[1] #('43', 0.99934321641922)
            name = name_rate[0] #'43'
            # print("name: {}".format(str(name)))
            if text in name:
                corners = result[0]
                center = utils.get_center_of_corners(corners)
                adb_controller.click(center)
                return True
    return False


# 点击洞穴传送
def click_transfer_cave(cave_name):
    print("click_transfer_cave: {}".format(str(cave_name)))
    # 米色参数
    lower_color = [0,0,212]
    upper_color = [179,255,255]

    match_scope = (284,608,966,1618)
    match_scope = utils.convert_scope(match_scope, (1664, 936))

    resultss = image_processor.paddleocr_read(settings.screenshot_path, match_scope, lower_color, upper_color)
    for idx in range(len(resultss)):
        results = resultss[idx]
        for result in results:
            name_rate = result[1] #('43', 0.99934321641922)
            name = name_rate[0] #'43'
            print("cave name: {}".format(str(name)))
            # 骷髅两个字识别不出来
            if cave_name == "骷髅洞":
                cave_name = "洞"
            if cave_name == name:
                # print("result: {}".format(str(result)))
                corners = result[0]
                center = utils.get_center_of_corners(corners)
                adb_controller.click(center)
                return True
    return False


# 消除如何移动提示
def click_msg_box(text, is_green=False):
    # 米色
    lower_color = [0,0,212]
    upper_color = [179,255,255]
    # 绿色
    if is_green:
        lower_color = [35,43,46]
        upper_color = [75,255,255]

    match_scope = (583,651,673,985)
    match_scope = utils.convert_scope(match_scope, (1664, 936))

    resultss = image_processor.paddleocr_read(settings.screenshot_path, match_scope, lower_color, upper_color)
    for idx in range(len(resultss)):
        results = resultss[idx]
        for result in results:
            name_rate = result[1] #('43', 0.99934321641922)
            name = name_rate[0] #'43'
            if text == name:
                # print("result: {}".format(str(result)))
                corners = result[0]
                center = utils.get_center_of_corners(corners)
                adb_controller.click(center)
                return True
    return False


# 点击右侧菜单
def click_menu(text, match_scope):
    adb_controller.screenshot(settings.screenshot_path)
    match_scope = utils.convert_scope(match_scope, (1664, 936))

    resultss = image_processor.paddleocr_read(settings.screenshot_path, match_scope)
    for idx in range(len(resultss)):
        results = resultss[idx]
        for result in results:
            name_rate = result[1] #('43', 0.99934321641922)
            name = name_rate[0] #'43'
            print("name: {}".format(str(name)))
            if text in name:
                corners = result[0]
                center = utils.get_center_of_corners(corners)
                adb_controller.click(center)
                return True
    return False

# 点击右侧菜单（商店、仓库、寄售、更多、出售、整理）
def click_right_menu(text):
    match_scope = (146,760,1542,1632)
    return click_menu(text, match_scope)

# 点击左侧菜单（药品、杂货、服装、武器、首饰、书籍、绑C、绑金）
def click_left_menu(text):
    match_scope = (38,660,22,138)
    return click_menu(text, match_scope)

# 点击商品菜单
def click_item_menu(text):
    match_scope = (36,688,180,428)
    return click_menu(text, match_scope)

# 点击购买
def click_btn_buy():
    match_scope = (798,864,426,546)
    return click_menu("购买", match_scope)


# 点击“依然传送”
def click_btn_confirm_transform():
    match_scope = (582,650,908,1166)
    return click_menu("依然传送", match_scope)


# 点击“登录”
def click_btn_login():
    match_scope = (694,788,724,940)
    return click_menu("登录", match_scope)


def read_current_page():
    match_scope = (698,756,322,532)
    match_scope = utils.convert_scope(match_scope, (1664, 936))
    resultss = image_processor.paddleocr_read(settings.screenshot_path, match_scope)
    for idx in range(len(resultss)):
        results = resultss[idx]
        for result in results:
            rec = result[1] #('43', 0.99934321641922)
            res = rec[0] #'43'
            print("page: {}".format(str(res)))
            if "/" in res:
                splits = res.split('/')
                if len(splits) == 2:
                    return splits
    return None


def click_btn(btn_name):
    path = "{}{}.png".format("template_images/", btn_name)
    match_loc = image_processor.match_template(
        settings.screenshot_path, path, 0.05)
    if(match_loc != None):
        adb_controller.click(match_loc)
        return True
    return False


def wipe_down_npc_dialog_menu():
    print("wipe_down_npc_dialog_menu")
    pos = (680, 500)
    adb_controller.swipe((pos[0], pos[1] + 80), (pos[0], pos[1] - 80), 200)


def template_exist(template_name):
    path = "{}{}.png".format("template_images/", template_name)
    match_loc = image_processor.match_template(
        settings.screenshot_path, path, 0.05)
    if(match_loc != None):
        return True
    return False


def open_bag_and_drink(item_name):
    open_bag()
    time.sleep(0.5)
    drink_item(item_name)
    click_left_return()
    click_right_return()


def is_save_power_mode():
    adb_controller.screenshot(settings.screenshot_path)

    match_scope = (440,500,560,1110)
    match_scope = utils.convert_scope(match_scope, (1664, 936))
    resultss = image_processor.paddleocr_read(settings.screenshot_path, match_scope)
    for idx in range(len(resultss)):
        results = resultss[idx]
        for result in results:
            rec = result[1] #('43', 0.99934321641922)
            res = rec[0] #'43'
            if res != None:
                print("省电文字: {}".format(str(res)))
                if "省电" in res:
                    return True

    return False
