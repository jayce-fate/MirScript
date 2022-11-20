import settings
########### 全局变量 ###########

# 当前位置读取出错调整次数累计
adjust_count = 0

# 当前x轴坐标
current_x = 0
# 当前y轴坐标
current_y = 0

# 期望当前x轴坐标
expect_current_x = 0
# 期望当前y轴坐标
expect_current_y = 0

# 期望路径序号
current_path_index = 0

# 读取当前坐标失败，尝试重新读取剩余次数
read_coordinate_fail_remain = settings.read_coordinate_fail_limit