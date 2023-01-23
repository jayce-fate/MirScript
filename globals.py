import settings
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