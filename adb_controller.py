import os
import time
import re
import cv2
import shutil
import logging

import subprocess
import settings
import image_processor


def connect():
    command = "\"" + settings.adb_path + "\"" + " connect " + settings.device_address
    # print("command:\n", command)
    os.system(command)

# use_time 单位 毫秒
def swipe(from_loc,to_loc,use_time):
    command = "\"" + settings.adb_path + "\"" + " -s " + settings.device_address + " shell input swipe " + str(from_loc[0]) + " " + str(from_loc[1]) + " " + str(to_loc[0]) + " " + str(to_loc[1]) + " " + str(use_time)
    # print("command:\n", command)
    os.system(command)
    time.sleep(use_time/1000)

# 输入文字
def input_text(text):
    command = "\"" + settings.adb_path + "\"" + " -s " + settings.device_address + " shell input text \"" + text + "\""
    # print("command:\n", command)
    subprocess.call(command)
    time.sleep(0.001)

# 关闭app
def stop_app():
    command = "\"" + settings.adb_path + "\"" + " -s " + settings.device_address + " shell am force-stop  --user " + settings.package_UserId + " " + settings.package_name
    # print("command:\n", command)
    os.system(command)
    time.sleep(0.001)

# 启动app
def start_app():
    command = "\"" + settings.adb_path + "\"" + " -s " + settings.device_address + " shell am start --user " + settings.package_UserId + " " + settings.package_name + "/." + settings.package_activity
    # print("command:\n", command)
    os.system(command)
    time.sleep(0.001)


# 点击操作
def click(location, sleep_time = 0.001):
    command = "\"" + settings.adb_path + "\"" + " -s " + settings.device_address + " shell input tap " + str(location[0]) + " " + str(location[1])
    # print("command:\n", command)
    os.system(command)
    if sleep_time > 0:
        time.sleep(sleep_time)


# 截屏
def screenshot(path):
    tmp_path = path + ".tmp"
    command = "\"" + settings.adb_path + "\"" + " -s " + settings.device_address + " exec-out screencap -p > " + tmp_path
    # print("command:\n", command)
    os.system(command)
    shutil.move(tmp_path, path)
    time.sleep(0.001)

# restart adb-server
def restart_adb():
    print("restart_adb")
    command = "\"" + settings.adb_path + "\"" + " kill-server"
    # print("command:\n", command)
    os.system(command)

    time.sleep(3)

    command = "\"" + settings.adb_path + "\"" + " start-server"
    # print("command:\n", command)
    os.system(command)

    time.sleep(3)

# restart mumu
def restart_emulator():
    print("restart_emulator")

    emulator_name = ""
    if settings.device_address == "emulator-5554":
        emulator_name = "NemuPlayer"
        subprocess.run(["pkill", "-x", emulator_name])
        time.sleep(0.001)
        subprocess.run(["pkill", "-x", emulator_name])
        time.sleep(0.001)
        subprocess.run(["open", "/Applications/" + emulator_name + ".app"])
        time.sleep(0.001)
    elif settings.device_address == "127.0.0.1:62001":
        emulator_name = "NoxAppPlayer"
        subprocess.run(["pkill", "-x", emulator_name])
        time.sleep(0.001)
        subprocess.run(["pkill", "-x", emulator_name])
        time.sleep(0.5)
        subprocess.run(["open", "/Applications/" + emulator_name + ".app"])
        time.sleep(0.5)
        subprocess.run(["open", "/Applications/" + emulator_name + ".app"])
        time.sleep(0.5)
    else:
        logging.warning('未知模拟器')
