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
        if character.name == None:
            raise Exception("RESTART")
    return character.name

def get_character_level():
    print('get_character_level')
    if character.level == None:
        read_character_data()
        if character.level == None:
            character.level = game_controller.read_lv_text()
            if character.level == None:
                raise Exception("RESTART")
            else:
                write_character_data()
    return character.level

def set_character_level(level):
    print('set_character_level')
    if level != None:
        if character.level == None or character.level < level:
            character.level = level
            write_character_data()

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
    character.name = json_object['name']
    character.level = json_object['level']
