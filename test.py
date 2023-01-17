from utils import *
from global_data import *
from worker import *
from file_parser import *
from cmd_parser import *
from drawer import *

import time



# 绘制PNG图片
dpi = 96*15

# init_work
worker = ParserWorker('test', False)


# 获取 profile 信息
profile_info, _ = line_record_parser(worker.edit_profile)

# 获取profile 画布
canvas, profile_img = get_canvas(cmd_parser(profile_info[0],True), dpi)

# 画 profile
for info in profile_info:
    draw_cmd = cmd_parser(info,True,canvas)
    profile_img = draw(draw_cmd, profile_img, canvas)

gtl_info, gtl_symbols = line_record_parser('test.txt')
s = time.clock()
for info in gtl_info:
    draw_cmd = cmd_parser([gtl_info, gtl_symbols], False , canvas)
    gtl_img = draw(draw_cmd, profile_img, canvas)
e = time.clock()
print(e-s)
# 画原点
draw_origin(gtl_img, canvas)

cv.imwrite('test.png',gtl_img)





