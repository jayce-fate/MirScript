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
	print("AdbController:Swipe from "+str(from_loc)+" to "+str(to_loc)+" by "+str(use_time)+" millisecond")
	process = os.system("\""+settings.adb_path+"\""+" -s "+settings.device_address+" shell input swipe "
		+str(from_loc[0])+" "+str(from_loc[1])+" "+str(to_loc[0])+" "+str(to_loc[1])+" "+str(use_time))
	time.sleep(use_time/1000)
	time.sleep(2)

# 关闭app
def stop_app():
	os.system("\""+settings.adb_path+"\""+" -s "+settings.device_address+" shell am force-stop "+settings.package_name)
	time.sleep(1)

# 点击操作
def click(location):
	print("AdbController: Tap "+str(location[0])+" "+str(location[1]))
	last_click_loc = location
	os.system("\""+settings.adb_path+"\""+" -s "+settings.device_address+" shell input tap "+str(location[0])+" "+str(location[1]))
	time.sleep(0.5)

# 截屏
def screenshot(path):
	os.system("\""+settings.adb_path+"\""+" -s "+settings.device_address+" exec-out screencap -p > " + path)
	time.sleep(0.5)

# 图片匹配,直到匹配成功或者超时
def wait_till_match_any(template_paths,thresholds,return_center,max_time,step_time,scope = None,except_locs = None):
	print("AdbController: Start to wait till match screenshot by any "+str(template_paths)+" for up to "+str(max_time)+" seconds  ....")
	time_start = time.time()
	match_loc = None

	while(True):
		screenshot(settings.screenshot_path)
		for index in range(0,len(template_paths)):
			match_loc = image_processor.match_template(
				settings.screenshot_path,template_paths[index],thresholds[index],return_center,scope = scope,except_locs = except_locs)
			if(match_loc != None):
				return match_loc
		if(time.time() - time_start > max_time):
			print("AdbController: Reach max_time but failed to match")
			return None
		time.sleep(step_time)
	return None

# 图片匹配，匹配成功后执行点击
def wait_to_match_and_click(template_paths,thresholds,return_center,max_time,step_time
							,click_offset = None,scope = None,except_locs = None):
	re = wait_till_match_any(template_paths,thresholds,return_center,max_time,step_time,scope = scope,except_locs = except_locs)
	if(re == None):
		print("Cannot find "+str(template_paths))
		return "failed"
	if(click_offset != None):
		re = (re[0]+click_offset[0],re[1]+click_offset[1])
	click(re)
	return "success"

#图片匹配，如果成功，则持续进行匹配，如果失败或者超时，则返回退出
def wait_while_match(template_paths,thresholds,max_time,step_time,scope = None,except_locs = None):
	print("Start to wait while match screenshot by "+str(template_paths)+" for up to "+str(max_time)+" seconds  ....")
	time_start = time.time()
	while(True):
		screenshot(settings.screenshot_path)
		for i in range(0,len(template_paths)):
			match_loc = image_processor.match_template(
				settings.screenshot_path,template_paths[i],thresholds[i],True,scope = scope,except_locs=except_locs)
			if(match_loc != None):
				break
		if(match_loc == None or time.time() - time_start > max_time):
			return "over wait"
		time.sleep(step_time)

def read_text(max_time = 1,step_time = 1,scope = None,print_debug = False):
	print("AdbController: Start to read text for up to "+str(max_time)+" seconds  ....")
	time_start = time.time()

	while(True):
		screenshot(settings.screenshot_path)
		result = image_processor.easyocr_read(settings.screenshot_path,scope = scope,print_debug = print_debug)
		for reline in result:
			re_text = reline[1].replace(" ","")
			return re_text
		if(time.time() - time_start > max_time):
			print("AdbController: Reach max_time but failed to read")
			return None
		time.sleep(step_time)


#文字匹配
def wait_till_match_any_text(aim_texts = [],max_time = 1,step_time = 1,scope = None):
	print("AdbController: Start to wait till match screenshot by any text"+str(aim_texts)+" for up to "+str(max_time)+" seconds  ....")
	time_start = time.time()
	match_loc = None

	while(True):
		screenshot(settings.screenshot_path)
		result = image_processor.easyocr_read(settings.screenshot_path)
		for reline in result:
			re_text = reline[1].replace(" ","")
			for aim_text in aim_texts:
				k = re.findall(aim_text,re_text)
				if(len(k)>0):
					return reline
		if(time.time() - time_start > max_time):
			print("AdbController: Reach max_time but failed to match")
			return None
		time.sleep(step_time)
