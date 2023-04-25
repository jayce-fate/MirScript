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
import btn_controller
import enums
import user_controller

def loop_drop_one_item(trash_name, is_green = False, force_drop = False):
    print("loop_drop_one_item:" + trash_name + ",isgreen:" + str(is_green) + ",force_drop:" + str(force_drop))
    if game_controller.select_item(trash_name):
        btn_controller.click_drop()
        if force_drop:
            btn_controller.click_confirm_drop()
            # print("click_confirm_drop")
            adb_controller.screenshot(settings.screenshot_path)
            loop_drop_one_item(trash_name, is_green, force_drop)
        else:
            time.sleep(0.1)
            adb_controller.screenshot(settings.screenshot_path)
            if game_controller.is_ji_pin():
                btn_controller.click_cancel_drop()
                adb_controller.screenshot(settings.screenshot_path)
            elif trash_name == "ji_neng_shu" and game_controller.is_zhen_xi():
                btn_controller.click_cancel_drop()
                adb_controller.screenshot(settings.screenshot_path)
            else:
                if is_green:
                    btn_controller.click_confirm_drop()
                    adb_controller.screenshot(settings.screenshot_path)
                loop_drop_one_item(trash_name, is_green, force_drop)


def loop_drink_one_item(trash_name):
    print("loop_drink_one_item:" + trash_name)
    if drink_item(trash_name):
        loop_drink_one_item(trash_name)


def drop_trashes_loop():
    adb_controller.screenshot(settings.screenshot_path)

    trash_list = settings.trash_list_white
    list_len = len(trash_list)
    for index in range(0, list_len):
        trash_name = trash_list[index]
        print("trash_name: {}".format(str(trash_name)))
        loop_drop_one_item(trash_name)

    trash_list = settings.trash_list_green
    list_len = len(trash_list)
    for index in range(0, list_len):
        trash_name = trash_list[index]
        print("trash_name: {}".format(str(trash_name)))
        loop_drop_one_item(trash_name, is_green = True)

    trash_list = settings.trash_list_force_drop
    list_len = len(trash_list)
    for index in range(0, list_len):
        trash_name = trash_list[index]
        print("trash_name: {}".format(str(trash_name)))
        loop_drop_one_item(trash_name, force_drop = True)

    trash_list = settings.trash_list_drink
    # 道士不扔强效魔法药
    if user_controller.get_character_occupation() == enums.Occupation.Taoist:
        if "qiang_xiao_mo_fa_yao" in trash_list:
            trash_list.remove("qiang_xiao_mo_fa_yao")
    # 道士不扔强效金创药
    elif user_controller.get_character_occupation() == enums.Occupation.Magician:
        if "qiang_xiao_jin_chuang_yao" in trash_list:
            trash_list.remove("qiang_xiao_jin_chuang_yao")
    list_len = len(trash_list)
    for index in range(0, list_len):
        trash_name = trash_list[index]
        print("trash_name: {}".format(str(trash_name)))
        loop_drink_one_item(trash_name)

def drop_trashes(neen_open_close_bag = True):
    if neen_open_close_bag:
        game_controller.open_bag()
        time.sleep(0.5)

    game_controller.wipe_up_bag()
    btn_controller.click_right_menu("整理")
    time.sleep(2.0)
    drop_trashes_loop()

    if neen_open_close_bag:
        btn_controller.click_left_return()
        btn_controller.click_right_return()


def drop_binding_trashes(neen_open_close_bag = True):
    if neen_open_close_bag:
        game_controller.open_bag()
        time.sleep(0.5)

    trash_list = settings.binding_trash_list
    list_len = len(trash_list)
    for index in range(0, list_len):
        trash_name = trash_list[index]
        print("trash_name: {}".format(str(trash_name)))
        loop_drop_one_item(trash_name, force_drop = True)

    if neen_open_close_bag:
        btn_controller.click_left_return()
        btn_controller.click_right_return()


def try_get_bag_space(space_need):
    if space_need > 0:
        game_controller.open_bag()
        time.sleep(0.5)
        remain_capacity = game_controller.read_bag_remain_capacity()
        if space_need <= remain_capacity:
            btn_controller.click_left_return()
            btn_controller.click_right_return()
            return True
        else:
            drop_trashes(neen_open_close_bag = False)
            remain_capacity = game_controller.read_bag_remain_capacity()
            if space_need <= remain_capacity:
                btn_controller.click_left_return()
                btn_controller.click_right_return()
                return True

            for idx in range(0, space_need - remain_capacity):
                # 道士剩蓝，其他剩红
                drink_item_name = "qiang_xiao_jin_chuang_yao"
                if user_controller.get_character_occupation() == enums.Occupation.Taoist:
                    drink_item_name = "qiang_xiao_mo_fa_yao"
                if not drink_item(drink_item_name):
                    break

            time.sleep(0.5)
            remain_capacity = game_controller.read_bag_remain_capacity()
            if space_need <= remain_capacity:
                btn_controller.click_left_return()
                btn_controller.click_right_return()
                return True

            for idx in range(0, space_need - remain_capacity):
                if not drink_item("qiang_xiao_tai_yang_shui"):
                    break

            remain_capacity = game_controller.read_bag_remain_capacity()
            if space_need <= remain_capacity:
                btn_controller.click_left_return()
                btn_controller.click_right_return()
                return True

        btn_controller.click_left_return()
        btn_controller.click_right_return()

    return False

def handle_bag_full():
    while game_controller.got_bag_full_text():
        if not try_get_bag_space(1):
            print("背包已满，无法腾出空间，休息2秒")
            time.sleep(2)

def collect_ground_treasures():
    collect_count = 0
    # 先捡金币，防止捡绿色物品后有遮挡
    gold_coords = check_ground_golds()
    while 0 < len(gold_coords):
        game_controller.dismissSureDialog(False)
        for idx in range(0, len(gold_coords)):
            print("捡金币")
            coord = gold_coords[idx]
            path = path_controller.find_path(globals.current_pos, coord)
            if len(path) > 0:
                move_controller.step_go_by_path(path)
                collect_count = collect_count + 1
                handle_bag_full()
        gold_coords = check_ground_golds()

    item_coords = check_ground_items()
    while 0 < len(item_coords):
        game_controller.dismissSureDialog(False)
        for idx in range(0, len(item_coords)):
            print("捡绿色物品")
            coord = item_coords[idx]
            path = path_controller.find_path(globals.current_pos, coord)
            if len(path) > 0:
                move_controller.step_go_by_path(path)
                collect_count = collect_count + 1
                handle_bag_full()
        item_coords = check_ground_items()

    print("collect_count：" + str(collect_count))
    return collect_count


def perform_buy(item_list, shop_item_list):
    for key, value in item_list.items():
        print('buy:', key, '->', value)
        if key in shop_item_list and value > 0:
            index = shop_item_list.index(key)
            btn_controller.click_item_menu_at_index(index)
            for idx in range(value):
                btn_controller.click_btn_buy()


def buy_loop_every_page(item_list, all_page_item_list):
    current_total_page = game_controller.read_current_page()
    if current_total_page != None:
        current_page = int(current_total_page[0])
        max_page = int(current_total_page[1])

        for idx in range(max_page):
            current_page_index = current_page - 1 + idx
            page_index = current_page_index % max_page
            perform_buy(item_list, all_page_item_list[page_index])
            if current_page_index != max_page - 1:
                btn_controller.click_btn("btn_page_right")
            else:
                btn_controller.click_btn("btn_page_left_most")
            time.sleep(0.5)


def buy_items(item_list, neen_not_open_but_close_bag = True):
    btn_controller.click_right_menu("商店")
    time.sleep(0.5)
    btn_controller.click_left_menu("绑金")
    time.sleep(1.0)
    adb_controller.screenshot(settings.screenshot_path)

    buy_loop_every_page(item_list, settings.bind_gold_item_list)

    if neen_not_open_but_close_bag:
        btn_controller.click_left_return()
        btn_controller.click_left_return()
        btn_controller.click_right_return()


def buy_books(item_list, neen_open_close_bag = True):
    if neen_open_close_bag:
        game_controller.open_bag()
        time.sleep(0.5)

    btn_controller.click_right_menu("商店")
    time.sleep(0.5)
    btn_controller.click_left_menu("书籍")
    time.sleep(1.0)
    adb_controller.screenshot(settings.screenshot_path)

    buy_loop_every_page(item_list, settings.book_item_list)

    if neen_open_close_bag:
        btn_controller.click_left_return()
        btn_controller.click_left_return()
        btn_controller.click_right_return()


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


def check_ground_items(need_screenshot = True):
    if need_screenshot:
        adb_controller.screenshot(settings.screenshot_path)

    #地图名称,如果是"盟重土城"，就重启，防止认为npc是绿色物品，死循环
    map_name = game_controller.read_map_name()
    if map_name == "盟重土城":
        print("check_ground_items, map_name == 盟重土城")
        raise Exception("RESTART")

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
            if utils.is_contains_chinese(name):
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
                    target_coord = game_controller.map_point_to_coordination(center)
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
                target_coord = game_controller.map_point_to_coordination(match_loc)
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
        btn_controller.click_cancel_select()
        return True
    return False


def batch_drink_item(item_name):
    print("batch_drink_item:", item_name)
    #debug
    if item_name == 'ji_neng_shu':
        globals.debug_times = globals.debug_times + 1
        prefix = "ji_neng_shu{}".format(str(globals.debug_times))
        adb_controller.screenshot(settings.screenshot_path, prefix)
    else:
        adb_controller.screenshot(settings.screenshot_path)
    item_template = "template_images/items/{}.png".format(str(item_name))
    match_locs = image_processor.multiple_match_template(
        settings.screenshot_path,item_template,0.05)

    if item_name == 'ji_neng_shu':
        file_name = "temp_screenshot/ji_neng_shu{}_log.txt".format(str(globals.debug_times))
        file = open(file_name,'w')
        file.write("match_locs:\n")
        for item in match_locs:
        	file.write(str(item)+"\n")
        file.close()

    item_indexs = []
    for idx in range(0, len(match_locs)):
        match_loc = match_locs[idx]
        index = utils.index_of_item_in_bag(match_loc)
        if not index in item_indexs:
            print("index:", index)
            print("match_loc:", str(match_loc))
            item_indexs.append(index)
            adb_controller.double_click(match_loc)
            if item_name == 'ji_neng_shu':
                file_name = "temp_screenshot/ji_neng_shu{}_log.txt".format(str(globals.debug_times))
                file = open(file_name,'a')
                file.write("index:\n")
                file.write(str(index)+"\n")
                file.write("double click match_loc:\n")
                file.write(str(match_loc)+"\n")
                file.close()

    if(len(item_indexs) != 0):
        btn_controller.click_cancel_select()
        return True
    return False

def batch_sell_item(item_name, force = False):
    print("batch_sell_item:", item_name)
    adb_controller.screenshot(settings.screenshot_path)
    item_template = "template_images/items/{}.png".format(str(item_name))
    match_locs = image_processor.multiple_match_template(
        settings.screenshot_path,item_template,0.05)

    item_indexs = []
    for idx in range(0, len(match_locs)):
        match_loc = match_locs[idx]
        index = utils.index_of_item_in_bag(match_loc)
        if not index in item_indexs:
            item_indexs.append(index)
            adb_controller.click(match_loc)
            btn_controller.click_right_menu('出售')
            if force:
                btn_controller.click_yes()
            else:
                if game_controller.is_ji_pin():
                    btn_controller.click_no()
                else:
                    btn_controller.click_yes()

    if(len(item_indexs) != 0):
        btn_controller.click_cancel_select()
        return True
    return False

#获取补给缺少数量清单
def get_supply_shortage_list(buy_list, neen_open_but_not_close_bag = True):
    if neen_open_but_not_close_bag:
        game_controller.open_bag()
        game_controller.wipe_up_bag()

    #一键出售
    btn_controller.click_right_menu("更多")
    adb_controller.screenshot(settings.screenshot_path)
    btn_controller.click_sell_all()
    adb_controller.screenshot(settings.screenshot_path)
    btn_controller.click_confirm()
    adb_controller.screenshot(settings.screenshot_path)
    btn_controller.click_yes()
    btn_controller.click_right_menu("整理")

    #出售技能书（极品也卖）
    batch_sell_item('ji_neng_shu', force = True)
    #出售白色虎齿项链（极品不卖）
    batch_sell_item('bai_se_hu_chi_xiang_lian', force = False)

    shortage_list = count_trashes(buy_list)
    return shortage_list

def count_trash(item_name):
    # print("count_trash:", item_name)
    item_template = "template_images/items/{}.png".format(str(item_name))
    match_locs = image_processor.multiple_match_template(
        settings.screenshot_path,item_template,0.05)

    item_indexs = []
    for idx in range(0, len(match_locs)):
        match_loc = match_locs[idx]
        # print("match_loc:", match_loc[0], match_loc[1])
        index = utils.index_of_item_in_bag(match_loc)
        if not index in item_indexs:
            item_indexs.append(index)
            # print("index:", index)

    return item_indexs

def count_trashes(item_list):
    supply_indexs = []

    #添加空位(为了把其他物品存仓)
    item_list['空位'] = 0
    #为了不存仓
    if not '强效金创药' in item_list:
        item_list['强效金创药'] = 0
    if not '强效魔法药' in item_list:
        item_list['强效魔法药'] = 0

    adb_controller.screenshot(settings.screenshot_path)
    for key, value in item_list.items():
        item_name = settings.item_name_dict[key]
        item_indexs = count_trash(item_name)
        item_list[key] = item_list[key] - len(item_indexs)
        print(key, '->', item_list[key])
        for item_index in item_indexs:
            if not item_index in supply_indexs:
                supply_indexs.append(item_index)

    for idx in range(42):
        if not idx in supply_indexs:
            print('宝贝坐标：', idx)
            item_pos = utils.get_item_pos_of_index(idx)
            print('item_pos：', str(item_pos))
            adb_controller.click(item_pos)
            btn_controller.click_in_warehouse()

    #去掉空位
    item_list.pop('空位', None)
    return item_list
