import os
import time
import re
import cv2

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
        print("当前等级: {}".format(str(result)))
        return int(result)
    return -1

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

def got_exp_add_text():
    adb_controller.screenshot(settings.screenshot_path)
    # 颜色参数
    lower_color = [14,255,255]
    upper_color = [30,255,255]

    match_scope = (100,350,675,1000)
    match_scope = utils.convert_scope(match_scope, (1664, 936))

    resultss = image_processor.paddleocr_read(settings.screenshot_path, match_scope, lower_color, upper_color)
    for idx in range(len(resultss)):
        results = resultss[idx]
        for result in results:
            rec = result[1] #('43', 0.99934321641922)
            res = rec[0] #'43'
            print("text: {}".format(str(res)))
            if "+" in res:
                return True
    return False

def got_bag_full_text():
    adb_controller.screenshot(settings.screenshot_path)
    # 颜色参数
    lower_color = [14,255,255]
    upper_color = [30,255,255]

    match_scope = (100,350,675,1000)
    match_scope = utils.convert_scope(match_scope, (1664, 936))

    resultss = image_processor.paddleocr_read(settings.screenshot_path, match_scope, lower_color, upper_color)
    for idx in range(len(resultss)):
        results = resultss[idx]
        for result in results:
            rec = result[1] #('43', 0.99934321641922)
            res = rec[0] #'43'
            print("text: {}".format(str(res)))
            if "满" in res:
                return True
    return False

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

def get_map_path():
    adb_controller.screenshot(settings.screenshot_path)
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
def to_each_step_path(path):
    if len(path) < 1:
        return path

    #使得头尾相连
    if path[-1] != path[0]:
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


def wait_till_match_any(template_path,threshold,max_time,step_time,scope = None):
    print("Start to wait till match screenshot by any "+str(template_path)+" for up to "+str(max_time)+" seconds  ....")
    time_start = time.time()
    match_loc = None
    while(True):
        adb_controller.screenshot(settings.screenshot_path)
        match_loc = image_processor.match_template(
            settings.screenshot_path,template_path,threshold,scope = scope)
        if(match_loc != None):
            return match_loc
        if(time.time() - time_start > max_time):
            print("Reach max_time but failed to match")
            return None
        time.sleep(step_time)
    return None


def wait_to_match_and_click(template_path,threshold,max_time,step_time,scope = None):
    match_loc = wait_till_match_any(template_path,threshold,max_time,step_time,scope = scope)
    if(match_loc == None):
        print("Cannot find "+str(template_path))
        return False
    adb_controller.click(match_loc)
    return True


def restart_game():
    adb_controller.stop_app()
    adb_controller.start_app()

    #消除系统确定消息框
    click_sure_btn()

    match_scope = (706,779,737,930)
    match_scope = utils.convert_scope(match_scope, (1664, 936))

    success = wait_to_match_and_click(r"template_images/btn_login.png",0.05,60,1,match_scope)
    if not success:
        if settings.device_address == "127.0.0.1:62001":
            exp_controller.restart_routine(True)
        else:
            restart_game()

def reactive_pet():
    adb_controller.screenshot(settings.screenshot_path)

    match_scope = (144,175,359,386)
    match_scope = utils.convert_scope(match_scope, (1664, 936))

    match_loc = image_processor.match_template(
        settings.screenshot_path,r"template_images/btn_close_pet_list.png",0.05,match_scope)
    if(match_loc != None):
        adb_controller.click(match_loc)

    time.sleep(1)

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


def active_pet():
    match_scope = (144,175,359,386)
    match_scope = utils.convert_scope(match_scope, (1664, 936))

    success = wait_to_match_and_click(r"template_images/btn_close_pet_list.png", 0.05, 120, 1, match_scope)
    if not success:
        return False

    time.sleep(1)

    match_scope = (43,83,453,516)
    match_scope = utils.convert_scope(match_scope, (1664, 936))

    result = wait_to_match_and_click(r"template_images/btn_active_pet.png", 0.05, 60, 1, match_scope)
    return result

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

def click_arrange_bag():
    point = utils.convert_point((1590, 714), (1664, 936))
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


# def is_trash(trash_name):
#     trash = False
#     keywords = settings.ground_trashes_green_key_word
#     for idx in range(len(keywords)):
#         keyword = keywords[idx]
#         if keyword in trash_name:
#             trash = True
#             break
#
#     return trash


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
        adb_controller.click(match_loc, 0)
        #除了网易mumu，所有双击无效，改为批量使用
        if settings.device_address == "emulator-5554" or settings.device_address == "127.0.0.1:7555":
            adb_controller.click(match_loc, 0)
            adb_controller.click(match_loc, 0)
        else:
            time.sleep(0.5)
            if click_menu_batch_use():
                time.sleep(0.5)
                click_confirm_batch_use()
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
    if globals.current_lvl <= 29:
        globals.current_lvl = read_lv_text()

    if globals.already_has_master == None:
        if globals.current_lvl <= 29:
            globals.already_has_master = already_has_master()
        else:
            globals.already_has_master = True

    if (globals.current_lvl >= 26 and globals.current_lvl <= 29) and (not globals.already_has_master):
        for index in range(0, 20):
            print("等级已达到{}级，请先去拜师!!!".format(str(globals.current_lvl)))
        if (globals.current_lvl == 29):
            if globals.check_has_master_fail_remain > 0:
                globals.check_has_master_fail_remain = globals.check_has_master_fail_remain - 1
                print("达到29级，请先去拜师，再提示{}次将结束本程序".format(str(globals.read_coordinate_fail_remain)))
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


def is_bag_full():
    open_bag()
    time.sleep(0.5)

    is_bag_full = False
    result = read_bag_remain_capacity()
    if result < 6:
        is_bag_full = True

    click_left_return()
    click_right_return()

    return is_bag_full


def read_pet_HP():
    # 收起宠物列表（如有）
    adb_controller.screenshot(settings.screenshot_path)

    match_scope = (144,175,359,386)
    match_scope = utils.convert_scope(match_scope, (1664, 936))

    match_loc = image_processor.match_template(settings.screenshot_path, r"template_images/btn_close_pet_list.png",0.05,match_scope)
    if(match_loc != None):
        adb_controller.click(match_loc)
        time.sleep(1.0)
        adb_controller.screenshot(settings.screenshot_path)


    match_scope = (132,160,400,580)
    match_scope = utils.convert_scope(match_scope, (1664, 936))

    # 识别血量
    resultss = image_processor.paddleocr_read(settings.screenshot_path, match_scope)
    for idx in range(len(resultss)):
        results = resultss[idx]
        for result in results:
            rec = result[1] #('43', 0.99934321641922)
            res = rec[0] #'43'
            res = re.sub(u"([^\u0030-\u0039\u002f])", "", res)
            print("宝宝血量: {}".format(str(res)))
            if "/" in res:
                splits = res.split('/')
                if len(splits) == 2:
                    return splits
    return None


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


def cast_fire_ball():
    print("cast_fire_ball....")

    match_loc = get_fire_ball_pos()
    if(match_loc != None):
        adb_controller.click(match_loc)


def cast_lighting():
    print("cast_lighting....")
    match_loc = image_processor.match_template(
        settings.screenshot_path,r"template_images/skill_lighting.png",0.05,get_skill_scope())
    if(match_loc != None):
        adb_controller.click(match_loc)


def cast_shield():
    match_loc = image_processor.match_template(
        settings.screenshot_path,r"template_images/skill_shield.png",0.05,get_skill_scope())
    if(match_loc != None):
        adb_controller.click(match_loc)


def cast_heal():
    match_loc = image_processor.match_template(
        settings.screenshot_path,r"template_images/skill_heal.png",0.05,get_skill_scope())
    if(match_loc != None):
        adb_controller.click(match_loc)
    # 技能后摇1秒
    time.sleep(1)


def cast_defence():
    match_loc = image_processor.match_template(
        settings.screenshot_path,r"template_images/skill_defence.png",0.05,get_skill_scope())
    if(match_loc != None):
        adb_controller.click(match_loc)
    # 技能后摇1秒
    time.sleep(1)


def cast_invisible():
    match_loc = image_processor.match_template(
        settings.screenshot_path,r"template_images/skill_invisible.png",0.05,get_skill_scope())
    if(match_loc != None):
        adb_controller.click(match_loc)


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
            res = re.sub(u"([^\u0030-\u0039\u002f])", "", res)
            print("我的血量: {}".format(str(res)))
            if "/" in res:
                splits = res.split('/')
                if len(splits) == 2:
                    return splits
    return None


def get_my_lose_HP():
    my_HP = get_my_health()
    if my_HP != None:
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
