import os
import time
import re
import cv2

import adb_controller

def one_step_walk_left():
	print("one_step_walk_left....")
	adb_controller.swipe((300,600),(250,600),1000)

def one_step_walk_right():
	print("one_step_walk_right....")
	adb_controller.swipe((300,600),(350,600),1000)

def one_step_walk_up():
	print("one_step_walk_up....")
	adb_controller.swipe((300,600),(300,550),1000)

def one_step_walk_down():
	print("one_step_walk_down....")
	adb_controller.swipe((300,600),(300,650),1000)