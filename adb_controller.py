import os
import time
import re
import cv2

import settings
import image_processor


# use_time 单位 毫秒
def swipe(from_loc,to_loc,use_time):
	# start_app()
	# print("AdbController:Swipe from "+str(from_loc)+" to "+str(to_loc)+" by "+str(use_time)+" millisecond")
	process = os.system("\""+settings.adb_path+"\""+" -s "+settings.device_address+" shell input swipe "
		+str(from_loc[0])+" "+str(from_loc[1])+" "+str(to_loc[0])+" "+str(to_loc[1])+" "+str(use_time))
	time.sleep(use_time/1000)

# 输入文字
def input_text(text):
	os.system("\"" + settings.adb_path + "\"" + " -s " + settings.device_address + " shell input text \"" + text + "\"")
	time.sleep(0.001)

# 关闭app
def stop_app():
	os.system("\"" + settings.adb_path + "\"" + " -s " + settings.device_address + " shell am force-stop  --user " + settings.package_UserId + " " + settings.package_name)
	time.sleep(0.001)

# 启动app
def start_app():
	os.system("\"" + settings.adb_path + "\"" + " -s " + settings.device_address + " shell am start --user " + settings.package_UserId + " " + settings.package_name + "/." + settings.package_activity)
	time.sleep(0.001)

# 点击操作
def click(location):
	# start_app()
	# print("AdbController: Tap "+str(location[0])+" "+str(location[1]))
	os.system("\""+settings.adb_path+"\""+" -s "+settings.device_address+" shell input tap "+str(location[0])+" "+str(location[1]))
	time.sleep(0.001)

# 截屏
def screenshot(path):
	# start_app()
	os.system("\""+settings.adb_path+"\""+" -s "+settings.device_address+" exec-out screencap -p > " + path)
	time.sleep(0.001)

