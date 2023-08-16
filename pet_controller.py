import re
import time

import adb_controller
import btn_controller
import enums
import game_controller
import image_processor
import match_controller
import settings
import skill_controller
import user_controller
import utils

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

def rest_pet():
    match_scope = (38, 88, 448, 521)
    match_scope = utils.convert_scope(match_scope, (1664, 936))

    btn_controller.click_btn("btn_rest_pet", match_scope)

    match_loc = match_controller.wait_till_not_match_template("btn_rest_pet", settings.act_time_limit, settings.act_time)
    if match_loc != None:
        raise Exception("RESTART")

def active_pet():
    match_scope = (43, 83, 453, 516)
    match_scope = utils.convert_scope(match_scope, (1664, 936))

    return btn_controller.click_btn("btn_active_pet", match_scope)

def reactive_pet():
    adb_controller.screenshot(settings.screenshot_path)

    collapse_pet_list()

    rest_pet()

    # time.sleep(0.5)
    # adb_controller.screenshot(settings.screenshot_path)

    active_pet()


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


def try_active_pet():
    collapse_pet_list()

    #是否已激活
    match_scope = (38,88,448,521)
    match_scope = utils.convert_scope(match_scope, (1664, 936))
    match_loc = match_controller.match_template("btn_rest_pet", match_scope)
    if(match_loc != None):
        return True

    # 激活宠物
    return active_pet()

def read_pet_HP():
    adb_controller.screenshot(settings.screenshot_path)

    collapse_pet_list()

    # lower_color = [20,67,119]
    # upper_color = [21,72,255]

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
            # print("宝宝血量原始: {}".format(str(res)))
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
            elif len(res) == 9:
                digit1 = res[0:4]
                digit2 = res[5:9]
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
            elif not "/" in res:
                res_length = len(res)
                each_length = int(res_length / 2)
                if len(res) % 2 == 0:
                    digit1 = res[0:each_length]
                    digit2 = res[each_length:res_length]
                    print("digit1 = ", digit1)
                    print("digit2 = ", digit2)
                    if digit1 == digit2:
                        res = digit1 + "/" + digit2
                else:
                    digit1 = res[0:each_length]
                    digit2 = res[each_length+1:res_length]
                    print("digit1 = ", digit1)
                    print("digit2 = ", digit2)
                    if digit1 == digit2:
                        res = digit1 + "/" + digit2

            print("宝宝血量修正后: {}".format(str(res)))
            if "/" in res:
                splits = res.split('/')
                if len(splits) == 2:
                    pet_HP = splits
                    current_hp = int(pet_HP[0])
                    max_hp = int(pet_HP[1])
                    #容错，比如480/0
                    if max_hp < current_hp:
                        max_hp = current_hp
                    splits[0] = str(current_hp)
                    splits[1] = str(max_hp)
                    globals.read_pet_hp_fail_remain = settings.read_pet_hp_fail_limit
                    return splits

    # 读取宠物血量失败达到限定次数，重启
    globals.read_pet_hp_fail_remain = globals.read_pet_hp_fail_remain - 1
    if globals.read_pet_hp_fail_remain < 0:
        globals.read_pet_hp_fail_remain = settings.read_pet_hp_fail_limit
        print("globals.read_pet_hp_fail_remain < 0")
        raise Exception("RESTART")
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