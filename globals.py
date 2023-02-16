import settings
from enum import Enum

class Occupation(Enum):
    Default = 0
    Magician = 1
    Taoist = 2
    Warrior = 3

########### 全局变量 ###########

# 当前位置读取出错调整次数累计
adjust_count = 0

# 当前坐标
current_pos = (0, 0)

# 期望当前坐标
expect_current_pos = (0, 0)

# 期望路径序号
current_path_index = 0

# 读取当前坐标失败，尝试重新读取剩余次数
read_coordinate_fail_remain = settings.read_coordinate_fail_limit

# 检测未拜师剩余尝试次数
check_has_master_fail_remain = settings.check_has_master_fail_limit

# 连续走路步数统计（主要是押镖）
# step_count = 0

#屏幕（截图）尺寸
resolution = None

# 当前等级
current_lvl = 0

# 是否拜师
already_has_master = None

# 当前职业
occupation = Occupation.Default

skill_fire_ball_pos = None
skill_lighting_pos = None
skill_shield_pos = None
skill_heal_pos = None
skill_defence_pos = None
skill_invisible_pos = None
skill_poison_pos = None
skill_talisman_pos = None
skill_back_town = None
