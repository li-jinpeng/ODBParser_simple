from utils import *
from global_data import *
from worker import *
from file_parser import *
from cmd_parser import *
from drawer import *

# 绘制PNG图片
dpi = 96*3

# init_work
worker = ParserWorker('1', False)


# 获取 profile 信息
profile_info, _ = line_record_parser(worker.edit_profile)

# 获取profile 画布
canvas, profile_img = get_canvas(cmd_parser(profile_info[0],True), dpi)
'''
# 画 profile
for info in profile_info:
    draw_cmd = cmd_parser(info,True,canvas)
    profile_img = draw(draw_cmd, profile_img, canvas)

# 画原点
draw_origin(profile_img, canvas)

# 保存profile图片
cv.imwrite(os.path.join(worker.output_pictures,'profile.png'),profile_img)

# 初始化自定义 symbol
# 初始化文字
'''
# 画顶层
# 画gtl层
gtl_img = get_blank_img(canvas)

gtl_info, gtl_symbols = line_record_parser(worker.edit_gtl)

for info in gtl_info:
    draw_cmd = cmd_parser([gtl_info, gtl_symbols], False , canvas)
    gtl_img = draw(draw_cmd, gtl_img, canvas)




