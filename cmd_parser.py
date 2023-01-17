# 将ODB命令转换为绘图命令

from utils import *
from global_data import *
from symbols_parser import *
from drawer import *

def cmd_parser(odb_cmd, profile, canvas=None):
    '''
    输入 ODB++命令
    输出 绘画指令
    '''
    draw_cmd = []
    
    if not profile:
        cmd_odb, symbol_dict = odb_cmd[0], odb_cmd[1]
        for cmd_line in cmd_odb:
            if cmd_line['type'] == 'line':
                _, xs, ys, xe, ye, sym_num, polarity, dcode = cmd_line['info'].split(';')[0].split(' ')
                xs, ys, xe, ye = float(xs), float(ys), float(xe), float(ye)
                symbol = symbol_dict[sym_num]
                d = float(symbol[1:]) * symbol_factor
                r = d/2
                if polarity == 'P':
                    color = WHITE
                else:
                    color = BLACK  
                if ys == ye:
                    # 斜率为0
                    if symbol[0] == 'r':
                        draw_cmd.append({'type':POLY,'info':[[(xs,ys+r),(xs,ys-r),(xe,ye-r),(xe,ye+r)],color]})
                        draw_cmd.append({'type':CIRLE,'info':[xs,ys,r,-1,color]})
                        draw_cmd.append({'type':CIRLE,'info':[xe,ye,r,-1,color]})
                    else:
                        xs_, xe_ = min(xs,xe), max(xs,xe)
                        draw_cmd.append({'type':POLY,'info':[[(xs_-r,ys+r),(xs_-r,ys-r),(xe_+r,ye-r),(xe_+r,ye+r)],color]})
                else:
                    k = (xs - xe) / (ye - ys)
                    k_alpha = math.atan(k)
                    dy = r * math.sin(k_alpha)
                    dx = r * math.cos(k_alpha)
                    if symbol[0] == 'r':
                        draw_cmd.append({'type':POLY,'info':[[(xs+dx,ys+dy),(xs-dx,ys-dy),(xe-dx,ye-dy),(xe+dx,ye+dy)],color]})
                        draw_cmd.append({'type':CIRLE,'info':[xs,ys,r,-1,color]})
                        draw_cmd.append({'type':CIRLE,'info':[xe,ye,r,-1,color]})
                    else:
                        ys_, ye_ = min(ys,ye), max(ys,ye)
                        if k == 0:    
                            draw_cmd.append({'type':POLY,'info':[[(xs-r,ys_-r),(xs+r,ys_-r),(xe+r,ye_+r),(xe-r,ye_+r)],color]})
                        else:
                            k_ = -1 / k
                            k_alpha_ = math.atan(k_)
                            dy_ = r * math.sin(k_alpha_)
                            dx_ = r * math.cos(k_alpha_)
                            if ys_ == ys:
                                xs_, xe_ = xs, xe
                            else:
                                xs_, xe_ = xe, xs
                            draw_cmd.append({'type':POLY,'info':[[(xs_+dx-dx_,ys_+dy-dy_),(xs_-dx-dx_,ys_-dy-dy_),(xe_-dx+dx_,ye_-dy+dy_),( \
                                xe_+dx+dx_,ye_+dy+dy_)],color]})
            elif cmd_line['type'] == 'arc':
                _, xs, ys, xe, ye, xc, yc, sym_num, polarity, dcode, cw = cmd_line['info'].split(';')[0].split(' ')
                xs, ys, xe, ye, xc, yc = float(xs), float(ys), float(xe), float(ye), float(xc), float(yc)
                symbol = symbol_dict[sym_num]
                d = float(symbol[1:]) * symbol_factor 
                if cw == 'Y':
                    mode = CLOCKWISE
                else:
                    mode = COUNTER_CLOCKWISE
                if polarity == 'P':
                    color = WHITE
                else:
                    color = BLACK 
                draw_cmd.append({'type':SECTOR,'info':[xs,ys,xe,ye,xc,yc,mode,d,color]})
                if symbol[0] == 's':
                    r = d/2
                    r_ = r * math.sqrt(2)
                    if ys == yc or xs == xc:
                        draw_cmd.append({'type':POLY,'info':[[(xs-r,ys-r),(xs+r,ys-r),(xs+r,ys+r),(xs-r,ys+r)],color]})
                    else:
                        k = (ys-yc) / (xs-xc)
                        k_alpha = 90 - abs(math.atan(k) / (math.pi)*180) 
                        assert k_alpha > 0
                        alpha = k_alpha - 45
                        d1 = r_ * math.cos(math.radians(alpha))
                        d2 = r_ * math.sin(math.radians(alpha))
                        draw_cmd.append({'type':POLY,'info':[[(xs+d1,ys+d2),(xs+d2,ys-d1),(xs-d1,ys-d2),(xs-d2,ys+d1)],color]})
                    if ye == yc or xe == xc:
                        draw_cmd.append({'type':POLY,'info':[[(xe-r,ye-r),(xe+r,ye-r),(xe+r,ye+r),(xe-r,ye+r)],color]})
                    else:
                        k = (ye-yc) / (xe-xc)
                        k_alpha = 90 - abs(math.atan(k) / (math.pi)*180) 
                        assert k_alpha > 0
                        alpha = k_alpha - 45
                        d1 = r_ * math.cos(math.radians(alpha))
                        d2 = r_ * math.sin(math.radians(alpha))
                        draw_cmd.append({'type':POLY,'info':[[(xe+d1,ye+d2),(xe+d2,ye-d1),(xe-d1,ye-d2),(xe-d2,ye+d1)],color]})
            elif cmd_line['type'] == 'pad':
                """
                P <x> <y> <apt_def> <polarity> <dcode> <orient_def>;<atr>=<value>,...;ID=<id>
                """
                splits = cmd_line['info'].split(";")
                splits = [sp.strip() for sp in splits]
                items = splits[0].split(' ')
                if items[3] == '-1':
                    if int(items[8]) <= 7:
                        _, x, y, _, sym_num, resize_factor, polarity, dcode, orient_def = items
                        if (int(items[8])) <= 3:
                            flip_x = False
                            orient_deg = int(items[8]) * 90
                        else:
                            flip_x = True
                            orient_deg = (int(items[8]) - 4) * 90
                    else:
                        _, x, y, _, sym_num, resize_factor, polarity, dcode, orient_def, orient_deg = items
                        if int(orient_def) == 8:
                            flip_x = False
                        else:
                            flip_x = True
                else:
                    if int(items[6]) <= 7:
                        _, x, y, sym_num, polarity, dcode, orient_def = items
                        if (int(items[6])) <= 3:
                            flip_x = False
                            orient_deg = int(items[6]) * 90.0
                        else:
                            flip_x = True
                            orient_deg = (int(items[6]) - 4) * 90.0
                    else:
                        _, x, y, sym_num, polarity, dcode, orient_def, orient_deg = items
                        if int(orient_def) == 8:
                            flip_x = False
                        else:
                            flip_x = True
                    resize_factor = 1
                x, y, resize_factor, orient_deg = float(x), float(y), float(resize_factor), float(orient_deg) 
                symbol_str = symbol_dict[int(sym_num)] 
                if polarity == 'P':
                    color = WHITE
                else:
                    color = BLACK
                draw_cmd.extend(draw_symbol_cmd(x,y,symbol_str,orient_deg,flip_x,resize_factor,color,canvas))         
    else:       
        sx,sy,ex,ey,cx,cy = 0, 0, 0, 0, 0, 0
        for cmd_line in odb_cmd['info']:
            poly_cmd = {}
            cmd = cmd_line.split(' ')
            if cmd[0] == 'OB':
                sx = float(cmd[1])
                sy = float(cmd[2])
            elif cmd[0] == 'OS':
                ex = float(cmd[1])
                ey = float(cmd[2])
                poly_cmd['type'] = LINE
                poly_cmd['info'] = [sx,sy,ex,ey]
                draw_cmd.append(poly_cmd)
                sx = ex
                sy = ey
                poly_cmd = {}
            elif cmd[0] == 'OC':
                ex = float(cmd[1])
                ey = float(cmd[2])
                cx = float(cmd[3])
                cy = float(cmd[4])
                poly_cmd['type'] = ARC
                poly_cmd['info'] = [sx,sy,ex,ey,cx,cy,CLOCKWISE]
                if cmd[5] == 'N':
                    poly_cmd['info'][-1] = COUNTER_CLOCKWISE
                draw_cmd.append(poly_cmd)
                sx = ex
                sy = ey
                poly_cmd = {}
            else:
                continue
    return draw_cmd

def draw_symbol_cmd(x,y,symbol_str,rotate,mirror,resize,color,canvas):
    key, params = symbol_parse(symbol_str)
    if key == 'ROUND_SYMBOL':
        d = float(params[0]) * symbol_factor * resize
        r = d/2
        if mirror:
            x = -x
        return [{'type':CIRLE,'info':[x,y,r,-1,color]}]
    elif key == 'SQUARE_SYMBOL':
        s = float(params[0]) * symbol_factor * resize
        pts = [(x+s/2,y+s/2),(x+s/2,y-s/2),(x-s/2,y-s/2),(x-s/2,y+s/2)]
        pts_ = pts_rotate_mirror(pts, (x,y),rotate,mirror)
        return [{'type':POLY,'info':[pts_,color]}]
    elif key == 'RECT_SYMBOL':
        w, h = float(params[0])*symbol_factor*resize ,float(params[1])*symbol_factor*resize
        pts = [(x+w/2,y+h/2),(x+w/2,y-h/2),(x-w/2,y-h/2),(x-w/2,y+h/2)]
        pts_ = pts_rotate_mirror(pts, (x,y),rotate,mirror)
        return [{'type':POLY,'info':[pts_,color]}]
    elif key == 'ROUNDED_RECT_SYMBOL':
        draw_cmd = []
        w,h,rad,corners = float(params[0])*symbol_factor*resize ,float(params[1])*symbol_factor*resize\
            ,float(params[2])*symbol_factor*resize,params[3]
        # 2 1
        # 3 4
        if corners is None:
            corners = '1234'
        pts = [(x+w/2,y+h/2-rad),(x+w/2-rad,y+h/2),(x-w/2+rad,y+h/2),(x-w/2,y+h/2-rad),\
        (x-w/2,y-h/2+rad),(x-w/2+rad,y-h/2),(x+w/2-rad,y-h/2),(x+w/2,y-h/2+rad)]
        ptc = [(x+w/2-rad,y+h/2-rad),(x+w/2,y+h/2),\
               (x-w/2+rad,y+h/2-rad),(x-w/2,y+h/2),\
               (x-w/2+rad,y-h/2+rad),(x-w/2,y-h/2),\
               (x+w/2-rad,y-h/2+rad),(x+w/2,y-h/2)]
        ptc_ = pts_rotate_mirror(ptc,(x,y),rotate,mirror)
        pts_ = pts_rotate_mirror(pts,(x,y),rotate,mirror)
        draw_cmd.append({'type':POLY,'info':[pts_,color]})
        if mirror:
            mode = COUNTER_CLOCKWISE
        else:
            mode = CLOCKWISE
        for index in range(4):
            pto1, pto2 = ptc_[2*index],ptc_[2*index+1]
            if str(index+1) in corners:
                draw_cmd.append({'type':CIRLE,'info':[pto1[0],pto1[1],rad,-1,color]})
            else:
                draw_cmd.append({'type':POLY,'info':[[pt1,pt2,pto2],color]})
        return draw_cmd
    elif key == 'CHAMFERED_RECT_SYMBOL':
        draw_cmd = []
        w,h,rad,corners = float(params[0])*symbol_factor*resize ,float(params[1])*symbol_factor*resize\
            ,float(params[2])*symbol_factor*resize,params[3]
        # 2 1
        # 3 4
        if corners is None:
            corners = '1234'
        pts = [(x+w/2,y+h/2-rad),(x+w/2-rad,y+h/2),(x-w/2+rad,y+h/2),(x-w/2,y+h/2-rad),\
        (x-w/2,y-h/2+rad),(x-w/2+rad,y-h/2),(x+w/2-rad,y-h/2),(x+w/2,y-h/2+rad)]
        ptc = [(x+w/2-rad,y+h/2-rad),(x+w/2,y+h/2),\
               (x-w/2+rad,y+h/2-rad),(x-w/2,y+h/2),\
               (x-w/2+rad,y-h/2+rad),(x-w/2,y-h/2),\
               (x+w/2-rad,y-h/2+rad),(x+w/2,y-h/2)]
        ptc_ = pts_rotate_mirror(ptc,(x,y),rotate,mirror)
        pts_ = pts_rotate_mirror(pts,(x,y),rotate,mirror)
        draw_cmd.append({'type':POLY,'info':[pts_,color]})
        for index in range(4):
            pt1, pt2 = pts_[2*index], pts_[2*index+1]
            pto1, pto2 = ptc_[2*index],ptc_[2*index+1]
            if str(index+1) not in corners:
                draw_cmd.append({'type':POLY,'info':[[pt1,pt2,pto2],color]})
        return draw_cmd
    elif key == 'OVAL_SYMBOL':
        draw_cmd = []
        w,h = float(params[0])*symbol_factor*resize ,float(params[1])*symbol_factor*resize
        if w > h:
            r = h/2
            pts = [(x+w/2-r,y+h/2),(x-w/2+r,y+h/2),(x-w/2+r,y-h/2),(x+w/2-r,y-h/2)]
            ptc = [(x+w/2-r,y),(x-w/2+r,y)]
            pts_  = pts_rotate_mirror(pts,(x,y),rotate,mirror)
            ptc_  = pts_rotate_mirror(ptc,(x,y),rotate,mirror)
        else:
            r = w/2
            pts = [(x+w/2,y+h/2-r),(x-w/2,y+h/2-r),(x-w/2,y-h/2+r),(x+w/2,y-h/2+r)]
            ptc = [(x,y+h/2-r),(x,y-h/2+r)]
            pts_  = pts_rotate_mirror(pts,(x,y),rotate,mirror)
            ptc_  = pts_rotate_mirror(ptc,(x,y),rotate,mirror)
        draw_cmd.append({'type':POLY,'info':[pts_,color]})
        draw_cmd.append({'type':CIRLE,'info':[ptc_[0][0],ptc_[0][1],r,-1,color]})
        draw_cmd.append({'type':CIRLE,'info':[ptc_[1][0],ptc_[1][1],r,-1,color]})
        return draw_cmd
    elif key == 'DIAMOND_SYMBOL':
        w,h = float(params[0])*symbol_factor*resize ,float(params[1])*symbol_factor*resize
        pts = [(x,y+h/2),(x-w/2,y),(x,y-h/2),(x+w/2,y)]
        pts_ = pts_rotate_mirror(pts,(x,y),rotate,mirror)
        return [{'type':POLY,'info':[pts_,color]}]
    elif key == 'OCTAGON_SYMBOL':
        w,h,r = float(params[0])*symbol_factor*resize ,float(params[1])*symbol_factor*resize,float(params[2])*symbol_factor*resize
        pts = [(x+w/2-r,y+h/2),(x-w/2+r,y+h/2),(x-w/2,y+h/2-r),(x-w/2,y-h/2+r),\
            (x-w/2+r,y-h/2),(x+w/2-r,y-h/2),(x+w/2,y-h/2+r),(x+w/2,y+h/2-r)]
        pts_ = pts_rotate_mirror(pts,(x,y),rotate,mirror)
        return [{'type':POLY,'info':[pts_,color]}]
    elif key == 'ROUND_DONUT_SYMBOL':
        od,id = float(params[0])*symbol_factor*resize ,float(params[1])*symbol_factor*resize
        if mirror:
            x = -x
        r = (od + id) / 4 
        d = (od - id) / 2
        return [{'type':CIRLE,'info':[x,y,r,d,color]}]
    elif key == 'SQUARE_DONUT_SYMBOL':
        od,id = float(params[0])*symbol_factor*resize ,float(params[1])*symbol_factor*resize
        pts1 = [(x+od/2,y+od/2),(x-od/2,y+od/2),(x-od/2,y+id/2),(x+od/2,y+id/2)]
        pts2 = [(x+od/2,y+id/2),(x+id/2,y+id/2),(x+id/2,y-id/2),(x+od/2,y-id/2)]
        pts3 = [(x-id/2,y+id/2),(x-od/2,y+id/2),(x-od/2,y-id/2),(x-id/2,y-id/2)]
        pts4 = [(x-od/2,y-id/2),(x-od/2,y-od/2),(x+od/2,y-od/2),(x+od/2,y-id/2)]
        pts1_ = pts_rotate_mirror(pts1,(x,y),rotate,mirror)
        pts2_ = pts_rotate_mirror(pts2,(x,y),rotate,mirror)
        pts3_ = pts_rotate_mirror(pts3,(x,y),rotate,mirror)
        pts4_ = pts_rotate_mirror(pts4,(x,y),rotate,mirror)
        return [{'type':POLY,'info':[pts1_,color]},{'type':POLY,'info':[pts2_,color]},\
            {'type':POLY,'info':[pts3_,color]},{'type':POLY,'info':[pts4_,color]}]
    elif key == 'SQUARE_ROUND_DONUT_SYMBOL':
        od,id = float(params[0])*symbol_factor*resize ,float(params[1])*symbol_factor*resize
        pts = [(x+od/2,y+od/2),(x-od/2,y+od/2),(x-od/2,y-od/2),(x+od/2,y-od/2)]
        pts_ = pts_rotate_mirror(pts,(x,y),rotate,mirror)
        o = (x,y)
        if mirror:
            o = (-x,y)
        blank_canvas = get_blank_img(canvas)
        draw_poly([pts_, WHITE], blank_canvas, canvas)
        draw_cirle([o[0],o[1],id/2,-1,BLACK], blank_canvas, canvas)
        return [{'type':STICKER,'info':[blank_canvas,color]}]
    elif key == 'ROUNDED_SQUARE_DONUT_SYMBOL':
        od,id,rad,corners = params[0]*symbol_factor*resize ,params[1]*symbol_factor*resize, params[2]*symbol_factor*resize, params[3]
        # 2 1
        # 3 4
        if corners == '':
            corners = '1234'
        # pts = [oo1,os1,oe1,p11n,p11w,p1n,p1w,p12n,p12w]
        mode = CLOCKWISE
        if mirror:
            mode = COUNTER_CLOCKWISE
        d = (od - id) / 2
        r1 = rad
        r2 = r1 + d/2
        r3 = r1 + d
        p1x, p1y = x+id/2-rad, y+id/2-rad
        pts1 = [(p1x,p1y),(p1x,p1y+r2),(p1x+r2,p1y),(p1x,p1y+r1),(p1x,p1y+r3),(p1x+r1,p1y+r1),(p1x+r3,p1y+r3),(p1x+r1,p1y),(p1x+r3,p1y)]
        p2x, p2y = x-id/2+rad, y+id/2-rad
        pts2 = [(p2x,p2y),(p2x-r2,p2y),(p2x,p2y+r2),(p2x-r1,p2y),(p2x-r3,p2y),(p2x-r1,p2y+r1),(p2x-r3,p2y+r3),(p2x,p2y+r1),(p2x,p2y+r3)]
        p3x,p3y = x-id/2+rad, y-id/2+rad
        pts3 = [(p3x,p3y),(p3x,p3y-r2),(p3x-r2,p3y),(p3x,p3y-r1),(p3x,p3y-r3),(p3x-r1,p3y-r1),(p3x-r3,p3y-r3),(p3x-r1,p3y),(p3x-r3,p3y)]
        p4x,p4y = x+id/2-rad,y-id/2+rad
        pts4 = [(p4x,p4y),(p4x+r2,p4y),(p4x,p4y-r2),(p4x+r1,p4y),(p4x+r3,p4y),(p4x+r1,p4y-r1),(p4x+r3,p4y-r3),(p4x,p4y-r1),(p4x,p4y-r3)]
        pts1_ = pts_rotate_mirror(pts1,(x,y),rotate,mirror)
        pts2_ = pts_rotate_mirror(pts2,(x,y),rotate,mirror)
        pts3_ = pts_rotate_mirror(pts3,(x,y),rotate,mirror)
        pts4_ = pts_rotate_mirror(pts4,(x,y),rotate,mirror)
        draw_cmd = []
        draw_cmd.append({'type':POLY,'info':[[pts1_[3],pts1_[4],pts2_[8],pts2_[7]],color]})
        draw_cmd.append({'type':POLY,'info':[[pts2_[3],pts2_[4],pts3_[8],pts3_[7]],color]})
        draw_cmd.append({'type':POLY,'info':[[pts3_[3],pts3_[4],pts4_[8],pts4_[7]],color]})
        draw_cmd.append({'type':POLY,'info':[[pts4_[3],pts4_[4],pts1_[8],pts1_[7]],color]})
        pts = [pts1_,pts2_,pts3_,pts4_]
        for index in range(4):
            if str(index+1) in corners:
                draw_cmd.append({'type':SECTOR,'info':[pts[index][1][0],pts[index][1][1],pts[index][2][0],pts[index][2][1],pts[index][0][0],pts[index][0][1],mode,d,color]})
            else:
                draw_cmd.append({'type':POLY,'info':[[pts[index][3],pts[index][4],pts[index][6],pts[index][8],pts[index][7],pts[index][5]],color]}) 
        return draw_cmd
    elif key == 'RECT_DONUT_SYMBOL':
        ow,oh,lw = params[0]*symbol_factor*resize, params[1]*symbol_factor*resize, params[2]*symbol_factor*resize
        pts1 = [(x+ow/2-lw,y+oh/2-lw),(x+ow/2-lw,y+oh/2),(x-ow/2+lw,y+oh/2),(x-ow/2+lw,y+oh/2-lw)]
        pts2 = [(x-ow/2+lw,y+oh/2),(x-ow/2,y+oh/2),(x-ow/2,y-oh/2),(x-ow/2+lw,y-oh/2)]
        pts3 = [(x-ow/2+lw,y-oh/2+lw),(x-ow/2+lw,y-oh/2),(x+ow/2-lw,y-oh/2),(x+ow/2-lw,y-oh/2+lw)]
        pts4 = [(x+ow/2-lw,y-oh/2),(x+ow/2,y-oh/2),(x+ow/2,y+oh/2),(x+ow/2-lw,y+oh/2)]
        pts = [pts1,pts2,pts3,pts4]
        pts_ = []
        for pt in pts:
            pts_.append(pts_rotate_mirror(pt,(x,y),rotate,mirror))
        draw_cmd = []
        for pt in pts_:
            draw_cmd.append({'type':POLY,'info':[pt,color]})
        return draw_cmd
    elif key == 'ROUNDED_RECT_DONUT_SYMBOL':
        ow,oh,lw,rad,corners = params[0]*symbol_factor*resize, params[1]*symbol_factor*resize, params[2]*symbol_factor*resize\
            ,params[3]*symbol_factor*resize, params[4]
        if corners == '':
            corners = '1234'
        pts1 = [(x+ow/2-lw,y+oh/2-lw),(x+ow/2-lw,y+oh/2),(x-ow/2+lw,y+oh/2),(x-ow/2+lw,y+oh/2-lw)]
        pts2 = [(x+ow/2-lw,y-oh/2+lw),(x+ow/2-lw,y-oh/2),(x-ow/2+lw,y-oh/2),(x-ow/2+lw,y-oh/2+lw)]
        pts3 = [(x+ow/2-lw,y+oh/2-lw),(x+ow/2,y+oh/2-lw),(x+ow/2,y-oh/2+lw),(x+ow/2-lw,y-oh/2+lw)]
        pts3 = [(x-ow/2+lw,y+oh/2-lw),(x-ow/2,y+oh/2-lw),(x-ow/2,y-oh/2+lw),(x-ow/2+lw,y-oh/2+lw)]
        pts = [pts1,pts2,pts2,pts3]
        draw_cmd = []
        for pt in pts:
            draw_cmd.append({'type':POLY,'info':[pts_rotate_mirror(pt,(x,y),rotate,mirror),color]})
        mode = CLOCKWISE
        if mirror:
            mode = COUNTER_CLOCKWISE
        d = lw
        for index in range(4):
            c1 = 1-((index%3+1)//2)*2 # 1 -1 -1 1
            c2 = 1-(index//2)*2 # 1 1 -1 -1
            ox = x + (ow/2-lw-rad)*c1
            oy = y + (oh/2-lw-rad)*c2
            r = rad + lw/2
            if str(index+1) in corners:
                sx = -(math.sin(math.pi*index/2))*r + ox
                sy = (math.cos(math.pi*index/2))*r + oy
                ex = (math.cos(math.pi*index/2))*r + ox
                ey = (math.sin(math.pi*index/2))*r + oy
                pts = pts_rotate_mirror([(sx,sy),(ex,ey),(ox,oy)],(x,y),rotate,mirror)
                draw_cmd.append({'type':SECTOR,'info':[pts[0],pts[1],pts[2],pts[3],pts[4],pts[5],mode,d,color]})
            else:
                pts = [(ox+c1*rad,oy),(ox+c1*(rad+lw),oy),(ox+c1*(rad+lw),oy+c2*(rad+lw))\
                    ,(ox,oy+c2*(rad+lw)),(ox,oy+c2*rad),(ox+c1*rad,oy+c2*rad)]
                pts_ = pts_rotate_mirror(pts,(x,y),rotate,mirror)
                draw_cmd.append({'type':POLY,'info':[pts_,color]})
    elif key == 'OVAL_DONUT_SYMBOL':
        ow,oh,lw = params[0]*symbol_factor*resize, params[1]*symbol_factor*resize, params[2]*symbol_factor*resize
        draw_cmd = []
        d = lw
        mode = CLOCKWISE
        if mirror:
            mode = COUNTER_CLOCKWISE
        if ow > oh:
            r3 = oh/2
            r1 = r3 - lw
            r2 = r3 - lw/2
            pts1 = [(x+ow/2-r3,y+r1),(x+ow/2-r3,y+r3),(x-ow/2+r3,y+r3),(x-ow/2+r3,y+r1)]
            pts2 = [(x+ow/2-r3,y+r1),(x+ow/2-r3,y+r3),(x-ow/2+r3,y+r3),(x-ow/2+r3,y+r1)]
            draw_cmd.append({'type':POLY,'info':[pts_rotate_mirror(pts1,(x,y),rotate,mirror),color]})
            draw_cmd.append({'type':POLY,'info':[pts_rotate_mirror(pts2,(x,y),rotate,mirror),color]})
            pts = [(x+ow/2-r3,y+oh/2-lw/2),(x+ow/2-r3,y-oh/2+lw/2),(x+ow/2-r3,y)]
            pts_ = pts_rotate_mirror(pts1,(x,y),rotate,mirror)
            draw_cmd.append({'type':SECTOR,'info':[pts_[0],pts_[1],pts_[2],pts_[3],pts_[4],pts_[5],mode,d,color]})
            pts = [(x-ow/2+r3,y-oh/2+lw/2),(x-ow/2+r3,y+oh/2-lw/2),(x-ow/2+r3,y)]
            pts_ = pts_rotate_mirror(pts1,(x,y),rotate,mirror)
            draw_cmd.append({'type':SECTOR,'info':[pts_[0],pts_[1],pts_[2],pts_[3],pts_[4],pts_[5],mode,d,color]})
        else:
            r3 = ow/2
            r1 = r3 - lw
            r2 = r3 - lw/2
            pts1 = [(x+r1,y+oh/2-r3),(x+r3,y+oh/2-r3),(x+r3,y-oh/2+r3),(x+r1,y-oh/2+r3)]
            pts2 = [(x-r1,y+oh/2-r3),(x-r3,y+oh/2-r3),(x-r3,y-oh/2+r3),(x-r1,y-oh/2+r3)]
            draw_cmd.append({'type':POLY,'info':[pts_rotate_mirror(pts1,(x,y),rotate,mirror),color]})
            draw_cmd.append({'type':POLY,'info':[pts_rotate_mirror(pts2,(x,y),rotate,mirror),color]})
            pts = [(x-ow/2+lw/2,y+oh/2-r3),(x+ow/2-lw/2,y+oh/2-r3),(x,y+oh/2-r3)]
            pts_ = pts_rotate_mirror(pts1,(x,y),rotate,mirror)
            draw_cmd.append({'type':SECTOR,'info':[pts_[0],pts_[1],pts_[2],pts_[3],pts_[4],pts_[5],mode,d,color]})
            pts = [(x+ow/2-lw/2,y-oh/2+r3),(x-ow/2+lw/2,y-oh/2+r3),(x,y-oh/2+r3)]
            pts_ = pts_rotate_mirror(pts1,(x,y),rotate,mirror)
            draw_cmd.append({'type':SECTOR,'info':[pts_[0],pts_[1],pts_[2],pts_[3],pts_[4],pts_[5],mode,d,color]})
        return draw_cmd
    elif key == 'HORIZONTAL_HEXAGON_SYMBOL':
        w,h,r = params[0]*symbol_factor*resize, params[1]*symbol_factor*resize, params[2]*symbol_factor*resize
        pts = [(x+w/2-r,y+h/2),(x-w/2+r,y+h/2),(x-w/2,y),(x-w/2+r,y-h/2),\
            (x+w/2-r,y-h/2),(x+w/2,y)]
        pts_ = pts_rotate_mirror(pts,(x,y),rotate,mirror)
        return [{'type':POLY,'info':[pts_,color]}]
    elif key == 'VERTICAL_HEXAGON_SYMBOL':
        w,h,r = params[0]*symbol_factor*resize, params[1]*symbol_factor*resize, params[2]*symbol_factor*resize
        pts = [(x+w/2,y+h/2-r),(x,y+h/2),(x-w/2,y+h/2-r),(x-w/2,y-h/2+r),\
            (x,y-h/2),(x+w/2,y-h/2+r)]
        pts_ = pts_rotate_mirror(pts,(x,y),rotate,mirror)
        return [{'type':POLY,'info':[pts_,color]}]
    elif key == 'BUTTERFLY_SYMBOL':
        d = params[0]*symbol_factor*resize
        r = d/2
        draw_cmd = []
        mode = CLOCKWISE
        if mirror:
            mode = COUNTER_CLOCKWISE
        pts = [(x-r,y),(x,y+r),(x,y)]
        pts_ = pts_rotate_mirror(pts,(x,y),rotate,mirror)
        draw_cmd.append({'type':SECTOR,'info':[pts_[0],pts_[1],pts_[2],pts_[3],pts_[4],pts_[5],mode,-1,color]})
        pts = [(x+r,y),(x,y-r),(x,y)]
        pts_ = pts_rotate_mirror(pts,(x,y),rotate,mirror)
        draw_cmd.append({'type':SECTOR,'info':[pts_[0],pts_[1],pts_[2],pts_[3],pts_[4],pts_[5],mode,-1,color]})
        return draw_cmd
    elif key == 'SQUARE_BUTTERFLY_SYMBOL':
        s = params[0]*symbol_factor*resize
        r = s/2
        draw_cmd = []
        pts = [(x-r,y),(x-r,y+r),(x,y+r),(x,y)]
        pts_ = pts_rotate_mirror(pts,(x,y),rotate,mirror)
        draw_cmd.append({'type':POLY,'info':[pts_,color]})
        pts = [(x+r,y),(x+r,y-r),(x,y-r),(x,y)]
        pts_ = pts_rotate_mirror(pts,(x,y),rotate,mirror)
        draw_cmd.append({'type':POLY,'info':[pts_,color]})
        return draw_cmd
    elif key == 'TRIANGLE_SYMBOL':
        base,h = params[0]*symbol_factor*resize, params[1]*symbol_factor*resize
        pts = [(x,y+h/2),(x+base/2,y-h/2),(x-base/2,y-h/2)]
        pts_ = pts_rotate_mirror(pts,(x,y),rotate,mirror)
        return [{'type':POLY,'info':[pts_,color]}]
    elif key == 'HALF_OVAL_SYMBOL':
        w,h = params[0]*symbol_factor*resize, params[1]*symbol_factor*resize
        draw_cmd = []
        mode = CLOCKWISE
        if mirror:
            mode = COUNTER_CLOCKWISE
        if w*2>h:
            r = h/2
            pts = [(x-w/2,y+h/2),(x-w/2,y-h/2),(x+w/2-r,y-h/2),(x+w/2-r,y+h/2)]
            pts_ = pts_rotate_mirror(pts,(x,y),rotate,mirror)
            draw_cmd.append({'type':POLY,'info':[pts_,color]})
            pts = [(x+w/2-r,y+h/2),(x+w/2-r,y-h/2),(x+w/2-r,y)]
            pts_ = pts_rotate_mirror(pts,(x,y),rotate,mirror)
            draw_cmd.append({'type':SECTOR,'info':[pts_[0],pts_[1],pts_[2],pts_[3],pts_[4],pts_[5],mode,-1,color]})
        else:
            r = w/2
            pts = [(x-w/2,y-h/2),(x+w/2,y-h/2),(x+w/2,y+h/2-r),(x-w/2,y+h/2-r)]
            pts_ = pts_rotate_mirror(pts,(x,y),rotate,mirror)
            draw_cmd.append({'type':POLY,'info':[pts_,color]})
            pts = [(x-w/2,y+h/2-r),(x+w/2,y+h/2-r),(x,y+h/2-r)]
            pts_ = pts_rotate_mirror(pts,(x,y),rotate,mirror)
            draw_cmd.append({'type':SECTOR,'info':[pts_[0],pts_[1],pts_[2],pts_[3],pts_[4],pts_[5],mode,-1,color]})
        return draw_cmd
    elif key == 'ROUNDED_ROUND_THERMAL_SYMBOL':
        od,id,angle,num_spokes,gap = params[0]*symbol_factor*resize, params[1]*symbol_factor*resize\
            , float(params[2]), int(params[3]), float(params[4])
        r = (od+id)/2
        theta1 = (math.asin(gap/(2*r)) + math.pi/2) % (math.pi/2)
        theta2 = (od-id)/(2*r)
        theta = theta1 + theta2
        d_theta = 2*math.pi / num_spokes
        s_theta = math.radians(angle)
        pts = []
        mode = COUNTER_CLOCKWISE
        if mirror:
            mode = CLOCKWISE
        d = (od-id)/2
        for i in range(num_spokes):
            c_theta = s_theta + i*d_theta
            c_theta1 = c_theta - theta
            pts.append((x+r*math.cos(c_theta1),y+r*math.sin(c_theta1)))
            c_theta2 = c_theta + theta
            pts.append((x+r*math.cos(c_theta2),y+r*math.sin(c_theta2)))
        pts_ = pts_rotate_mirror(pts,(x,y),rotate,mirror)
        draw_cmd = []
        for index in range(num_spokes):
            p1 = pts_[(index*2 + 1)%num_spokes]
            p2 = pts_[(index*2 + 2)%num_spokes]
            po = (x,y)
            if mirror:
                po = (-x,y)
            draw_cmd.append({'type':SECTOR,'info':[p1[0],p1[1],p2[0],p2[1],po[0],po[1],mode,d,color]})
    elif key == 'SQAURED_ROUND_THERMAL_SYMBOL':
        od,id,angle,num_spokes,gap = params[0]*symbol_factor*resize, params[1]*symbol_factor*resize\
            , float(params[2]), int(params[3]), float(params[4])
        r = (od+id)/2
        d = (od-id)/2
        ox, oy = x, y 
        if mirror:
            ox = -x
        blank_sticker = get_blank_img(canvas)
        draw_cirle([ox,oy,r,d,WHITE],blank_sticker,canvas)
        r_ = id/2
        s_theta = math.radians(angle)
        d_theta = 2*math.pi/num_spokes
        theta = (math.asin(gap/(2*r_)) + math.pi/2) % (math.pi/2)
        for index in range(num_spokes):
            c_theta = s_theta + index*d_theta 
            c_theta1 = c_theta + theta
            c_theta2 = c_theta - theta
            pts = [(id/2*math.cos(c_theta1),id/2*math.sin(c_theta1)),(id/2*math.cos(c_theta1)+d*math.cos(c_theta),id/2*math.sin(c_theta1)+d*math.sin(c_theta))\
                ,(id/2*math.cos(c_theta2)+d*math.cos(c_theta),id/2*math.sin(c_theta2)+d*math.sin(c_theta)),(id/2*math.cos(c_theta2),id/2*math.sin(c_theta2))]
            pts_ = pts_rotate_mirror(pts,(x,y),rotate,mirror)
            draw_poly([pts_,BLACK],blank_sticker,canvas)
        return [{'type':STICKER,'info':[blank_sticker,color]}]
    elif key == 'SQUARE_THERMAL_SYMBOL':
        od,id,angle,num_spokes,gap = params[0]*symbol_factor*resize, params[1]*symbol_factor*resize\
            , float(params[2]), int(params[3]), float(params[4])
        # 有待完善
        assert gap <= math.sqrt(2) * id/2
        assert mirror is False
        os = od
        dx = math.sqrt(2) * os / 2
        blank_sticker = get_blank_img(canvas)
        pts = [(x+os/2,y+os/2),(x-os/2,y+os/2),(x-os/2,y-os/2),(x+os/2,y-os/2)]
        pts_ = pts_rotate_mirror(pts,(x,y),rotate,mirror)
        draw_poly([pts_,WHITE],blank_canvas,canvas)
        pts = [(x+id/2,y+id/2),(x-id/2,y+id/2),(x-id/2,y-id/2),(x+id/2,y-id/2)]
        pts_ = pts_rotate_mirror(pts,(x,y),rotate,mirror)
        draw_poly([pts_,BLACK],blank_canvas,canvas)
        for index in range(num_spokes):
            # x, y
            theta = math.radians(angle) + index*(2*math.pi/num_spokes)
            theta += rotate
            x1 = x + math.cos(theta)*dx
            y1 = y + math.sin(theta)*dx
            draw_line_c([x,y,x1,y1,gap,BLACK],blank_sticker,canvas)
        return [{'type':STICKER,'info':[blank_sticker,color]}]
    elif key == 'SQUARE_THERMAL_OPEN_CORNERS_SYMBOL':
        od,id,angle,num_spokes,gap = params[0]*symbol_factor*resize, params[1]*symbol_factor*resize\
            , float(params[2]), int(params[3]), float(params[4])
        if num_spokes == 1:
            if (angle + 90 - 45) % 90 == 0:
                rotate = angle - 45 + rotate
                pts = [(x+id/2-gap/math.sqrt(2),y+id/2),(x-id/2,y+id/2),(x-id/2,y-id/2),\
                    (x+id/2,y-id/2),(x+id/2,y+id/2-gap/math.sqrt(2)),(x+od/2,y+id/2-gap/math.sqrt(2)),\
                        (x+od/2,y-od/2),(x-od/2,y-od/2),(x-od/2,y+od/2),(x+id/2-gap/math.sqrt(2),y+od/2)]
            else:
                rotate = angle + rotate
                pts = [(x+id/2,y+gap/2),(x+id/2,y+id/2),(x-id/2,y+id/2),(x-id/2,y-id/2),\
                    (x+id/2,y-id/2),(x+id/2,y-gap/2),(x+od/2,y-gap/2),(x+od/2,y-od/2),\
                        (x-od/2,y-od/2),(x-od/2,y+od/2),(x+od/2,y+od/2),(x+od/2,y+gap/2)]
            pts_ = pts_rotate_mirror(pts,(x,y),rotate,mirror)
            return [{'type':POLY,'info':[pts_,color]}]
        elif num_spokes == 2:
            if (angle + 90 - 45) % 90 == 0:
                rotate = angle - 45 + rotate
                pts = [(x+id/2-gap/math.sqrt(2),y+id/2),(x-id/2,y+id/2),(x-id/2,y-id/2+gap/math.sqrt(2)),\
                    (x-od/2,y-id/2+gap/math.sqrt(2)),(x-od/2,y+od/2),(x+id/2-gap/math.sqrt(2),y+od/2)]
            else:
                rotate = angle + rotate
                pts = [(x+id/2,y+gap/2),(x+id/2,y+id/2),(x-id/2,y+id/2),(x-id/2,y+gap/2),\
                    (x-od/2,y+gap/2),(x-od/2,y+od/2),(x+od/2,y+od/2),(x+od/2,y+gap/2)]
            pts1 = pts_rotate_mirror(pts,(x,y),rotate,mirror)
            pts2 = pts_rotate_mirror(pts,(x,y),rotate+180,mirror)  
            return [{'type':POLY,'info':[pts1,color]},{'type':POLY,'info':[pts2,color]}]
        else:
            # num_spokes == 4
            draw_cmd = []
            if (angle + 90 - 45) % 90 == 0:
                pts = [(x+id/2,y+id/2-gap/math.sqrt(2)),(x+od/2,y+id/2-gap/math.sqrt(2)),\
                    (x+od/2,y-id/2+gap/math.sqrt(2)),(x+id/2,y-id/2+gap/math.sqrt(2))]
            else:
                pts = [(x+id/2,y+gap/2),(x+id/2,y+id/2),(x+gap/2,y+id/2),(x+gap/2,y+od/2),\
                    (x+od/2,y+od/2),(x+od/2,y+gap/2)]
            for index in range(4):
                pts_ = pts_rotate_mirror(pts,(x,y),rotate+90*index,mirror)
                draw_cmd.append({'type':POLY,'info':[pts_,color]})
            return draw_cmd
    elif key == 'LINE_THERMAL_SYMBOL':
        od,id,angle,num_spokes,gap = params[0]*symbol_factor*resize, params[1]*symbol_factor*resize\
            , float(params[2]), int(params[3]), float(params[4])
        # num_spokes == 4 && angle == 45
        d = (od-id)/2
        r = d/2
        pts = [(x+id/2+r,y-od/2+r*2+gap/math.sqrt(2)),(x+id/2+r,y+od/2-r*2-gap/math.sqrt(2))]
        draw_cmd = []
        for index in range(4):
            pts_ = pts_rotate_mirror(pts,(x,y),rotate+90*index,mirror)
            draw_cmd.append({'type':LINE_C,'info':[pts_[0][0],pts_[0][1],pts_[1][0],pts_[1][1],d,color]})
        return draw_cmd
    elif key == 'SQUARE_ROUND_THERMAL_SYMBOL':
        od,id,angle,num_spokes,gap = params[0]*symbol_factor*resize, params[1]*symbol_factor*resize\
            , float(params[2]), int(params[3]), float(params[4])
        assert mirror is False
        os = od
        dx = math.sqrt(2) * os / 2
        blank_sticker = get_blank_img(canvas)
        pts = [(x+os/2,y+os/2),(x-os/2,y+os/2),(x-os/2,y-os/2),(x+os/2,y-os/2)]
        pts_ = pts_rotate_mirror(pts,(x,y),rotate,mirror)
        draw_poly([pts_,WHITE],blank_canvas,canvas)
        draw_cirle([x,y,id/2,-1,BLACK],blank_sticker,canvas)
        for index in range(num_spokes):
            # x, y
            theta = math.radians(angle) + index*(2*math.pi/num_spokes)
            theta += rotate
            x1 = x + math.cos(theta)*dx
            y1 = y + math.sin(theta)*dx
            draw_line_c([x,y,x1,y1,gap,BLACK],blank_sticker,canvas)
        return [{'type':STICKER,'info':[blank_sticker,color]}]
    elif key == 'RECT_THERMAL_SYMBOL':
        return []
    elif key == 'RECT_THERMAL_OPEN_CORNERS_SYMBOL':
        return []
    elif key == 'ROUNDED_SQUARE_THERMAL_SYMBOL':
        return []
    elif key == 'ROUNDED_SQUARE_THERMAL_OPEN_CORNERS_SYMBOL':
        return []
    elif key == 'ROUNDED_RECT_THERMAL_SYMBOL':
        return []
    elif key == 'OVAL_THERMAL_SYMBOL':
        return []
    elif key == 'OBLONG_THERMAL_SYMBOL':
        return []
    elif key == 'HOME_PLATE_SYMBOL':
        return []
    elif key == 'INVERTED_HOME_PLATE_SYMBOL':
        return []
    elif key == 'FLAT_HOME_PLATE_SYMBOL':
        return []
    elif key == 'RADIUS_INVERTED_HOME_PLATE_SYMBOL':
        return []
    elif key == 'RADIUS_HOME_PLATE_SYMBOL':
        return []
    elif key == 'CROSS_SYMBOL':
        return []
    elif key == 'DOGBONE_SYMBOL':
        return []
    elif key == 'DPACK_SYMBOL':
        return []
    elif key == 'ECLIPSE_SYMBOL':
        return []
    elif key == 'MOIRE_SYMBOL':
        return []
    else:
        return []


def pts_rotate_mirror(pts,center,rotate,mirror):
    '''
    旋转和镜像坐标
    输入：坐标+旋转中心
    输出：处理后的坐标和中心
    '''
    x = center[0]
    y = center[1]
    if rotate == 0 and mirror == False:
        return pts
    if rotate != 0:
        pts_r = []
        for pt in pts: 
            pts_r.append(pt_rotate(pt,x,y,rotate))
    if mirror:
        pts_rm = []
        for pt in pts_r:
            pt = (-pt[0],pt[1])
            pts_rm.append(pt)
        return pts_rm
    return pts_r

def pt_rotate(pt,x,y,rotate):
    x1, y1 = pt[0], pt[1]
    if x == x1:
        assert y!=y1
        if y>y1:
            theta = 270
        else:
            theta = 90
    else:
        theta = (math.atan2(y1-y,x1-x)/math.pi * 180 + 360) % 360
    angle = math.radians(theta + rotate)
    r = math.sqrt((y-y1)*(y-y1)+(x-x1)*(x-x1))
    return (r*math.cos(angle)+x,r*math.sin(angle)+y)

