from utils import *
from global_data import *

def get_canvas(profile_cmd, dpi=DPI):
    '''
    输入 profile_cmd
    输出 画布尺寸和原点
    '''
    bl_x,bl_y,tr_x,tr_y = PIF,PIF,NIF,NIF #左下角和右上角坐标
    for cmd in profile_cmd:
        if cmd['type'] == LINE:
            bl_x = min(bl_x,cmd['info'][0],cmd['info'][2])
            bl_y = min(bl_y,cmd['info'][1],cmd['info'][3])
            tr_x = max(tr_x,cmd['info'][0],cmd['info'][2])
            tr_y = max(tr_y,cmd['info'][1],cmd['info'][3])
        else:
            cx = cmd['info'][4]
            cy = cmd['info'][5]
            r2 = (cx-cmd['info'][0])*(cx-cmd['info'][0]) + (cy-cmd['info'][1])*(cy-cmd['info'][1])
            r = math.sqrt(r2)
            bl_x = min(bl_x,cx-r)
            bl_y = min(bl_y,cx-r)
            tr_x = max(tr_x,cx+r)
            tr_y = max(tr_y,cy+r)
    ox = int(-bl_x * dpi) + padding
    oy = int(-bl_y * dpi) + padding
    w = int((tr_x - bl_x)*dpi) + 2*padding
    h = int((tr_y - bl_y)*dpi) + 2*padding
    img = np.zeros([h, w, 3], dtype = np.int32)
    return [ox,oy,w,h,dpi], img

def get_sticker_bound(pts, canvas):
    bl_x = min(pts[0][0], pts[1][0], pts[2][0], pts[3][0])
    tr_x = max(pts[0][0], pts[1][0], pts[2][0], pts[3][0])
    bl_y = min(pts[0][1], pts[1][1], pts[2][1], pts[3][1])
    tr_y = max(pts[0][1], pts[1][1], pts[2][1], pts[3][1])
    bl_x_, bl_y_ = ODBpoint2CVpoint(canvas,bl_x,bl_y)
    tr_x_, tr_y_ = ODBpoint2CVpoint(canvas,tr_x,tr_y)
    return (bl_x_, tr_y_, tr_x_, bl_y_)

def get_blank_img(canvas):
    return np.zeros([canvas[3],canvas[2],3],dtype = np.int32)

def ODBpoint2CVpoint(canvas,x,y):
    '''
    ODB++坐标转为CV坐标
    '''
    cvx = round(x*canvas[-1]) + canvas[0]
    cvy = canvas[3] - (round(y*canvas[-1] + canvas[1]))
    return (cvx, cvy)

'''
非填充图形
画直线 LINE
画弧 ARC
填充图形：
画圆 CIRLE
画多边形 POLY
'''
def draw_line(info, img, canvas):
    ptstart = ODBpoint2CVpoint(canvas, info[0], info[1])
    ptend = ODBpoint2CVpoint(canvas, info[2], info[3])
    cv.line(img, ptstart, ptend, WHITE, THICKNESS, cv.LINE_AA)

def draw_line_c(info, img, canvas):
    '''
    info = [x1,y1,x2,y2,d,color]
    '''
    ptstart = ODBpoint2CVpoint(canvas, info[0], info[1])
    ptend = ODBpoint2CVpoint(canvas, info[2], info[3])
    cv.line(img, ptstart, ptend, info[-1], info[-2], cv.LINE_AA)

def get_next_angle(start,end,mode):
    angles = [0, 90, 180, 270, 360, end]
    angles.sort()
    if mode == CLOCKWISE:
        if start == 360:
            start = 0
        for angle in angles:
            if angle > start:
                tmp_angle = angle
                break
        if tmp_angle == end:
            return Success, tmp_angle
        else:
            return Fail, tmp_angle
    else:
        angles.reverse()
        if start == 0:
            start = 360
        for angle in angles:
            if angle < start:
                tmp_angle = angle
                break
        if tmp_angle == end:
            return Success, tmp_angle
        else:
            return Fail, tmp_angle
        
def draw_arc(info, img, canvas):
    ps = ODBpoint2CVpoint(canvas,info[0],info[1])
    pe = ODBpoint2CVpoint(canvas,info[2],info[3])
    po = ODBpoint2CVpoint(canvas,info[4],info[5])
    r = int(math.sqrt((po[0]-ps[0])*(po[0]-ps[0])+(po[1]-ps[1])*(po[1]-ps[1])))
    sangle = (math.atan2(ps[1]-po[1],ps[0]-po[0])/(math.pi)*180 + 360) % 360
    eangle = (math.atan2(pe[1]-po[1],pe[0]-po[0])/(math.pi)*180 +360) % 360
    mode = info[6]
    if eangle == 0.0 and mode == CLOCKWISE:
        eangle = 360.0
    if sangle == 0.0 and mode == COUNTER_CLOCKWISE:
        sangle = 360.0
    while True:
        state, next_angle = get_next_angle(sangle,eangle,mode)
        cv.ellipse(img,po,(r,r),0,sangle,next_angle,WHITE,THICKNESS,cv.LINE_AA)
        if state == Success:
            break
        else:
            sangle = next_angle

def draw_sector(info, img, canvas):
    '''
    扇形(r == -1) 和 扇环
    info = [sx,sy,ex,ey,ox,oy,mode,d,color]
    '''
    ps = ODBpoint2CVpoint(canvas,info[0],info[1])
    pe = ODBpoint2CVpoint(canvas,info[2],info[3])
    po = ODBpoint2CVpoint(canvas,info[4],info[5])
    r = int(math.sqrt((po[0]-ps[0])*(po[0]-ps[0])+(po[1]-ps[1])*(po[1]-ps[1])))
    sangle = (math.atan2(ps[1]-po[1],ps[0]-po[0])/(math.pi)*180 + 360) % 360
    eangle = (math.atan2(pe[1]-po[1],pe[0]-po[0])/(math.pi)*180 +360) % 360
    mode = info[6]
    if eangle == 0.0 and mode == CLOCKWISE:
        eangle = 360.0
    if sangle == 0.0 and mode == COUNTER_CLOCKWISE:
        sangle = 360.0
    while True:
        state, next_angle = get_next_angle(sangle,eangle,mode)
        cv.ellipse(img,po,(r,r),0,sangle,next_angle,info[-1],info[-2],cv.LINE_AA)
        if state == Success:
            break
        else:
            sangle = next_angle

def draw_cirle(info, img, canvas):
    '''
    圆形d=-1 和 圆环
    info = [x, y, r, d, color]
    '''
    po = ODBpoint2CVpoint(canvas,info[0],info[1])
    r = round(info[2]*canvas[-1])
    d = round(info[-2]*canvas[-1])
    cv.circle(img,po,r,info[-1],d)


def draw_poly(info, img, canvas):
    '''
    info = [[(x1,y1),(x2,y2)...], color]
    '''
    point_list = info[0]
    vertex = []
    for point in point_list:
        v = ODBpoint2CVpoint(canvas,point[0],point[1])
        v_tmp = [v[0], v[1]]
        vertex.append(v_tmp)
    vertex_np = np.array([vertex],dtype=np.int32)
    cv.fillPoly(img, vertex_np, info[-1], cv.LINE_AA)

def draw_sticker(info, img, canvas):
    '''
    info = [sticker_canvas, color]
    '''
    if info[-1] == WHITE:
        return img | info[0]
    else:
        return img & info[0]


def draw(draw_cmd, img, canvas):
    for cmd in draw_cmd:
        if cmd['type'] == LINE:
            draw_line(cmd['info'], img, canvas)
        elif cmd['type'] == ARC:
            draw_arc(cmd['info'], img, canvas)
        elif cmd['type'] == POLY:
            draw_poly(cmd['info'],img,canvas)
        elif cmd['type'] == CIRLE:
            draw_cirle(cmd['info'],img,canvas)
        elif cmd['type'] == SECTOR:
            draw_sector(cmd['info'],img,canvas)
        elif cmd['type'] == LINE_C:
            draw_line_c(cmd['info'],img,canvas)
        elif cmd['type'] == STICKER:
            img = draw_sticker(cmd['info'], img, canvas)
    return img

def draw_origin(img, canvas):
    # 画原点
    draw_line_c([3/96,0,-3/96,0,3,(0,0,255)],img,canvas)
    draw_line_c([0,3/96,0,-3/96,3,(0,0,255)],img,canvas)
    draw_cirle([0,0,3/96,1/200,(0,0,255)],img,canvas)
    
