import adb_controller
import btn_controller
import match_controller
import settings


def open_map():
    btn_controller.click_map()
    match_loc = match_controller.wait_till_match_template("btn_xun_lu", settings.act_time_limit, settings.act_time)
    if match_loc == None:
        raise Exception("RESTART")

def open_cords_input():
    btn_controller.click_map_aim()
    match_loc = match_controller.wait_till_match_template("msg_btn/que_ding_r", settings.act_time_limit, settings.act_time)
    if match_loc == None:
        raise Exception("RESTART")

def close_cords_input():
    btn_controller.click_btn("msg_btn/que_ding_r")
    match_loc = match_controller.wait_till_not_match_template("msg_btn/que_ding_r", settings.act_time_limit, settings.act_time)
    if match_loc != None:
        raise Exception("RESTART")

def open_cords_edit():
    btn_controller.click_map_input()
    match_loc = match_controller.wait_till_match_template("que_ding_input", settings.act_time_limit, settings.act_time)
    if match_loc == None:
        raise Exception("RESTART")

def close_cords_edit():
    btn_controller.click_btn("que_ding_input")
    match_loc = match_controller.wait_till_not_match_template("que_ding_input", settings.act_time_limit, settings.act_time)
    if match_loc != None:
        raise Exception("RESTART")

def input_text(text):
    print("MapController input_text: {}".format(str(text)))
    open_cords_input()
    open_cords_edit()
    btn_controller.click_map_clear()
    adb_controller.input_text(text)
    close_cords_edit()
    close_cords_input()