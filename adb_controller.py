import os
import time
import re
import cv2

import settings
import image_processor

last_click_loc = None

def test():
	# process = os.system("adb -s 127.0.0.1:62028 shell pm list packages")
	process = os.system("adb -s 127.0.0.1:62028 shell input swipe 1200 340 1200 181 2000")
	# process = os.system("adb -s 127.0.0.1:62028 shell input tap 1200 340")
	# process = os.system("adb -s 127.0.0.1:62028 shell input tap 30 30")

def swipe(from_loc,to_loc,use_time):
	# print("AdbController:Swipe from "+str(from_loc)+" to "+str(to_loc)+" by "+str(use_time)+" millisecond")
	process = os.system("\""+settings.adb_path+"\""+" -s "+settings.device_address+" shell input swipe "
		+str(from_loc[0])+" "+str(from_loc[1])+" "+str(to_loc[0])+" "+str(to_loc[1])+" "+str(use_time))
	time.sleep(use_time/1000)

# 关闭app
def stop_app():
	os.system("\""+settings.adb_path+"\""+" -s "+settings.device_address+" shell am force-stop "+settings.package_name)
	time.sleep(1)

# 点击操作
def click(location):
	print("AdbController: Tap "+str(location[0])+" "+str(location[1]))
	last_click_loc = location
	os.system("\""+settings.adb_path+"\""+" -s "+settings.device_address+" shell input tap "+str(location[0])+" "+str(location[1]))
	time.sleep(0.001)

# 截屏
def screenshot(path):
	os.system("\""+settings.adb_path+"\""+" -s "+settings.device_address+" exec-out screencap -p > " + path)
	time.sleep(0.001)

