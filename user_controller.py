import os
import time
import re
import cv2
import random
import numpy
import datetime
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

def get_character_name():
    print('get_character_name')
    if character.name == None:
        character.name = game_controller.read_character_name()
        if character.name == None or len(character.name) <= 1:
            raise Exception("RESTART")
    return character.name

def get_character_level(refresh=False):
    print('get_character_level')
    if character.level == None:
        read_character_data()

    if refresh or character.level == None:
        level = game_controller.read_lv_text()
        if level != None:
            if character.level == None or character.level < level:
                character.level = level
                write_character_data()
        else:
            # 非刷新，获取不到等级，重启
            if not refresh:
                raise Exception("RESTART")

    return character.level

def get_character_has_master(refresh=False):
    print('get_character_has_master')
    # 20级能拜师了么？
    if character.level < 20 or character.level >= 35:
        return False

    if character.has_master == None:
        read_character_data()

    if character.has_master == None or refresh:
        has_master = game_controller.already_has_master()
        if has_master != False:
            character.has_master = has_master
            write_character_data()
        else:
            # 获取不到拜师，重启
            if character.has_master == None:
                raise Exception("RESTART")

    return character.has_master

def get_character_file_path():
    print('get_character_file_path')

    current_path = Path().resolve()
    print("current_path:", current_path)
    character_file = current_path.joinpath('caches').joinpath(get_character_name() + '.json')
    print("character_file:", character_file)
    return character_file

def write_character_data():
    print('write_character_data')
    character_file = get_character_file_path()
    # Data to be written
    dictionary = {
        "name": character.name,
        "level": character.level,
        "has_master": character.has_master,
    }
    with open(character_file, "w") as outfile:
        json.dump(dictionary, outfile)

def read_character_data():
    print('read_character_data')

    character_file = get_character_file_path()
    print("character_file:", character_file)
    if not character_file.is_file():
        write_character_data()

    # Opening JSON file
    with open(character_file, 'r') as openfile:
        # Reading from json file
        json_object = json.load(openfile)

    print(json_object)
    if "name" in json_object:
        character.name = json_object['name']
    if "level" in json_object:
        character.level = json_object['level']
    if "has_master" in json_object:
        character.has_master = json_object['has_master']
