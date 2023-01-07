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

def get_first_result(resultss):
	for idx in range(len(resultss)):
		results = resultss[idx]
		for result in results:
			rec = result[1] #('43', 0.99934321641922)
			# print("rec: {}".format(str(rec)))
			res = rec[0] #'43'
			# print("res: {}".format(str(res)))
			return res
	return None

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
	# monster_list = image_processor.easyocr_read_cn(settings.screenshot_path,(24,870,948,1512),lower_color,upper_color)
	# for reline in monster_list:
	# 	re_text = reline[1].replace(" ","")
	# 	print("怪物名: {}".format(str(re_text)))

	monster_list = []
	resultss = image_processor.paddleocr_read(settings.screenshot_path, (24,870,948,1512),lower_color,upper_color)
	for idx in range(len(resultss)):
		results = resultss[idx]
		for result in results:
			rec = result[1] #('43', 0.99934321641922)
			# print("rec: {}".format(str(rec)))
			res = rec[0] #'43'
			# print("res: {}".format(str(res)))
			print("怪物名: {}".format(str(res)))
		monster_list = results
		break

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

def read_coordinate_text(need_screenshot = True):
	if need_screenshot:
		adb_controller.screenshot(settings.screenshot_path)

	# 坐标颜色绿色参数
	lower_color = [35,43,46]
	upper_color = [75,255,255]
	resultss = image_processor.paddleocr_read(settings.screenshot_path, (42,82,1540,1664),lower_color,upper_color)
	result = get_first_result(resultss)
	if result != None:
		result = re.findall(r'\d+', result)
		# print("当前坐标: {}".format(str(result)))
		return result
	return None

def read_lv_text():
	# 等级颜色米色参数
	lower_color = [0,0,212]
	upper_color = [179,255,255]

	resultss = image_processor.paddleocr_read(settings.screenshot_path, (56,100,58,104),lower_color,upper_color)
	result = get_first_result(resultss)
	if result != None:
		print("当前等级: {}".format(str(result)))
		return int(result)
	return -1

def connection_lose():
	# adb_controller.screenshot(settings.screenshot_path)
	# 等级颜色米色参数
	lower_color = [0,0,212]
	upper_color = [179,255,255]
	resultss = image_processor.paddleocr_read(settings.screenshot_path, (390,462,620,1023),lower_color,upper_color)
	result = get_first_result(resultss)
	if result != None:
		print("当前提示文字: {}".format(str(result)))
		if "断开" in result:
			return True
	return False

def already_has_master():
	print("检查是否已拜师....")
	lower_color = [0,0,0]
	upper_color = [0,0,255]
	# result = image_processor.easyocr_read_cn(settings.screenshot_path,(450,482,722,938),lower_color,upper_color)
	# for reline in result:
	# 	re_text = reline[1].replace(" ","")
	# 	print("我的名字: {}".format(str(re_text)))
	# 	if "徒" in re_text or "弟" in re_text or "[" in re_text or "]" in re_text:
	# 		print("当前已拜师")
	# 		return True
	# print("当前未拜师")
	# return False

	resultss = image_processor.paddleocr_read(settings.screenshot_path, (450,482,722,938),lower_color,upper_color)
	result = get_first_result(resultss)
	if result != None:
		print("我的名字: {}".format(str(result)))
		if "徒" in result or "弟" in result or "[" in result or "]" in result:
			print("当前已拜师")
			return True
	print("当前未拜师")
	return False

def read_current_exp():
	adb_controller.screenshot(settings.screenshot_path)
	# 经验颜色米色参数
	lower_color = [0,0,212]
	upper_color = [179,255,255]
	# result = image_processor.easyocr_read_en(settings.screenshot_path,(56,100,181,316),lower_color,upper_color)
	# for reline in result:
	# 	re_text = reline[1].replace(" ","")
	# 	if(re_text != None):
	# 		# print("exp text Found: {}".format(str(re_text)))
	# 		digit_array = re.findall(r'\d+\.?\d*', re_text)
	# 		# print("digit_array: {}".format(str(digit_array)))
	# 		for index in range(0,len(digit_array)):
	# 			return float(digit_array[index])
	# return None

	resultss = image_processor.paddleocr_read(settings.screenshot_path, (56,100,181,316),lower_color,upper_color)
	result = get_first_result(resultss)
	if result != None:
		digit_array = re.findall(r'\d+\.?\d*', result)
		for index in range(0,len(digit_array)):
			current_exp = digit_array[index]
			# print("当前经验: {}".format(str(current_exp)))
			return float(current_exp)
	return None

def got_exp_add_text():
	adb_controller.screenshot(settings.screenshot_path)
	# 颜色参数
	lower_color = [14,255,255]
	upper_color = [30,255,255]

	resultss = image_processor.paddleocr_read(settings.screenshot_path, (100,350,675,1000),lower_color,upper_color)
	for idx in range(len(resultss)):
		results = resultss[idx]
		for result in results:
			rec = result[1] #('43', 0.99934321641922)
			res = rec[0] #'43'
			print("text: {}".format(str(res)))
			if "+" in res:
				return True
	return False

def got_bag_full_text():
	adb_controller.screenshot(settings.screenshot_path)
	# 颜色参数
	lower_color = [14,255,255]
	upper_color = [30,255,255]

	resultss = image_processor.paddleocr_read(settings.screenshot_path, (100,350,675,1000),lower_color,upper_color)
	for idx in range(len(resultss)):
		results = resultss[idx]
		for result in results:
			rec = result[1] #('43', 0.99934321641922)
			res = rec[0] #'43'
			print("text: {}".format(str(res)))
			if "满" in res:
				return True
	return False

def read_map_name():
	# 等级颜色米色参数
	lower_color = [0,0,130]
	upper_color = [179,169,255]
	# result = image_processor.easyocr_read_cn(settings.screenshot_path,(4,41,1355,1662),lower_color,upper_color)
	# for reline in result:
	# 	re_text = reline[1].replace(" ","")
	# 	print("地图名称: {}".format(re_text))
	# 	return re_text

	resultss = image_processor.paddleocr_read(settings.screenshot_path, (4,41,1355,1662),lower_color,upper_color)
	result = get_first_result(resultss)
	if result != None:
		print("地图名称: {}".format(str(result)))
		return result
	return None

def read_quality_text():
	adb_controller.screenshot(settings.screenshot_path)
	# 等级颜色米色参数
	lower_color = [0,0,212]
	upper_color = [179,255,255]
	resultss = image_processor.paddleocr_read(settings.screenshot_path, (370,412,865,973),lower_color,upper_color)
	result = get_first_result(resultss)
	if result != None:
		print("当前极品文字: {}".format(str(result)))
		return result
	return None

def read_bag_remain_capacity():
	adb_controller.screenshot(settings.screenshot_path)
	# 等级颜色米色参数
	lower_color = [0,0,212]
	upper_color = [179,255,255]
	resultss = image_processor.paddleocr_read(settings.screenshot_path, (881,915,1011,1192),lower_color,upper_color)
	result = get_first_result(resultss)
	if result != None:
		print("背包容量: {}".format(str(result)))
		digit_array = re.findall(r'\d+\.?\d*', result)
		print("digit_array: {}".format(str(digit_array)))
		capacity = int(digit_array[0])
		return capacity
	return -1

def is_quality():
	result = read_quality_text()
	if result != None:
		if "极" in result:
			return True
	return False

def get_map_path():
	adb_controller.screenshot(settings.screenshot_path)
	map_name = read_map_name()
	cave_path = []
	if map_name == "废矿东部":
		cave_path = settings.zombie_cave_path
	elif map_name == "生死之间":
		cave_path = settings.centipede_cave_path
	elif map_name == "盟重土城":
		cave_path = settings.ya_biao_path
	else:
		print("当前地图:{} 未设置挂机路径".format(map_name))
	return cave_path


# 如有弹出公告，则点击确定
def click_sure_btn():
	adb_controller.screenshot(settings.screenshot_path)
	# 弹框可被拖动，所以不指定区域
	match_loc = image_processor.match_template(
		settings.screenshot_path,r"template_images/btn_sure.png",0.05,(529,702,623,1039))
	if(match_loc != None):
		print("检测到弹框确定按钮，自动关闭...." + str(match_loc))
		adb_controller.click(match_loc)


def click_scope(scope):
	point = ((scope[3] - scope[2]) / 2 + scope[2], (scope[1] - scope[0]) / 2 + scope[0])
	adb_controller.click(point)

def click_map():
	adb_controller.click((1645, 100))

def click_map_aim():
	click_scope((712,781,1556,1619))

def click_map_input():
	click_scope((420,501,562,1084))

def click_map_clear():
	click_scope((37,101,1398,1528))

def click_map_edit_confirm():
	click_scope((229,289,1405,1520))

def click_map_input_confirm():
	click_scope((586,647,912,1166))

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
	# 坐标颜色绿色参数
	lower_color = [35,43,46]
	upper_color = [75,255,255]
	resultss = image_processor.paddleocr_read(settings.screenshot_path, (0,936,0,1664),lower_color,upper_color)
	for idx in range(len(resultss)):
		results = resultss[idx]
		for result in results:
			name_rate = result[1] #('43', 0.99934321641922)
			name = name_rate[0] #'43'
			if "温镖头" in name:
				print("result: {}".format(str(result)))
				corners = result[0]
				left_top_point = corners[0]
				right_top_point = corners[1]
				right_bottom_point = corners[2]
				left_bottom_point = corners[3]
				center_x = left_top_point[0] + (right_bottom_point[0] - left_top_point[0]) / 2
				center_y = left_top_point[1] + (right_bottom_point[1] - left_top_point[1]) / 2
				center = (center_x, center_y)
				adb_controller.click(center)
				return True
	return False

def click_accept_ya_biao():
	adb_controller.click((145, 450))

def click_npc_lu_lao_ban():
	match_loc = image_processor.match_template(
		settings.screenshot_path,r"template_images/btn_npc_lu_lao_ban.png",0.1)
	if(match_loc != None):
		adb_controller.click(match_loc)

def click_finish_ya_biao():
	adb_controller.click((185, 175))

# 计算间距为一步的路径
def to_each_step_path(path):
	if len(path) < 1:
		return path

	#使得头尾相连
	if path[-1] != path[0]:
		path.append(path[0])

	path_len = len(path)
	step_path = []
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


def move_by_path(path):
	# print("move_by_path:{}".format(str(path)))
	move_path = path.copy()
	if move_path == None:
		return

	path_length = len(move_path)
	if path_length < 2:
		return

	from_pos = move_path[0]
	to_pos = move_path[1]

	print("初始位置: {}".format(str(from_pos)))
	print("目标位置: {}".format(str(to_pos)))

	move_x = to_pos[0] - from_pos[0]
	move_y = to_pos[1] - from_pos[1]

	print("to_pos: {}".format(str(to_pos)))
	print("move_path[1]: {}".format(str(move_path[1])))
	if move_x > 0 and move_y > 0:
		one_step_walk_right_down()
	elif move_x > 0 and move_y < 0:
		one_step_walk_right_up()
	elif move_x < 0 and move_y > 0:
		one_step_walk_left_down()
	elif move_x < 0 and move_y < 0:
		one_step_walk_left_up()
	elif move_x > 0 and move_y == 0:
		one_step_walk_right()
	elif move_x < 0 and move_y == 0:
		one_step_walk_left()
	elif move_x == 0 and move_y > 0:
		one_step_walk_down()
	elif move_x == 0 and move_y < 0:
		one_step_walk_up()

	del(move_path[0])

	if len(move_path) >= 2:
		move_by_path(move_path)
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

	#消除系统确定消息框
	click_sure_btn()

	success = wait_to_match_and_click(r"template_images/btn_login.png",0.05,60,1,(706,779,737,930))
	if not success:
		restart_game()


def active_pet():
	success = wait_to_match_and_click(r"template_images/btn_close_pet_list.png",0.05,60,1,(144,175,359,386))
	if not success:
		return False

	result = wait_to_match_and_click(r"template_images/btn_active_pet.png",0.05,60,1,(43,83,453,516))
	return result

def open_bag():
	adb_controller.click((560, 860))

def wipe_down_bag():
	pos = (1000, 500)
	adb_controller.swipe((pos[0], pos[1] + 50), (pos[0], pos[1] - 50), 200)

def click_drop():
	adb_controller.click((1310, 840))

def click_cancel_drop():
	adb_controller.click((622, 616))

def click_confirm_drop():
	adb_controller.click((938, 616))

def click_arrange_bag():
	adb_controller.click((1590, 714))

def click_left_return():
	adb_controller.click((59, 872))

def click_right_return():
	adb_controller.click((1604, 872))


def show_scope():
	item_template = "template_images/screenshot.png"
	match_loc = image_processor.match_template(
		settings.screenshot_path,item_template,0.05)

def select_item(item_name):
	item_template = "template_images/items/{}.png".format(str(item_name))
	match_loc = image_processor.match_template(
		settings.screenshot_path,item_template,0.05,(125,807,939,1525))
	if(match_loc != None):
		adb_controller.click(match_loc)
		return True
	return False

def map_point_to_coordination(map_point):
	my_coordinate = read_coordinate_text(need_screenshot = False)
	center = (841.5, 504.5)
	cell_size = (86, 58)
	offset_x = (map_point[0] - center[0]) / cell_size[0]
	offset_y = (map_point[1] - center[1]) / cell_size[1]
	offset_x = round(offset_x)
	offset_y = round(offset_y)
	target_coord = (int(my_coordinate[0]) + offset_x, int(my_coordinate[1]) + offset_y)
	print("target_coord: {}".format(str(target_coord)))
	# print("offset_x: {}".format(str(offset_x)))
	# print("offset_y: {}".format(str(offset_y)))
	return target_coord


def is_trash(trash_name):
	trash = False
	keywords = settings.ground_trashes_green_key_word
	for idx in range(len(keywords)):
		keyword = keywords[idx]
		if keyword in trash_name:
			trash = True
			break

	return trash


#检验是否全是中文字符
def is_all_chinese(strs):
    for _char in strs:
        if not '\u4e00' <= _char <= '\u9fa5':
            return False
    return True


#检验是否含有中文字符
def is_contains_chinese(strs):
    for _char in strs:
        if '\u4e00' <= _char <= '\u9fa5':
            return True
    return False


def check_ground_items(need_screenshot = True):
	if need_screenshot:
		adb_controller.screenshot(settings.screenshot_path)
	coords = []
	# 底色绿色文字物品
	lower_color = [35,43,46]
	upper_color = [75,255,255]
	resultss = image_processor.paddleocr_read(settings.screenshot_path, (0,790,0,1360),lower_color,upper_color)
	for idx in range(len(resultss)):
		results = resultss[idx]
		for result in results:
			# print("result: {}".format(str(result)))
			name_rate = result[1] #('43', 0.99934321641922)
			name = name_rate[0] #'43'
			if is_contains_chinese(name):
				if not is_trash(name):
					print("found ground treasure: {}".format(str(name)))
					corners = result[0]
					left_top_point = corners[0]
					right_top_point = corners[1]
					right_bottom_point = corners[2]
					left_bottom_point = corners[3]
					center_x = left_top_point[0] + (right_bottom_point[0] - left_top_point[0]) / 2
					center_y = left_top_point[1] + (right_bottom_point[1] - left_top_point[1]) / 2
					center = (center_x, center_y)
					# print("center: {}".format(str(center)))
					target_coord = map_point_to_coordination(center)
					coords.append(target_coord)

	return coords


def check_ground_golds(need_screenshot = True):
	if need_screenshot:
		adb_controller.screenshot(settings.screenshot_path)
	coords = []

	dir = "template_images/ground_treasures/"
	entries = os.listdir(dir)
	for entry in entries:
		if not "DS_Store" in entry:
			path = "{}{}".format(dir, entry)
			print("path: {}".format(str(path)))
			match_loc = image_processor.match_template(
				settings.screenshot_path, path, 0.01)
			if(match_loc != None):
				print("find match_loc: {}".format(str(match_loc)))
				target_coord = map_point_to_coordination(match_loc)
				coords.append(target_coord)

	return coords


def drink_red():
	print("drink_red")
	adb_controller.screenshot(settings.screenshot_path)
	match_loc = image_processor.match_template(
		settings.screenshot_path,r"template_images/items/强效金疮药.png",0.1)
	if(match_loc != None):
		adb_controller.click(match_loc)
		adb_controller.click(match_loc)
		adb_controller.click(match_loc)
		return True
	else:
		return False

def drink_sun_water():
	print("drink_sun_water")
	adb_controller.screenshot(settings.screenshot_path)
	match_loc = image_processor.match_template(
		settings.screenshot_path,r"template_images/items/强效太阳水.png",0.1)
	if(match_loc != None):
		adb_controller.click(match_loc)
		adb_controller.click(match_loc)
		adb_controller.click(match_loc)
		return True
	else:
		return False

def check_monster_reachable():
	monster_list = get_monster_list()
	# print("monster_list: {}".format(str(monster_list)))
	if len(monster_list) > 0:
		return True
	else:
		return False

def check_exp_getting():
	for index in range(0, 5):
		if got_exp_add_text():
			print("exp adding")
			return True
		else:
			print("exp cheking")

	print("exp not adding")
	return False


def check_level():
	#检查等级，等级等于29且未拜师，停止练级
	lv = read_lv_text()
	if (lv >= 26 and lv <= 29) and (not already_has_master()):
		for index in range(0, 20):
			print("等级已达到{}级，请先去拜师!!!".format(str(lv)))
		if (lv == 29):
			if globals.check_has_master_fail_remain > 0:
				globals.check_has_master_fail_remain = globals.check_has_master_fail_remain - 1
				print("达到29级，请先去拜师，再提示{}次将结束本程序".format(str(globals.read_coordinate_fail_remain)))
			else:
				print("达到29级，请先去拜师，练级结束")
				return False
	return True


def is_monster_nearby():
	adb_controller.screenshot(settings.screenshot_path1)
	adb_controller.screenshot(settings.screenshot_path2)
	masks = []
	masks.append((0,34,440,1234)) #顶部滚动通知
	masks.append((42,198,1354,1664)) #右上角地图
	masks.append((796,936,625,1196)) #底部聊天窗口
	masks.append((358,600,710,980)) #我自己
	masks.append((152,274,756,910)) #经验提示框1
	masks.append((796,936,470,610)) #血、魔球
	match_loc = image_processor.match_template(
		settings.screenshot_path1, settings.screenshot_path2, 0.0001, masks = masks)
	if(match_loc != None):
		print("monster not nearby")
		return False
	else:
		print("monster nearby")
		return True


def is_bag_full():
	open_bag()
	time.sleep(0.5)

	is_bag_full = False
	result = read_bag_remain_capacity()
	if result < 6:
		is_bag_full = True

	click_left_return()
	click_right_return()

	return is_bag_full
