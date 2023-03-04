import os
import time
import re
import cv2
import random
import numpy
import datetime

import globals
import settings
import image_processor
import adb_controller
import game_controller
import path_controller
import move_controller


def get_resolution():
    if globals.resolution != None:
        return globals.resolution
    else:
        adb_controller.screenshot(settings.screenshot_path)
        target = cv2.imread(settings.screenshot_path)
        h, w = target.shape[0], target.shape[1]
        globals.resolution = (w, h)
        return globals.resolution


def convert_scope(scope, resolution = (1280, 720)):
    current_resolution = get_resolution()
    result = []
    if(scope != None):
        for idx in range(len(scope)):
            value = int(scope[idx] / resolution[0] * current_resolution[0])
            result.append(value)
    return tuple(result)


def convert_point(point, resolution = (1280, 720)):
    return convert_scope(point, resolution)


def convert_masks(masks, resolution = (1280, 720)):
    current_resolution = get_resolution()
    result = []
    if(masks != None):
        for mask in masks:
            result.append(convert_scope(mask, resolution))
    return tuple(result)


def convert_image(image, resolution):
    current_resolution = get_resolution()
    scale_x = current_resolution[0] / resolution[0]
    scale_y = current_resolution[1] / resolution[1]
    result = cv2.resize(image, (0, 0), fx=scale_x, fy=scale_y)
    return result

def get_center_of_corners(corners):
    left_top_point = corners[0]
    right_top_point = corners[1]
    right_bottom_point = corners[2]
    left_bottom_point = corners[3]
    center_x = left_top_point[0] + (right_bottom_point[0] - left_top_point[0]) / 2
    center_y = left_top_point[1] + (right_bottom_point[1] - left_top_point[1]) / 2
    # print("center_x: {}".format(str(center_x)))
    # print("center_y: {}".format(str(center_y)))
    center = (center_x, center_y)
    return center


#检验是否含有中文字符
def is_contains_chinese(strs):
    for _char in strs:
        if '\u4e00' <= _char <= '\u9fa5':
            return True
    return False


#检验是否全是中文字符
def is_all_chinese(strs):
    for _char in strs:
        if not '\u4e00' <= _char <= '\u9fa5':
            return False
    return True


def get_item_pos_of_index(item_index):
    left_top_point = convert_point((990, 178), (1664, 936))
    right_bottom_point = convert_point((1470, 750), (1664, 936))
    cell_width = (right_bottom_point[0] - left_top_point[0]) / 5 #96
    cell_height = (right_bottom_point[1] - left_top_point[1]) / 6 #96
    row = int(item_index / 6)
    column = item_index % 6
    item_pos = (left_top_point[0] + cell_width * column, left_top_point[1] + cell_height * row)
    return item_pos

def index_of_item_in_bag(item_pos):
    index = -1
    left_top_point = convert_point((990, 178), (1664, 936))
    right_bottom_point = convert_point((1470, 750), (1664, 936))
    cell_width = (right_bottom_point[0] - left_top_point[0]) / 5 #96
    cell_height = (right_bottom_point[1] - left_top_point[1]) / 6 #96

    cell_leftest = left_top_point[0] - cell_width / 2
    cell_toppest = left_top_point[1] - cell_height / 2
    for row in range(7):
        for column in range(6):
            cell_left = cell_leftest + cell_width * column
            cell_right = cell_left + cell_width
            cell_top = cell_toppest + cell_height * row
            cell_bottom = cell_top + cell_height

            if cell_left < item_pos[0] and item_pos[0] < cell_right and cell_top < item_pos[1] and item_pos[1] < cell_bottom:
                index = row * 6 + column
                return index

    return index
