import os
import time
import re
import cv2
import random

import adb_controller
import image_processor
import settings
import globals
import utils
import game_controller
import path_controller
import move_controller

def get_skill_scope():
    match_scope = (200,936,1355,1662)
    match_scope = utils.convert_scope(match_scope, (1664, 936))
    return match_scope


def get_fire_ball_pos():
    match_loc = image_processor.match_template(
        settings.screenshot_path,r"template_images/skill_fire_ball.png",0.05,get_skill_scope())
    return match_loc


def cast_attack():
    print("cast_attack....")
    if globals.skill_attack_pos == None:
        match_loc = image_processor.match_template(
            settings.screenshot_path,r"template_images/skill_attack.png",0.05,get_skill_scope())
        if(match_loc != None):
            globals.skill_attack_pos = match_loc
    if globals.skill_attack_pos != None:
        adb_controller.click(globals.skill_attack_pos)


def cast_fire_ball():
    print("cast_fire_ball....")
    if globals.skill_fire_ball_pos == None:
        match_loc = get_fire_ball_pos()
        if(match_loc != None):
            globals.skill_fire_ball_pos = match_loc
    if globals.skill_fire_ball_pos != None:
        adb_controller.click(globals.skill_fire_ball_pos)


def cast_lighting():
    print("cast_lighting....")
    if globals.skill_lighting_pos == None:
        match_loc = image_processor.match_template(
            settings.screenshot_path,r"template_images/skill_lighting.png",0.05,get_skill_scope())
        if(match_loc != None):
            globals.skill_lighting_pos = match_loc
    if globals.skill_lighting_pos != None:
        adb_controller.click(globals.skill_lighting_pos)


def cast_shield():
    if globals.skill_shield_pos == None:
        match_loc = image_processor.match_template(
            settings.screenshot_path,r"template_images/skill_shield.png",0.05,get_skill_scope())
        if(match_loc != None):
            globals.skill_shield_pos = match_loc
    if globals.skill_shield_pos != None:
        adb_controller.click(globals.skill_shield_pos)


def cast_heal():
    if globals.skill_heal_pos == None:
        match_loc = image_processor.match_template(
            settings.screenshot_path,r"template_images/skill_heal.png",0.05,get_skill_scope())
        if(match_loc != None):
            globals.skill_heal_pos = match_loc
    if globals.skill_heal_pos != None:
        adb_controller.click(globals.skill_heal_pos)

    # 技能后摇1秒
    time.sleep(1)


def cast_defence():
    if globals.skill_defence_pos == None:
        match_loc = image_processor.match_template(
            settings.screenshot_path,r"template_images/skill_defence.png",0.05,get_skill_scope())
        if(match_loc != None):
            globals.skill_defence_pos = match_loc
    if globals.skill_defence_pos != None:
        adb_controller.click(globals.skill_defence_pos)

    # 技能后摇1秒
    time.sleep(1)


def cast_invisible():
    if globals.skill_invisible_pos == None:
        match_loc = image_processor.match_template(
            settings.screenshot_path,r"template_images/skill_invisible.png",0.05,get_skill_scope())
        if(match_loc != None):
            globals.skill_invisible_pos = match_loc
    if globals.skill_invisible_pos != None:
        adb_controller.click(globals.skill_invisible_pos)
        return True
    return False

def cast_poison():
    if globals.skill_poison_pos == None:
        match_loc = image_processor.match_template(
            settings.screenshot_path,r"template_images/skill_poison.png",0.05,get_skill_scope())
        if(match_loc != None):
            globals.skill_poison_pos = match_loc
    if globals.skill_poison_pos != None:
        adb_controller.click(globals.skill_poison_pos)

    # 技能后摇1秒
    time.sleep(1)


def cast_talisman():
    if globals.skill_talisman_pos == None:
        match_loc = image_processor.match_template(
            settings.screenshot_path,r"template_images/skill_talisman.png",0.05,get_skill_scope())
        if(match_loc != None):
            globals.skill_talisman_pos = match_loc
    if globals.skill_talisman_pos != None:
        adb_controller.click(globals.skill_talisman_pos)


def cast_skeleton():
    if globals.skill_skeleton_pos == None:
        match_loc = image_processor.match_template(
            settings.screenshot_path,r"template_images/skill_skeleton.png",0.05,get_skill_scope())
        if(match_loc != None):
            globals.skill_skeleton_pos = match_loc
    if globals.skill_skeleton_pos != None:
        adb_controller.click(globals.skill_skeleton_pos)
        time.sleep(1)


def cast_dog():
    if globals.skill_dog_pos == None:
        match_loc = image_processor.match_template(
            settings.screenshot_path,r"template_images/skill_dog.png",0.05,get_skill_scope())
        if(match_loc != None):
            globals.skill_dog_pos = match_loc
    if globals.skill_dog_pos != None:
        adb_controller.click(globals.skill_dog_pos)
        # 技能后摇1秒
        time.sleep(1)
        return True
    return False


def cast_back_town():
    if globals.skill_back_town == None:
        match_loc = image_processor.match_template(
            settings.screenshot_path,r"template_images/btn_back_town.png",0.05,get_skill_scope())
        if(match_loc != None):
            globals.skill_back_town = match_loc
    if globals.skill_back_town != None:
        adb_controller.click(globals.skill_back_town)


# do_click==False,只检测存在，不点击
def cast_random_fly(do_click=True):
    if globals.skill_random_fly == None:
        match_loc = image_processor.match_template(
            settings.screenshot_path,r"template_images/btn_random_fly.png",0.05,get_skill_scope())
        if(match_loc != None):
            globals.skill_random_fly = match_loc
    if globals.skill_random_fly != None:
        if do_click:
            adb_controller.click(globals.skill_random_fly)
        return True
    return False
