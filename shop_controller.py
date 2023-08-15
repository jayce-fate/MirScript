import btn_controller
import match_controller
import settings


def close_shop():
    btn_controller.click_left_return()
    match_loc = match_controller.wait_till_not_match_template("btn_page_left", settings.act_time_limit, settings.act_time)
    if match_loc != None:
        raise Exception("RESTART")