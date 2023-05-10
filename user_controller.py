import os
import time
import re
import cv2
import random
import numpy
from datetime import datetime
from datetime import timedelta
import json
from pathlib import Path

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
import character
import enums

def get_character_name():
    # print('get_character_name')
    if character.name == None:
        character.name = game_controller.read_character_name()
        if character.name == None or len(character.name) <= 1:
            print("character.name == None or len(character.name) <= 1")
            raise Exception("RESTART")
    return character.name

def get_character_level(refresh = False, use_raw_level = False):
    # print('get_character_level')
    if character.level == None:
        read_character_data()

    if refresh or character.level == None:
        level = game_controller.read_lv_text()
        set_level(level)
        is_legal_level = utils.is_legal_level(level)
        # 非刷新，则必须获取有效等级才行
        if not refresh and not is_legal_level:
            # 非刷新，获取不到等级，重启
            print("not refresh and not is_legal_level")
            raise Exception("RESTART")

        if use_raw_level:
            return level

    return character.level

def set_level(level):
    if level != None and level <= 52:
        if character.level == None or character.level < level:
            character.level = level
            write_character_data()

def get_character_has_master(refresh=False):
    # print('get_character_has_master')
    # 20级能拜师了么？
    if character.level < 20 or character.level >= 35:
        return False

    if character.has_master == None:
        read_character_data()

    if character.has_master == None or refresh:
        has_master = game_controller.already_has_master()
        character.has_master = has_master
        write_character_data()

    return character.has_master

def get_character_occupation(refresh=False):
    # print('get_character_occupation')
    if character.occupation == None:
        read_character_data()

    if refresh or character.occupation == None:
        occupation = game_controller.get_occupation()
        if occupation != None:
            character.occupation = occupation
            write_character_data()
        else:
            # 非刷新，获取不到等级，重启
            if not refresh:
                print("occupation != None and not refresh")
                raise Exception("RESTART")

    return character.occupation

# 是否已经领取低保
def can_get_subsidy():
    if character.subsidy_time == None:
        read_character_data()

    if character.subsidy_time != None:
        time_string = get_subsidy_time()
        if character.subsidy_time == time_string:
            print('already get subsidy')
            return False
    print('can get subsidy')
    return True

def get_subsidy_time():
    now = datetime.now()
    hour = now.strftime("%H")
    # print("hour:", hour)
    time_string = now.strftime("%Y-%m-%d")
    # print("time_string:", time_string)
    if int(hour) < 6:
        yesterday = now - timedelta(days = 1)
        time_string = yesterday.strftime("%Y-%m-%d")
    # print("time_string:", time_string)
    return time_string

def set_subsidy_time():
    # print('set_subsidy_time')
    time_string = get_subsidy_time()
    character.subsidy_time = time_string
    write_character_data()

# 是否已经领取经验
def can_get_exp_subsidy():
    if character.exp_subsidy_time == None:
        read_character_data()

    now = datetime.now()
    hour = int(now.strftime("%H"))
    if hour >= 18:
        if character.exp_subsidy_time == None:
            print('can get exp subsidy')
            return True
        else:
            time_string = get_exp_subsidy_time()
            if character.exp_subsidy_time != time_string:
                print('can get exp subsidy')
                return True

    # print('can not get exp subsidy')
    return False

def get_exp_subsidy_time():
    # print('get_exp_subsidy_time')
    now = datetime.now()
    time_string = now.strftime("%Y-%m-%d")
    # print("time_string:", time_string)
    return time_string

def set_exp_subsidy_time():
    time_string = get_exp_subsidy_time()
    character.exp_subsidy_time = time_string
    write_character_data()

# 是否可以押镖
def can_ya_biao():
    # print('can_ya_biao')
    if character.ya_biao_time == None:
        read_character_data()

    now = datetime.now()
    hour = int(now.strftime("%H"))
    if (4 <= hour and hour <= 7):
        level = get_character_level()
        if level >= 28:
            if character.ya_biao_time == None:
                return True
            else:
                time_string = get_ya_biao_time()
                if character.ya_biao_time != time_string:
                    return True

    return False

def get_ya_biao_time():
    # print('get_ya_biao_time')
    now = datetime.now()
    hour = now.strftime("%H")
    # print("hour:", hour)
    time_string = now.strftime("%Y-%m-%d")
    # print("time_string:", time_string)
    if int(hour) < 6:
        yesterday = now - timedelta(days = 1)
        time_string = yesterday.strftime("%Y-%m-%d")
    # print("time_string:", time_string)
    return time_string

def set_ya_biao_time():
    time_string = get_ya_biao_time()
    character.ya_biao_time = time_string
    write_character_data()

def get_character_file_path():
    # print('get_character_file_path')

    current_path = Path().resolve()
    # print("current_path:", current_path)
    character_file = current_path.joinpath('caches').joinpath(get_character_name() + '.json')
    # print("character_file:", character_file)
    return character_file

def write_character_data():
    # print('write_character_data')
    character_file = get_character_file_path()
    # Data to be written
    dictionary = {
        "name": character.name,
        "level": character.level,
        "has_master": character.has_master,
        "occupation": character.occupation,
        "subsidy_time": character.subsidy_time,
        "exp_subsidy_time": character.exp_subsidy_time,
        "ya_biao_time": character.ya_biao_time,
    }
    with open(character_file, "w") as outfile:
        json.dump(dictionary, outfile)

def read_character_data():
    # print('read_character_data')

    character_file = get_character_file_path()
    # print("character_file:", character_file)
    if not character_file.is_file():
        write_character_data()

    # Opening JSON file
    with open(character_file, 'r') as openfile:
        # Reading from json file
        json_object = json.load(openfile)

    # print(json_object)
    if "name" in json_object:
        character.name = json_object['name']
    if "level" in json_object:
        character.level = json_object['level']
    if "has_master" in json_object:
        character.has_master = json_object['has_master']
    if "occupation" in json_object:
        character.occupation = json_object['occupation']
    if "subsidy_time" in json_object:
        character.subsidy_time = json_object['subsidy_time']
    if "exp_subsidy_time" in json_object:
        character.exp_subsidy_time = json_object['exp_subsidy_time']
    if "ya_biao_time" in json_object:
        character.ya_biao_time = json_object['ya_biao_time']
