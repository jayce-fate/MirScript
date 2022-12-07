import os
import time
import re
import cv2

import adb_controller
import image_processor
import settings
import globals

walk_swip_time = 200
run_swip_time = 550
joystick_pos = (275, 500)

def one_step_walk_left():
	print("往左走一步....")
	adb_controller.swipe((joystick_pos[0] + 25, joystick_pos[1]), (joystick_pos[0] - 25, joystick_pos[1]), walk_swip_time)

def one_step_walk_right():
	print("往右走一步....")
	adb_controller.swipe((joystick_pos[0] - 25, joystick_pos[1]), (joystick_pos[0] + 25, joystick_pos[1]), walk_swip_time)

def one_step_walk_up():
	print("往上走一步....")
	adb_controller.swipe((joystick_pos[0], joystick_pos[1] + 25), (joystick_pos[0], joystick_pos[1] - 25), walk_swip_time)

def one_step_walk_down():
	print("往下走一步....")
	adb_controller.swipe((joystick_pos[0], joystick_pos[1] - 25), (joystick_pos[0], joystick_pos[1] + 25), walk_swip_time)

def one_step_walk_left_up():
	print("往左上走一步....")
	adb_controller.swipe((joystick_pos[0] + 25, joystick_pos[1] + 25), (joystick_pos[0] - 25, joystick_pos[1] - 25), walk_swip_time)

def one_step_walk_right_up():
	print("往右上走一步....")
	adb_controller.swipe((joystick_pos[0] - 25, joystick_pos[1] + 25), (joystick_pos[0] + 25, joystick_pos[1] - 25), walk_swip_time)

def one_step_walk_left_down():
	print("往左下走一步....")
	adb_controller.swipe((joystick_pos[0] + 25, joystick_pos[1] - 25), (joystick_pos[0] - 25, joystick_pos[1] + 25), walk_swip_time)

def one_step_walk_right_down():
	print("往右下走一步....")
	adb_controller.swipe((joystick_pos[0] - 25, joystick_pos[1] - 25), (joystick_pos[0] + 25, joystick_pos[1] + 25), walk_swip_time)

def one_step_run_left():
	print("往左跑两步....")
	adb_controller.swipe((joystick_pos[0] + 125, joystick_pos[1]), (joystick_pos[0] - 125, joystick_pos[1]), run_swip_time)

def one_step_run_right():
	print("往右跑两步....")
	adb_controller.swipe((joystick_pos[0] - 125, joystick_pos[1]), (joystick_pos[0] + 125, joystick_pos[1]), run_swip_time)

def one_step_run_up():
	print("往上跑两步....")
	adb_controller.swipe((joystick_pos[0], joystick_pos[1] + 125), (joystick_pos[0], joystick_pos[1] - 125), run_swip_time)

def one_step_run_down():
	print("往下跑两步....")
	adb_controller.swipe((joystick_pos[0], joystick_pos[1] - 125), (joystick_pos[0], joystick_pos[1] + 125), run_swip_time)

def one_step_run_left_up():
	print("往左上跑两步....")
	adb_controller.swipe((joystick_pos[0] + 125, joystick_pos[1] + 125), (joystick_pos[0] - 125, joystick_pos[1] - 125), run_swip_time)

def one_step_run_right_up():
	print("往右上跑两步....")
	adb_controller.swipe((joystick_pos[0] - 125, joystick_pos[1] + 125), (joystick_pos[0] + 125, joystick_pos[1] - 125), run_swip_time)

def one_step_run_left_down():
	print("往左下跑两步....")
	adb_controller.swipe((joystick_pos[0] + 125, joystick_pos[1] - 125), (joystick_pos[0] - 125, joystick_pos[1] + 125), run_swip_time)

def one_step_run_right_down():
	print("往右下跑两步....")
	adb_controller.swipe((joystick_pos[0] - 125, joystick_pos[1] - 125), (joystick_pos[0] + 125, joystick_pos[1] + 125), run_swip_time)

def get_monster_list():
	print("获取怪物列表:")
	#打开目标列表
	open_target_list()
	time.sleep(0.2)

	#切换到怪物列表
	adb_controller.screenshot(settings.screenshot_path)
	open_monster_list()
	time.sleep(0.1)

	#识别怪物名称
	adb_controller.screenshot(settings.screenshot_path)
	lower_color = [0,0,118]
	upper_color = [179,255,255]
	monster_list = image_processor.easyocr_read_cn(settings.screenshot_path,(24,870,948,1512),lower_color,upper_color)
	for reline in monster_list:
		re_text = reline[1].replace(" ","")
		print("怪物名: {}".format(str(re_text)))

	if len(monster_list) == 0:
		print("怪物列表为空")
	#关闭目标列表
	close_target_list()
	return monster_list


# 关闭怪物信息面板（等级、名称、血量）
def close_target_panel():
	print("关闭怪物信息....")
	match_loc = image_processor.match_template(
		settings.screenshot_path,r"template_images/btn_target_close.png",0.05)
	if(match_loc != None):
		adb_controller.click(match_loc)
		return True
	else:
		return False

def cast_fire_ball():
	print("cast_fire_ball....")
	match_loc = image_processor.match_template(
		settings.screenshot_path,r"template_images/skill_fire_ball.png",0.05)
	if(match_loc != None):
		adb_controller.click(match_loc)

def open_target_list():
	# print("open_target_list....")
	adb_controller.click((1185, 584))

def open_monster_list():
	# print("open_monster_list....")
	match_loc = image_processor.match_template(
		settings.screenshot_path,r"template_images/btn_monster.png",0.02,(561,627,1525,1632))
	if(match_loc != None):
		adb_controller.click(match_loc)

def close_target_list():
	# print("close_target_list....")
	match_loc = image_processor.match_template(
		settings.screenshot_path,r"template_images/btn_return.png",0.05,(850,892,1576,1628))
	if(match_loc != None):
		adb_controller.click(match_loc)

def open_or_close_map():
	# print("open_or_close_map....")
	match_loc = image_processor.match_template(
		settings.screenshot_path,r"template_images/map_bar.png",0.05,(0,41,1636,1664))
	if(match_loc != None):
		adb_controller.click(match_loc)

def read_coordinate_text():
	adb_controller.screenshot(settings.screenshot_path)
	# 坐标颜色绿色参数
	lower_color = [35,43,46]
	upper_color = [75,255,255]
	result = image_processor.easyocr_read_en(settings.screenshot_path,(42,82,1540,1664),lower_color,upper_color)
	for reline in result:
		re_text = reline[1].replace(" ","")
		re_text = re.findall(r'\d+', re_text)
		print("coordinate text Found: {}".format(str(re_text)))
		return re_text
	return None

def read_lv_text():
	# 等级颜色米色参数
	lower_color = [0,0,212]
	upper_color = [179,255,255]
	result = image_processor.easyocr_read_en(settings.screenshot_path,(56,100,58,104),lower_color,upper_color)
	for reline in result:
		re_text = reline[1].replace(" ","")
		re_text = re.findall(r'\d+', re_text)
		if(len(re_text) != 0):
			print("当前等级: {}".format(str(re_text[0])))
			return int(re_text[0])
		else:
			return -1
	return -1

def already_has_master():
	print("检查是否已拜师....")
	lower_color = [0,0,0]
	upper_color = [0,0,255]
	result = image_processor.easyocr_read_cn(settings.screenshot_path,(450,482,722,938),lower_color,upper_color)
	for reline in result:
		re_text = reline[1].replace(" ","")
		print("我的名字: {}".format(str(re_text)))
		if "徒" in re_text or "弟" in re_text or "[" in re_text or "]" in re_text:
			print("当前已拜师")
			return True
	print("当前未拜师")
	return False

def read_current_exp():
	adb_controller.screenshot(settings.screenshot_path)
	# 经验颜色米色参数
	lower_color = [0,0,212]
	upper_color = [179,255,255]
	result = image_processor.easyocr_read_en(settings.screenshot_path,(56,100,181,316),lower_color,upper_color)
	for reline in result:
		re_text = reline[1].replace(" ","")
		if(re_text != None):
			# print("exp text Found: {}".format(str(re_text)))
			digit_array = re.findall(r'\d+\.?\d*', re_text)
			# print("digit_array: {}".format(str(digit_array)))
			for index in range(0,len(digit_array)):
				return float(digit_array[index])
	return None

def read_map_name():
	# 等级颜色米色参数
	lower_color = [0,0,130]
	upper_color = [179,169,255]
	result = image_processor.easyocr_read_cn(settings.screenshot_path,(4,41,1355,1662),lower_color,upper_color)
	for reline in result:
		re_text = reline[1].replace(" ","")
		print("地图名称: {}".format(re_text))
		return re_text

def get_map_path():
	adb_controller.screenshot(settings.screenshot_path)
	map_name = read_map_name()
	cave_path = []
	if map_name == "废矿东部":
		cave_path = settings.zombie_cave_path
	elif map_name == "生死之间":
		cave_path = settings.centipede_cave_path
	else:
		print("当前地图:{} 未设置挂机路径".format(map_name))
	return cave_path

def click_sure_btn():
	# print("click_sure_btn....")

	# 弹出公告自动点击确定
	for tab_index in range(0,1):
		adb_controller.screenshot(settings.screenshot_path)
		# 弹框可被拖动，所以不指定区域
		match_loc = image_processor.match_template(
			settings.screenshot_path,r"template_images/btn_sure.png",0.05)
		if(match_loc != None):
			print("检测到弹框确定按钮，自动关闭....")
			adb_controller.click(match_loc)
		else:
			time.sleep(0.001)


def click_map():
	adb_controller.click((1645, 100))

def click_map_npc_wen_biao_tou():
	match_loc = image_processor.match_template(
		settings.screenshot_path,r"template_images/npc_wen_biao_tou.png",0.05)
	if(match_loc != None):
		adb_controller.click(match_loc)

def click_xun_lu():
	match_loc = image_processor.match_template(
		settings.screenshot_path,r"template_images/btn_xun_lu.png",0.05)
	if(match_loc != None):
		adb_controller.click(match_loc)

def close_map():
	match_loc = image_processor.match_template(
		settings.screenshot_path,r"template_images/btn_close_map.png",0.05)
	if(match_loc != None):
		adb_controller.click(match_loc)

def click_npc_wen_biao_tou():
	match_loc = image_processor.match_template(
		settings.screenshot_path,r"template_images/btn_npc_wen_biao_tou.png",0.05)
	if(match_loc != None):
		adb_controller.click(match_loc)

def click_accept_ya_biao():
	adb_controller.click((145, 450))

def click_npc_lu_lao_ban():
	match_loc = image_processor.match_template(
		settings.screenshot_path,r"template_images/btn_npc_lu_lao_ban.png",0.05)
	if(match_loc != None):
		adb_controller.click(match_loc)

def click_finish_ya_biao():
	adb_controller.click((185, 175))

# 计算间距为一步的路径
def to_each_step_path(path):
	step_path = []

	path_len = len(path)
	if path_len < 1:
		return path
	step_path.append(path[0])
	for index in range(1, path_len):
		from_pos =  path[index - 1]
		to_pos =  path[index]
		# print(from_point)
		move_x = to_pos[0] - from_pos[0]
		move_y = to_pos[1] - from_pos[1]

		abs_move_x = abs(move_x)
		abs_move_y = abs(move_y)

		# 斜方向移动步数
		oblique_move_count = abs_move_x
		# 总移动步数
		total_move_count = abs_move_y
		if abs_move_x != 0 and abs_move_y != 0:
			if abs_move_y < abs_move_x:
				oblique_move_count = abs_move_y
				total_move_count = abs_move_x
		elif abs_move_x == 0:
			oblique_move_count = abs_move_y
			total_move_count = abs_move_y
		elif abs_move_y == 0:
			oblique_move_count = abs_move_x
			total_move_count = abs_move_x

		one_step_x = 0
		if abs_move_x != 0:
			one_step_x = (int)(move_x / abs_move_x)
		one_step_y = 0
		if abs_move_y != 0:
			one_step_y = (int)(move_y / abs_move_y)
		for i in range(0, total_move_count):
			if i < oblique_move_count:
				mid_pos = (from_pos[0] + one_step_x * (i + 1), from_pos[1] + one_step_y * (i + 1))
				step_path.append(mid_pos)
			elif abs_move_y < abs_move_x:
				mid_pos = (from_pos[0] + one_step_x * (i + 1), from_pos[1] + one_step_y * oblique_move_count)
				step_path.append(mid_pos)
			elif abs_move_y > abs_move_x:
				mid_pos = (from_pos[0] + one_step_x * oblique_move_count, from_pos[1] + one_step_y * (i + 1))
				step_path.append(mid_pos)

	# for index in range(0, len(step_path)):
	# 	print(step_path[index])
	return step_path


def move_by_path(path, must_walk = False):
	print("move_by_path")
	move_path = path.copy()
	if move_path == None:
		return

	path_length = len(move_path)
	if path_length < 2:
		return

	from_pos = move_path[0]
	to_pos = move_path[1]

	# 每步都走，太慢了（主要是押镖）
	must_must_walk = False
	if must_walk:
		globals.step_count = (globals.step_count + 1) % 2
		if globals.step_count == 1:
			must_must_walk = True

	if not must_must_walk and path_length > 2:
		third_pos = move_path[2]
		line_x = from_pos[0] + third_pos[0] == 2 * to_pos[0]
		line_y = from_pos[1] + third_pos[1] == 2 * to_pos[1]
		if line_x and line_y:
			to_pos = third_pos

	print("初始位置: {}".format(str(from_pos)))
	print("目标位置: {}".format(str(to_pos)))

	move_x = to_pos[0] - from_pos[0]
	move_y = to_pos[1] - from_pos[1]

	is_runing = to_pos != move_path[1]
	print("to_pos: {}".format(str(to_pos)))
	print("move_path[1]: {}".format(str(move_path[1])))
	print("is_runing: {}".format(str(is_runing)))
	if move_x > 0 and move_y > 0:
		if is_runing:
			one_step_run_right_down()
		else:
			one_step_walk_right_down()
	elif move_x > 0 and move_y < 0:
		if is_runing:
			one_step_run_right_up()
		else:
			one_step_walk_right_up()
	elif move_x < 0 and move_y > 0:
		if is_runing:
			one_step_run_left_down()
		else:
			one_step_walk_left_down()
	elif move_x < 0 and move_y < 0:
		if is_runing:
			one_step_run_left_up()
		else:
			one_step_walk_left_up()
	elif move_x > 0 and move_y == 0:
		if is_runing:
			one_step_run_right()
		else:
			one_step_walk_right()
	elif move_x < 0 and move_y == 0:
		if is_runing:
			one_step_run_left()
		else:
			one_step_walk_left()
	elif move_x == 0 and move_y > 0:
		if is_runing:
			one_step_run_down()
		else:
			one_step_walk_down()
	elif move_x == 0 and move_y < 0:
		if is_runing:
			one_step_run_up()
		else:
			one_step_walk_up()

	del(move_path[0])
	if is_runing:
		del(move_path[0])

	if len(move_path) >= 2:
		move_by_path(move_path, must_walk)
	else:
		globals.expect_current_pos = (to_pos[0], to_pos[1])


def wait_till_match_any(template_path,threshold,max_time,step_time,scope = None):
	print("Start to wait till match screenshot by any "+str(template_path)+" for up to "+str(max_time)+" seconds  ....")
	time_start = time.time()
	match_loc = None
	while(True):
		adb_controller.screenshot(settings.screenshot_path)
		match_loc = image_processor.match_template(
			settings.screenshot_path,template_path,threshold,scope = scope)
		if(match_loc != None):
			return match_loc
		if(time.time() - time_start > max_time):
			print("Reach max_time but failed to match")
			return None
		time.sleep(step_time)
	return None


def wait_to_match_and_click(template_path,threshold,max_time,step_time,scope = None):
	match_loc = wait_till_match_any(template_path,threshold,max_time,step_time,scope = scope)
	if(match_loc == None):
		print("Cannot find "+str(template_path))
		return False
	adb_controller.click(match_loc)
	return True


def restart_game():
	adb_controller.stop_app()
	adb_controller.start_app()

	success = wait_to_match_and_click(r"template_images/btn_login.png",0.05,60,1,(706,779,737,930))
	if not success:
		restart_game()


def active_pet():
	success = wait_to_match_and_click(r"template_images/btn_close_pet_list.png",0.05,60,1,(144,175,359,386))
	if not success:
		return False

	result = wait_to_match_and_click(r"template_images/btn_active_pet.png",0.05,60,1,(43,83,453,516))
	return result

