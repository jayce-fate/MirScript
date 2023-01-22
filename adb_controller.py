import os
import time
import re
import cv2
import shutil

import subprocess
import settings
import image_processor


# use_time 单位 毫秒
def swipe(from_loc,to_loc,use_time):
	process = os.system("\""+settings.adb_path+"\""+" -s "+settings.device_address+" shell input swipe "
		+str(from_loc[0])+" "+str(from_loc[1])+" "+str(to_loc[0])+" "+str(to_loc[1])+" "+str(use_time))
	time.sleep(use_time/1000)

# 输入文字
def input_text(text):
	os.system("\"" + settings.adb_path + "\"" + " -s " + settings.device_address + " shell input text \"" + text + "\"")
	time.sleep(0.001)

# 关闭app
def stop_app():
	command = "\"" + settings.adb_path + "\"" + " -s " + settings.device_address + " shell am force-stop  --user " + settings.package_UserId + " " + settings.package_name
	print("command:\n", command)
	os.system(command)
	time.sleep(0.001)

# 启动app
def start_app():
	command = "\"" + settings.adb_path + "\"" + " -s " + settings.device_address + " shell am start --user " + settings.package_UserId + " " + settings.package_name + "/." + settings.package_activity
	print("command:\n", command)
	os.system(command)
	time.sleep(0.001)


# 点击操作
def click(location, sleep_time = 0.001):
	os.system("\""+settings.adb_path+"\""+" -s "+settings.device_address+" shell input tap "+str(location[0])+" "+str(location[1]))
	if sleep_time > 0:
		time.sleep(sleep_time)


# 截屏
def screenshot(path):
	tmp_path = path + ".tmp"
	os.system("\""+settings.adb_path+"\""+" -s "+settings.device_address+" exec-out screencap -p > " + tmp_path)
	shutil.move(tmp_path, path)
	time.sleep(0.001)

# restart adb-server
def restart_adb():
	print("restart_adb")
	os.system(settings.adb_path + " kill-server")
	time.sleep(3)
	os.system(settings.adb_path + " start-server")
	time.sleep(3)

# restart mumu
def restart_mumu():
	print("restart_mumu")
	subprocess.run(["pkill", "-x", "NemuPlayer"])
	time.sleep(0.001)
	subprocess.run(["pkill", "-x", "NemuPlayer"])
	time.sleep(0.001)
	subprocess.run(["open", "/Applications/NemuPlayer.app"])
	time.sleep(0.001)

