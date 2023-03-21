import os
import time
import re
import cv2
import random
import numpy
import datetime
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

def init_user():
    if character.name == None:
        print('init_user')
        character.name = game_controller.read_character_name()
        current_path = Path().resolve()
        print("current_path:", current_path)
        character_file = current_path.joinpath('caches').joinpath(character.name + '.json')
        print("current_path:", current_path)
