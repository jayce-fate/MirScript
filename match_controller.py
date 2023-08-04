import os
import time
import re
import cv2
import random

import adb_controller
import image_processor
import settings

def match_template(template_name, match_scope = None):
    path = "{}{}.png".format("template_images/", template_name)
    match_loc = image_processor.match_template(
        settings.screenshot_path, path, 0.05, match_scope)
    return match_loc

def wait_till_match_template(template_name,max_time,step_time,match_scope = None):
    print("Start to wait till match text: "+str(template_name)+", for up to "+str(max_time)+" seconds  ....")
    time_start = time.time()
    match_loc = None
    while(True):
        adb_controller.screenshot(settings.screenshot_path)
        match_loc = match_template(template_name, match_scope)
        if match_loc != None:
            break
        if(time.time() - time_start > max_time):
            print("Reach max_time but failed to match")
            break
        time.sleep(step_time)
    return match_loc
