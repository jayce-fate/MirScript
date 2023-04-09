import os
import time
import re
import cv2
import random

import adb_controller
import skill_controller
import image_processor
import btn_controller
import trash_controller
import settings
import globals
import utils
import user_controller
import enums

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
        if len(digit_array) > 0:
            current_lvl = int(digit_array[0])
            print("current_lvl: {}".format(str(current_lvl)))
            return current_lvl

    return None

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


def read_character_name():
    # 颜色米色
    lower_color = [0,0,212]
    upper_color = [179,255,255]

    match_scope = (0,56,0,300)
    match_scope = utils.convert_scope(match_scope, (1664, 936))

    resultss = image_processor.paddleocr_read(settings.screenshot_path, match_scope, lower_color, upper_color)
    result = get_first_result(resultss)
    if result != None:
        result = re.sub("[^a-zA-Z0-9\u4e00-\u9fa5]", '', result)
        print("角色名: {}".format(str(result)))
        return result
    print("result == None")
    return None


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
        if "徒" in result or "弟" in result or ("[" in result and "]" in result):
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

def get_already_ya_biao_text():
    return tip_text_contains("每天只能")

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


def close_map():
    match_loc = image_processor.match_template(
        settings.screenshot_path,r"template_images/btn_close_map.png",0.05)
    if(match_loc != None):
        adb_controller.click(match_loc)


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


def restart_game():
    print("restart_game")
    adb_controller.stop_app()
    adb_controller.start_app()

    dismissSureDialog()

    match_scope = (694,788,724,940)
    success = btn_controller.wait_to_match_and_click("登录",0.05,60,1,match_scope)
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
    if user_controller.get_character_occupation() == enums.Occupation.Magician:
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
        lv_area_text = read_lv_area_text().lower()
        if "l" in lv_area_text or "v" in lv_area_text:
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
    pos = utils.convert_point((956, 520), (1664, 936))
    adb_controller.swipe((pos[0], pos[1] + 50), (pos[0], pos[1] - 50), 400)

def wipe_up_bag():
    pos = utils.convert_point((956, 520), (1664, 936))
    adb_controller.swipe((pos[0], pos[1] - 50), (pos[0], pos[1] + 50), 400)

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


def check_monster_reachable():
    monster_list = get_monster_list()
    # print("monster_list: {}".format(str(monster_list)))
    if len(monster_list) > 0:
        return True
    else:
        return False

def check_exp_getting():
    check_times = 5;
    if user_controller.get_character_occupation() == enums.Occupation.Taoist:
        check_times = 5
    for index in range(0, check_times):
        if got_exp_add_text():
            print("exp adding")
            return True
        else:
            print("exp cheking")

    print("exp not adding")
    return False

# 21-29级可拜师
def check_level():
    #检查等级，等级等于29且未拜师，停止练级
    my_level = user_controller.get_character_level(refresh=True)
    has_master = user_controller.get_character_has_master()

    if (my_level == 29) and (not has_master):
        for index in range(0, 20):
            print("等级已达到{}级，请先去拜师!!!".format(str(my_level)))

        # 增加判断次数（容错）
        if globals.check_has_master_fail_remain > 0:
            globals.check_has_master_fail_remain = globals.check_has_master_fail_remain - 1
            print("达到29级，请先去拜师，再提示{}次将结束本程序".format(str(globals.read_coordinate_fail_remain)))
            # 重新检测是否已拜师
            has_master = user_controller.get_character_has_master(refresh=True)
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
    btn_controller.click_left_return()
    btn_controller.click_right_return()
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
            elif len(res) == 7:
                digit1 = res[0:3]
                digit2 = res[4:7]
                print("digit1 = ", digit1)
                print("digit2 = ", digit2)
                if digit1 <= digit2:
                    res = digit1 + "/" + digit2
            elif len(res) == 6:
                digit1 = res[0:3]
                digit2 = res[3:6]
                print("digit1 = ", digit1)
                print("digit2 = ", digit2)
                if digit1 == digit2:
                    res = digit1 + "/" + digit2
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
    if user_controller.get_character_occupation() == enums.Occupation.Taoist:
        if user_controller.get_character_level() < 35:
            pet_max_HP = 480
        elif user_controller.get_character_level() >= 35:
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

def get_occupation():
    match_loc = skill_controller.get_fire_ball_pos()
    occupation = None
    if(match_loc != None):
        occupation = enums.Occupation.Magician
    else:
        occupation = enums.Occupation.Taoist
    return occupation


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
            # res = re.sub(u"([^\u0030-\u0039\u002f])", "", res)
            res = re.sub("[^0-9/]", "", res)
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


def open_bag_and_drink(item_name, batch=False):
    open_bag()
    btn_controller.click_right_menu("整理")
    wipe_up_bag()
    time.sleep(0.5)
    if batch:
        trash_controller.batch_drink_item(item_name)
    else:
        trash_controller.drink_item(item_name)
    btn_controller.click_left_return()
    btn_controller.click_right_return()


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

# 消除确认框，比如游戏断开，活动提醒
def dismissSureDialog(directly=True):
    current_time = time.time()
    if directly or current_time - globals.last_check_sure_dialog_time > 60:
        globals.last_check_sure_dialog_time = current_time
        while btn_controller.click_sure_btn():
            print("消除确认提示框")
            return True
    return False
