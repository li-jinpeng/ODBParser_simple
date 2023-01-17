import os

# 工作文件夹路径
rootPath = os.path.abspath('.')
outputPath = os.path.join(rootPath,'output')
assetsPath = os.path.join(rootPath,'assets')

# 程序状态码
Fail = 1
Success = 2
Error = 3

# 工作文件ID
miscID = 1
#symbolID = 2
fontID = 3
featureID = 4
profileID = 5

# ODB++单位
MM = 'MM'
INCH = 'INCH'

# 图片格式
PNG = 1
SVG = 2

# polarity
P = 1
N = 2

# 绘画
POLY = 1 #多边形
CIRLE = 2
SECTOR = 3 #扇形

LINE = 4
LINE_C = 7
ARC = 5

STICKER = 6

# 旋转方向
CLOCKWISE = 1
COUNTER_CLOCKWISE = 2

# 正负无穷
PIF = 1000000
NIF = -1000000

# 画图边界像素
padding = 20

# 绘图颜色
# 画布默认为黑色，绘图为白色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (0, 0, 255)
BLUE = (255, 0, 0)

# 各层颜色 GBR
# gtl 顶层 gbl 底层
GL_COLOR = (41, 55, 36) # 墨绿色前景
GL_BACK = (36, 39, 30) # 墨绿色后景
# gts gbs 阻焊层
GS_COLOR = (99, 159, 182) # 与gl有色区相交处，黄铜色
GS_BACK = (43, 48, 49) # 与gl无色区相交处， 红铜色
# gto gbo 丝印层 白色
GT_COLOR = WHITE
# ad1 钻孔层 黑色
AD_COLOR = BLACK
# gko 禁止布线区 黑色
GK_COLOR = BLACK

# 线宽
THICKNESS = 1

# symbol_factor
symbol_factor = 0.001

DPI = 96


