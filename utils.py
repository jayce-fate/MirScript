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
