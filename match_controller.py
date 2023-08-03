import image_processor
import settings

def match_template(template_name):
    path = "{}{}.png".format("template_images/", template_name)
    match_loc = image_processor.match_template(
        settings.screenshot_path, path, 0.05)
    if(match_loc != None):
        return True
    return False
