# 包名activity查看方法
# win: adb shell dumpsys window | findstr mCurrentFocus
# mac: adb shell dumpsys window | grep mCurrentFocus
# 获取UserId
# win: adb shell ps | findstr air.com.PaladinOfMarphaNew
# mac: adb shell ps | grep air.com.PaladinOfMarphaNew
import caches.user as user

# adb.exe 的路径，模拟器安装路径下的bin文件夹里面有
# adb_path = "/Applications/NemuPlayer.app/Contents/MacOS/adb"
# adb_path = "/Applications/Genymotion.app/Contents/MacOS/tools/adb"
# adb_path = "/Applications/NoxAppPlayer.app/Contents/MacOS/adb"
# adb_path = r"C:\Program Files\platform-tools\adb.exe"
adb_path = "adb"

# 模拟器的地址
# device_address = "emulator-5554"
# device_address = "192.168.58.104:5555"
# device_address = "127.0.0.1:62001"
# device_address = "127.0.0.1:7555"
# device_address = "127.0.0.1:8555"
# device_address = "127.0.0.1:8556"
# device_address = "127.0.0.1:8559"
device_address = user.device_address

# 包名
package_name = "air.com.PaladinOfMarphaNew"

# 包启动activity
package_activity = "AppEntry"

# 获取UserId, mumu 原生 0, #N1 10, #N2 11, #N3 12, #N4 13
package_UserId = "0"

# 截屏保存路径
screenshot_path = r"temp_screenshot/screenshot.png"
screenshot_path1 = r"temp_screenshot/screenshot1.png"
screenshot_path2 = r"temp_screenshot/screenshot2.png"
screenshot_path3 = r"temp_screenshot/screenshot3.png"

# 检查屏幕是否有怪间隔时间（距离上次移动），单位秒
move_check_time = 40

go_back_check_time = 60

# 检查背包容量时间间隔，单位秒
move_bag_capacity_time = 600

# 读取当前坐标失败，尝试重新读取最大次数
read_coordinate_fail_limit = 10

# 最大尝试移动次数
move_try_limit = 5
# 单次移动距离
one_time_move_distance = 5

# 检测未拜师最大尝试次数（容错）
check_has_master_fail_limit = 3

# 读取地图名称失败最大尝试次数（容错）
read_map_name_fail_limit = 10

# 读取宠物血量失败最大尝试次数（容错）
read_pet_hp_fail_limit = 10

########### 练级路径 ###########
# 僵尸洞二层路径
zombie_cave_path = [(14,144),(20,138),(26,132),(33,132),(36,139),(42,145),(47,150),(51,154),(56,159),(61,164)
                    ,(67,164),(67,173),(72,173),(78,173),(78,166),(85,166),(90,160),(94,163),(100,158),(104,154),(107,151),(107,143),(116,134),(116,129),(109,122),(106,119),(106,115),(106,119),(109,122),(116,129),(116,134),(107,143),(107,151)
                    ,(110,154),(114,154),(120,160),(125,165),(129,169),(133,165),(138,165),(142,169),(146,169)
                    ,(151,164),(156,159),(151,154),(157,148),(149,140),(149,136),(155,130),(155,124),(149,118)
                    ,(146,115),(142,111),(142,105),(142,98),(151,88),(151,78),(158,78),(165,78),(171,72),(177,78)
                    ,(181,82),(187,88),(181,82),(171,72),(166,77),(162,73),(158,73),(152,79),(146,73),(140,67),(135,62),(135,52)
                    ,(130,47),(130,40),(136,34),(142,34),(146,38),(154,38),(160,32),(166,26),(172,20),(175,17)
                    ,(170,12),(166,16),(160,10),(158,8),(154,16),(166,28),(154,40),(151,37),(145,37),(141,33),(134,33)
                    ,(128,39),(123,39),(117,39),(112,34),(107,39),(101,39),(96,39),(90,45),(90,52),(90,60),(86,65)
                    ,(86,70),(86,76),(93,83),(100,90),(100,100),(100,109),(106,115),(100,109),(100,100),(100,90),(93,83),(86,76),(82,81),(82,85),(78,89),(72,89),(72,95)
                    ,(66,95),(62,99),(58,103),(50,103),(44,103),(39,108),(31,100),(31,90),(25,84),(25,74),(18,67)
                    ,(25,60),(33,52),(33,44),(33,36),(39,42),(31,50),(31,57),(21,67),(32,78),(23,87),(32,96)
                    ,(32,110),(27,105),(22,110),(28,116),(22,122),(28,128),(20,138),(14,144)]


# 生死之间路径
centipede_cave_path = [(15,55),(21,61),(26,61),(31,61),(39,67),(46,74),(52,80),(59,80),(65,80),(71,80),(76,75),
                        (81,70),(81,64),(81,56),(73,48),(64,48),(58,42),(52,36),(46,30),(41,25),(35,19),(29,13),
                        (26,17),(17,17),(24,17),(31,17),(37,17),(44,25),(52,32),(59,39),(59,53),(52,53),(46,53),
                        (40,59),(34,65),(26,57),(19,57),(13,57),(15,55)]

test_path = [(60,78),(62,76),(64,76),(64,78),(61,81),(60,80),(59,80)]

# 押镖
ya_biao_path = [(439,207),(467,207),(467,307),(500,340),(500,357),(517,373),(539,373),(626,460),(630,460),(640,470)
                ,(640,475),(652,487),(652,492),(662,502),(662,508),(677,523),(689,523),(754,588),(794,588),(797,591)
                ,(797,595),(807,605),(808,611),(838,641)]

# 押镖完整路径
ya_biao_full_path = [(438, 204), (437, 205), (436, 206), (436, 207), (436, 208), (437, 209), (438, 210), (439, 211), (439, 212), (439, 213), (439, 214), (439, 215), (439, 216), (439, 217), (439, 218), (439, 219), (439, 220), (439, 221), (439, 222), (439, 223), (439, 224), (439, 225), (439, 226), (439, 227), (439, 228), (439, 229), (439, 230), (439, 231), (439, 232), (439, 233), (439, 234), (439, 235), (439, 236), (439, 237), (439, 238), (439, 239), (439, 240), (439, 241), (439, 242), (440, 243), (441, 244), (442, 245), (443, 246), (444, 247), (445, 248), (446, 249), (447, 250), (448, 251), (449, 252), (450, 253), (451, 254), (452, 255), (453, 256), (454, 257), (455, 258), (456, 259), (457, 260), (458, 261), (459, 262), (460, 263), (461, 264), (462, 265), (463, 266), (464, 267), (464, 268), (464, 269), (464, 270), (464, 271), (464, 272), (464, 273), (464, 274), (464, 275), (464, 276), (464, 277), (464, 278), (464, 279), (464, 280), (464, 281), (464, 282), (464, 283), (464, 284), (464, 285), (464, 286), (464, 287), (464, 288), (464, 289), (464, 290), (464, 291), (464, 292), (464, 293), (464, 294), (464, 295), (464, 296), (464, 297), (464, 298), (464, 299), (464, 300), (464, 301), (464, 302), (464, 303), (464, 304), (464, 305), (464, 306), (464, 307), (464, 308), (464, 309), (464, 310), (465, 311), (466, 312), (467, 313), (468, 314), (469, 315), (470, 316), (471, 317), (472, 318), (473, 319), (474, 320), (475, 321), (476, 322), (477, 323), (478, 324), (479, 325), (480, 326), (481, 327), (482, 328), (483, 329), (484, 330), (485, 331), (486, 332), (487, 333), (488, 334), (489, 335), (490, 336), (491, 337), (492, 338), (493, 339), (494, 340), (495, 341), (496, 342), (497, 343), (497, 344), (497, 345), (497, 346), (497, 347), (497, 348), (497, 349), (497, 350), (497, 351), (497, 352), (497, 353), (498, 354), (499, 355), (500, 356), (501, 357), (502, 358), (503, 359), (504, 360), (505, 361), (506, 362), (507, 363), (508, 364), (509, 365), (510, 366), (511, 367), (512, 368), (513, 369), (514, 370), (515, 371), (516, 372), (517, 373), (518, 372), (519, 371), (520, 370), (521, 370), (522, 370), (523, 370), (524, 370), (525, 370), (526, 370), (527, 370), (528, 370), (529, 370), (530, 370), (531, 370), (532, 370), (533, 370), (534, 370), (535, 370), (536, 370), (537, 370), (538, 370), (539, 371), (540, 372), (541, 373), (542, 374), (543, 375), (544, 376), (545, 377), (546, 378), (547, 379), (548, 380), (549, 381), (550, 382), (551, 383), (552, 384), (553, 385), (554, 386), (555, 387), (556, 388), (557, 389), (558, 390), (559, 391), (560, 392), (561, 393), (562, 394), (563, 395), (564, 396), (565, 397), (566, 398), (567, 399), (568, 400), (569, 401), (570, 402), (571, 403), (572, 404), (573, 405), (574, 406), (575, 407), (576, 408), (577, 409), (578, 410), (579, 411), (580, 412), (581, 413), (582, 414), (583, 415), (584, 416), (585, 417), (586, 418), (587, 419), (588, 420), (589, 421), (590, 422), (591, 423), (592, 424), (593, 425), (594, 426), (595, 427), (596, 428), (597, 429), (598, 430), (599, 431), (600, 432), (601, 433), (602, 434), (603, 435), (604, 436), (605, 437), (606, 438), (607, 439), (608, 440), (609, 441), (610, 442), (611, 443), (612, 444), (613, 445), (614, 446), (615, 447), (616, 448), (617, 449), (618, 449), (619, 449), (620, 450), (621, 451), (622, 452), (623, 453), (624, 454), (625, 455), (626, 456), (627, 457), (628, 458), (629, 459), (630, 460), (631, 461), (632, 462), (631, 463), (631, 464), (631, 465), (631, 466), (632, 467), (633, 468), (634, 469), (635, 470), (636, 471), (637, 472), (638, 473), (639, 474), (640, 475), (639, 476), (638, 477), (637, 478), (638, 479), (639, 480), (640, 481), (641, 482), (642, 483), (643, 484), (644, 485), (645, 486), (646, 487), (647, 488), (648, 489), (649, 490), (649, 491), (649, 492), (649, 493), (649, 494), (649, 495), (650, 496), (651, 497), (652, 498), (653, 499), (654, 500), (655, 501), (656, 502), (657, 503), (658, 504), (659, 505), (660, 506), (661, 507), (662, 508), (663, 509), (664, 510), (665, 511), (666, 512), (667, 513), (668, 514), (669, 515), (670, 516), (671, 517), (672, 518), (673, 519), (674, 520), (675, 521), (676, 522), (677, 523), (678, 522), (679, 521), (680, 520), (681, 521), (682, 521), (683, 521), (684, 521), (685, 521), (686, 521), (687, 521), (688, 521), (689, 521), (690, 521), (691, 522), (692, 523), (693, 524), (694, 524), (695, 525), (696, 526), (697, 527), (698, 528), (699, 529), (700, 530), (701, 531), (702, 532), (703, 533), (704, 534), (705, 535), (706, 536), (707, 537), (708, 538), (709, 539), (710, 540), (711, 541), (712, 542), (713, 543), (714, 544), (715, 545), (716, 546), (717, 547), (718, 548), (719, 549), (720, 550), (721, 551), (722, 552), (723, 553), (724, 554), (725, 555), (726, 556), (727, 557), (728, 558), (729, 559), (730, 560), (731, 561), (732, 562), (733, 563), (734, 564), (735, 565), (736, 566), (737, 567), (738, 568), (739, 569), (740, 570), (741, 571), (742, 572), (743, 573), (744, 574), (745, 575), (746, 576), (747, 577), (748, 578), (749, 579), (750, 580), (751, 581), (752, 582), (753, 583), (754, 584), (755, 585), (756, 586), (757, 586), (758, 586), (759, 586), (760, 586), (761, 586), (762, 586), (763, 586), (764, 586), (765, 586), (766, 586), (767, 586), (768, 586), (769, 586), (770, 586), (771, 586), (772, 586), (773, 586), (774, 586), (775, 586), (776, 586), (777, 586), (778, 586), (779, 586), (780, 586), (781, 586), (782, 585), (783, 586), (784, 586), (785, 586), (786, 586), (787, 586), (788, 586), (789, 587), (790, 588), (791, 589), (792, 590), (793, 591), (794, 592), (795, 593), (796, 594), (797, 595), (796, 596), (795, 597), (795, 598), (796, 599), (797, 600), (798, 601), (799, 602), (800, 603), (801, 604), (802, 605), (803, 606), (804, 607), (805, 608), (806, 609), (807, 610), (808, 611), (809, 612), (810, 613), (811, 614), (812, 615), (813, 616), (814, 617), (815, 618), (816, 619), (817, 620), (818, 621), (819, 622), (820, 623), (821, 624), (822, 625), (823, 626), (824, 627), (825, 628), (826, 629), (827, 630), (828, 631), (829, 632), (830, 633), (831, 634), (832, 635), (833, 636), (834, 637), (835, 638), (836, 639), (837, 640), (838, 641)]

# 包里的
# 极品不扔
trash_list_white = [
                "jin_shou_zhuo",        #金手镯
                "jin_jie_zhi",          #金戒指
                "dao_shi_tou_kui",      #道士头盔
                "sheng_tie_jie_zhi",    #生铁戒指
                "deng_long_xiang_lian", #灯笼项链
                "jian_gu_shou_tao",     #坚固手套
                "ji_neng_shu",          #技能书
                "si_sheng_shou_tao",    #死神手套
                "hei_tang_shou_zhuo",   #黑檀手镯
                "dao_shi_shou_zhuo",    #道士手镯
                ]

# 极品不扔，非极品扔，需要二次确认
trash_list_green = [
                "bai_se_hu_chi_xiang_lian", #白色虎齿项链
                "shan_hu_jie_zhi",          #珊瑚戒指
                ]

# 强制扔，不管是不是极品
trash_list_force_drop = [
                "hei_se_shui_jing_jie_zhi", #黑色水晶戒指
                "mo_gui_xiang_lian",        #魔鬼项链
                "mo_li_shou_zhuo",          #魔力手镯
                "mei_li_jie_zhi",           #魅力戒指
                "ku_lou_jie_zhi",           #骷髅戒指
                "ku_lou_tou_kui",           #骷髅头盔
                "xiang_mo",                 #降魔
                "dao_de_jie_zhi",           #道德戒指
                "qing_xing_kui_jia_nan",    #轻型盔甲（男）
                "qing_xing_kui_jia_nv",     #轻型盔甲（女）
                "she_yan_jie_zhi",          #蛇眼戒指
                "lan_se_shui_jing_jie_zhi", #蓝色水晶戒指
                "lan_fei_cui_xiang_lian",   #蓝翡翠项链
                "zhu_di",                   #竹笛
                "po_hun",                   #破魂
                "zhen_zhu_jie_zhi",         #珍珠戒指
                "hai_hun",                  #海魂
                "zhan_ma_dao",              #斩马刀
                "fang_da_jing",             #放大镜
                "yan_yue",                  #偃月
                "ban_yue_wan_dao",          #半月弯刀
                "feng_huang_ming_zhu",      #凤凰明珠
                "ning_shuang",              #凝霜
                "ling_feng",                #凌风
                "ba_huang",                 #八荒
                "xiu_luo",                  #修罗
                ]

# 直接喝
trash_list_drink = [
                "qiang_xiao_jin_chuang_yao",    #强效金创药
                "qiang_xiao_mo_fa_yao",         #强效魔法药
                "mo_fa_yao_zhong_liang",        #魔法药中量
                "tai_yang_shui",                #太阳水
                "jin_chuang_yao_zhong_liang",   #金创药中量
                "biao_yin",                     #镖银
                ]


# 地上的垃圾名称（中文）
ground_green_trash_list = [
                "白色虎齿项链",
                "珊瑚戒指",
                ]

# 绑定的垃圾
binding_trash_list = [
                "tie_jian",                 #铁剑
                "qing_xing_kui_jia_nan",    #轻型盔甲男
                "qing_xing_kui_jia_nv",     #轻型盔甲女
                "wu_mu_jian",               #乌木剑
                "bu_yi_nv",                 #布衣女
                "bu_yi_nan",                #布衣男
                "bo_li_jie_zhi",            #玻璃戒指
                "you_xia_gong_lve",         #游侠攻略
                ]


item_name_dict = {
    "护身符(大)": "hu_shen_fu_da",
    "黄色药粉(中)": "huang_se_yao_fen_zhong",
    "灰色药粉(中)": "hui_se_yao_fen_zhong",
    "强效金创药": "qiang_xiao_jin_chuang_yao",
    "强效魔法药": "qiang_xiao_mo_fa_yao",
    "超级金创药": "chao_ji_jin_chuang_yao",
    "超级魔法药": "chao_ji_mo_fa_yao",
    "随机传送卷包": "sui_ji_chuan_song_juan_bao",
    "随机传送卷": "sui_ji_chuan_song_juan",
    "地牢逃脱卷": "di_lao_tao_tuo_juan",
    "回城卷": "hui_cheng_juan",
    "棕色栗子": "zhong_se_li_zi",
    "空位": "kong_wei",
    "技能书": "ji_neng_shu",
    "技能书激活": "ji_neng_shu_active",
    "军饷": "jun_xiang",
    "魔法药小量": "mo_fa_yao_xiao_liang",
    "魔法药中包": "mo_fa_yao_zhong_bao",
    "金创药小量": "jin_chuang_yao_xiao_liang",
}

bind_gold_item_list = [
    [
        "护身符",
        "护身符(大)",
        "黄色药粉(中)",
        "灰色药粉(中)",
        "金创药(中量)",
        "魔法药(中量)",
        "金创药中包",
        "魔法药中包",
        "强效金创药",
        "强效魔法药",
    ],
    [
        "超级金创药",
        "超级魔法药",
        "太阳水",
        "强效太阳水",
        "随机传送卷",
        "随机传送卷包",
        "地牢逃脱卷",
        "行会回城卷",
        "棕色栗子",
    ]
]

book_item_list = [
    [
        "攻杀剑术",
        "刺杀剑术",
        "火球术",
        "抗拒火环",
        "诱惑之光",
        "雷电术",
        "爆裂火焰",
        "火墙",
        "疾光电影",
        "治愈术",
    ],
    [
        "施毒术",
        "灵魂火符",
        "召唤骷髅",
        "隐身术",
        "集体隐身术",
        "幽灵战甲术",
        "技能书页",
        "订书棉线",
    ]
]

map_name_dict = {
    "meng_zhong_tu_cheng": "盟重土城",
    "fei_kuang_dong_bu": "废矿东部",
    "ku_lou_dong_1_ceng": "骷髅洞1层",
    "bi_qi_kuang_qu": "比奇矿区",
    "sheng_si_zhi_jian": "生死之间",
    "di_lao_yi_ceng_dong": "地牢一层东",
    "hei_an_di_dai": "黑暗地带",
    "tong_xin_xiao_jing": "同心小径",
    "ma_fa_qiu_chang": "玛法球场",
}
