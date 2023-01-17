from utils import *
from global_data import *

from collections import OrderedDict

# r<d>
ROUND_SYMBOL_PATTERN = re.compile(r'r(\d+\.?\d*)')
# s<s>
SQUARE_SYMBOL_PATTERN = re.compile(r's(\d+\.?\d*)')
# rect<w>x<h>
RECT_SYMBOL_PATTERN = re.compile(r'rect(\d+\.?\d*)x(\d+\.?\d*)')
# rect<w>x<h>xr<rad>x<corners>
ROUNDED_RECT_SYMBOL_PATTERN = re.compile(
    r'rect(\d+\.?\d*)x(\d+\.?\d*)xr(\d+\.?\d*)(?:x(\d+))?')
# rect<w>x<h>xc<rad>x<corners>
CHAMFERED_RECT_SYMBOL_PATTERN = re.compile(
    r'rect(\d+\.?\d*)x(\d+\.?\d*)xc(\d+\.?\d*)(?:x(\d+))?')
# oval<w>x<h>
OVAL_SYMBOL_PATTERN = re.compile(r'oval(\d+\.?\d*)x(\d+\.?\d*)')
# di<w>x<h>
DIAMOND_SYMBOL_PATTERN = re.compile(r'di(\d+\.?\d*)x(\d+\.?\d*)')
# oct<w>x<h>x<r>
OCTAGON_SYMBOL_PATTERN = re.compile(r'oct(\d+\.?\d*)x(\d+\.?\d*)x(\d+\.?\d*)')
# donut_r<od>x<id>
ROUND_DONUT_SYMBOL_PATTERN = re.compile(r'donut_r(\d+\.?\d*)x(\d+\.?\d*)')
# donut_s<od>x<id>
SQUARE_DONUT_SYMBOL_PATTERN = re.compile(r'donut_s(\d+\.?\d*)x(\d+\.?\d*)')
# donut_sr<od>x<id>
SQUARE_ROUND_DONUT_SYMBOL_PATTERN = re.compile(r'donut_sr(\d+\.?\d*)x(\d+\.?\d*)')
# donut_s<od>x<id>xr<rad>x<corners>
ROUNDED_SQUARE_DONUT_SYMBOL_PATTERN = re.compile(r'donut_s(\d+\.?\d*)x(\d+\.?\d*)xr(\d+\.?\d*)(?:x(\d+))?')
# donut_rc<ow>x<oh>x<lw>
RECT_DONUT_SYMBOL_PATTERN = re.compile(r'donut_rc(\d+\.?\d*)x(\d+\.?\d*)x(\d+\.?\d*)')
# donut_rc<ow>x<oh>x<lw>xr<rad >x<corners>
ROUNDED_RECT_DONUT_SYMBOL_PATTERN = re.compile(r'donut_rc(\d+\.?\d*)x(\d+\.?\d*)x(\d+\.?\d*)xr(\d+\.?\d*)(?:x(\d+))?')
# donut_o<ow>x<oh>x<lw>
OVAL_DONUT_SYMBOL_PATTERN = re.compile(r'donut_o(\d+\.?\d*)x(\d+\.?\d*)x(\d+\.?\d*)')
# hex_l<w>x<h>x<r>
HORIZONTAL_HEXAGON_SYMBOL_PATTERN = re.compile(r'hex_l(\d+\.?\d*)x(\d+\.?\d*)x(\d+\.?\d*)')
# hex_s<w>x<h>x<r>
VERTICAL_HEXAGON_SYMBOL_PATTERN = re.compile(r'hex_s(\d+\.?\d*)x(\d+\.?\d*)x(\d+\.?\d*)')
# bfr<d>
BUTTERFLY_SYMBOL_PATTERN = re.compile(r'bfr(\d+\.?\d*)')
# bfs<s>
SQUARE_BUTTERFLY_SYMBOL_PATTERN = re.compile(r'bfs(\d+\.?\d*)')
# tri<base>x<h>
TRIANGLE_SYMBOL_PATTERN = re.compile(r'tri(\d+\.?\d*)x(\d+\.?\d*)')
# oval_h<w>x<h>
HALF_OVAL_SYMBOL_PATTERN = re.compile(r'oval_h(\d+\.?\d*)x(\d+\.?\d*)')
# thr<od>x<id>x<angle>x<num_spokes>x<gap>
ROUNDED_ROUND_THERMAL_SYMBOL_PATTERN = re.compile(
    r'thr(\d+\.?\d*)x(\d+\.?\d*)x(\d+\.?\d*)x(\d+)x(\d+\.?\d*)')
# ths<od>x<id>x<angle>x<num_spokes>x<gap>
SQAURED_ROUND_THERMAL_SYMBOL_PATTERN = re.compile(
    r'ths(\d+\.?\d*)x(\d+\.?\d*)x(\d+\.?\d*)x(\d+)x(\d+\.?\d*)')
# s_ths<os>x<is>x<angle>x<num_spokes>x<gap>
SQUARE_THERMAL_SYMBOL_PATTERN = re.compile(
    r's_ths(\d+\.?\d*)x(\d+\.?\d*)x(\d+\.?\d*)x(\d+)x(\d+\.?\d*)')
# s_tho<od>x<id>x<angle>x<num_spokes>x<gap>
SQUARE_THERMAL_OPEN_CORNERS_SYMBOL_PATTERN = re.compile(
    r's_tho(\d+\.?\d*)x(\d+\.?\d*)x(\d+\.?\d*)x(\d+)x(\d+\.?\d*)')
# s_thr<os>x<is>x<angle>x<num_spokes>x<gap>
LINE_THERMAL_SYMBOL_PATTERN = re.compile(
    r's_thr(\d+\.?\d*)x(\d+\.?\d*)x(\d+\.?\d*)x(\d+)x(\d+\.?\d*)')
# sr_ths<os>x<id>x<angle>x<num_spokes>x<gap>
SQUARE_ROUND_THERMAL_SYMBOL_PATTERN = re.compile(
    r'sr_ths(\d+\.?\d*)x(\d+\.?\d*)x(\d+\.?\d*)x(\d+)x(\d+\.?\d*)')
# rc_ths<w>x<h>x<angle>x<num_spokes>x<gap>x<air_gap>
RECT_THERMAL_SYMBOL_PATTERN = re.compile(
    r'rc_ths(\d+\.?\d*)x(\d+\.?\d*)x(\d+\.?\d*)x(\d+)x(\d+\.?\d*)x(\d+\.?\d*)')
# rc_tho<w>x<h>x<angle>x<num_spokes>x<gap>x<air_gap>
RECT_THERMAL_OPEN_CORNERS_SYMBOL_PATTERN = re.compile(
    r'rc_tho(\d+\.?\d*)x(\d+\.?\d*)x(\d+\.?\d*)x(\d+)x(\d+\.?\d*)x(\d+\.?\d*)')
# s_ths<os>x<is>x<angle>x<num_spokes>x<gap>xr<rad>x<corners>
ROUNDED_SQUARE_THERMAL_SYMBOL_PATTERN = re.compile(
    r's_ths(\d+\.?\d*)x(\d+\.?\d*)x(\d+\.?\d*)x(\d+)x(\d+\.?\d*)xr(\d+\.?\d*)x(\d+\.?\d*)')
# s_ths<os>x<is>x<angle>x<num_spokes>x<gap>xr<rad>x<corners>
ROUNDED_SQUARE_THERMAL_OPEN_CORNERS_SYMBOL_PATTERN = re.compile(
    r's_ths(\d+\.?\d*)x(\d+\.?\d*)x(\d+\.?\d*)x(\d+)x(\d+\.?\d*)xr(\d+\.?\d*)x(\d+\.?\d*)')
# rc_ths<ow>x<oh>x<angle>x<num_spokes>x<gap>x<lw>xr<rad>x<corners>
ROUNDED_RECT_THERMAL_SYMBOL_PATTERN = re.compile(
    r'rc_ths(\d+\.?\d*)x(\d+\.?\d*)x(\d+\.?\d*)x(\d+)x(\d+\.?\d*)x(\d+\.?\d*)xr(\d+\.?\d*)x(\d+\.?\d*)')
# o_ths<ow>x<oh>x<angle>x<num_spokes>x<gap>x<lw>
OVAL_THERMAL_SYMBOL_PATTERN = re.compile(
    r'o_ths(\d+\.?\d*)x(\d+\.?\d*)x(\d+\.?\d*)x(\d+)x(\d+\.?\d*)x(\d+\.?\d*)')
# oblong_ths<ow>x<oh>x<angle>x<num_spokes>x<gap>x<lw>x<r|s>
OBLONG_THERMAL_SYMBOL_PATTERN = re.compile(
    r'oblong_ths(\d+\.?\d*)x(\d+\.?\d*)x(\d+\.?\d*)x(\d+)x(\d+\.?\d*)x(\d+\.?\d*)x([rs])')
# hplate<w>x<h>x<c>x<ra>x<ro> | hplate<w>x<h>x<c>
HOME_PLATE_SYMBOL_PATTERN = re.compile(
    r'hplate(\d+\.?\d*)x(\d+\.?\d*)x(\d+\.?\d*)(?:x(\d+\.?\d*)x(\d+\.?\d*))?')
# rhplate<w>x<h>x<c>x<ra>x<ro> | rhplate<w>x<h>x<c>
INVERTED_HOME_PLATE_SYMBOL_PATTERN = re.compile(
    r'rhplate(\d+\.?\d*)x(\d+\.?\d*)x(\d+\.?\d*)(?:x(\d+\.?\d*)x(\d+\.?\d*))?')
# fhplate<w>x<h>x<vc>x<hc>x<ra>x<ro> | fhplate<w>x<h>x<vc>x<hc>
FLAT_HOME_PLATE_SYMBOL_PATTERN = re.compile(
    r'fhplate(\d+\.?\d*)x(\d+\.?\d*)x(\d+\.?\d*)x(\d+\.?\d*)(?:x(\d+\.?\d*)x(\d+\.?\d*))?')
# radhplate<w>x<h>x<ms>x<ra> | radhplate<w>x<h>x<ms>
RADIUS_INVERTED_HOME_PLATE_SYMBOL_PATTERN = re.compile(
    r'radhplate(\d+\.?\d*)x(\d+\.?\d*)x(\d+\.?\d*)(?:x(\d+\.?\d*))?'
)
# dshape<w>x<h>x<r>x<ra> | dshape<w>x<h>x<r>
RADIUS_HOME_PLATE_SYMBOL_PATTERN = re.compile(
    r'dshape(\d+\.?\d*)x(\d+\.?\d*)x(\d+\.?\d*)(?:x(\d+\.?\d*))?'
)
# cross<w>x<h>x<hs>x<vs>x<hc>x<vc>x[r|s]<ra> | cross<w>x<h>x<hs>x<vs>x<hc>x<vc>x[r|s]
CROSS_SYMBOL_PATTERN = re.compile(
    r'cross(\d+\.?\d*)x(\d+\.?\d*)x(\d+\.?\d*)x(\d+\.?\d*)x(\d+\.?\d*)x(\d+\.?\d*)x([rs])(\d+\.?\d*)?'
)
# dogbone<w>x<h>x<hs>x<vs>x<hc>x[r|s]x<ra> | dogbone<w>x<h>x<hs>x<vs>x<hc>x[r|s]
DOGBONE_SYMBOL_PATTERN = re.compile(
    r'dogbone(\d+\.?\d*)x(\d+\.?\d*)x(\d+\.?\d*)x(\d+\.?\d*)x(\d+\.?\d*)x([rs])(?:x(\d+\.?\d*))?'
)
# dpack<w>x<h>x<hg>x<vg>x<hn>x<vn>x<ra> | dpack<w>x<h>x<hg>x<vg>x<hn>x<vn>
DPACK_SYMBOL_PATTERN = re.compile(
    r'dpack(\d+\.?\d*)x(\d+\.?\d*)x(\d+\.?\d*)x(\d+\.?\d*)x(\d+\.?\d*)x(\d+\.?\d*)(?:x(\d+\.?\d*))?'
)
# el<w>x<h>
ECLIPSE_SYMBOL_PATTERN = re.compile(r'el(\d+\.?\d*)x(\d+\.?\d*)')
# moire<rw>x<rg>x<nr>x<lw>x<ll>x<la>
MOIRE_SYMBOL_PATTERN = re.compile(r'moire(\d+\.?\d*)x(\d+\.?\d*)x(\d+\.?\d*)x(\d+\.?\d*)x(\d+\.?\d*)x(\d+\.?\d*)')

# 不画
# hole<d>x<p>x<tp>x<tm>
HOLE_SYMBOL_PATTERN = re.compile(r'hole(\d+\.?\d*)x(\d+\.?\d*)x(\d+\.?\d*)x(\d+\.?\d*)')
# ext
NONE_GRAPHIC_SYMBOL_PATTERN = re.compile(r'ext')
# ## end symbols

RECOGNIZE_PATTERN_DICT = OrderedDict(ROUND_SYMBOL=ROUND_SYMBOL_PATTERN,
                                     SQUARE_SYMBOL=SQUARE_SYMBOL_PATTERN,
                                        
                                     ROUNDED_RECT_SYMBOL=ROUNDED_RECT_SYMBOL_PATTERN,
                                     CHAMFERED_RECT_SYMBOL=CHAMFERED_RECT_SYMBOL_PATTERN,

                                     RECT_SYMBOL=RECT_SYMBOL_PATTERN,
                                     
                                     OVAL_SYMBOL=OVAL_SYMBOL_PATTERN,
                                     DIAMOND_SYMBOL=DIAMOND_SYMBOL_PATTERN,
                                     OCTAGON_SYMBOL=OCTAGON_SYMBOL_PATTERN,
                                     ROUND_DONUT_SYMBOL=ROUND_DONUT_SYMBOL_PATTERN,
                                     SQUARE_DONUT_SYMBOL=SQUARE_DONUT_SYMBOL_PATTERN,
                                     SQUARE_ROUND_DONUT_SYMBOL=SQUARE_ROUND_DONUT_SYMBOL_PATTERN,
                                     ROUNDED_SQUARE_DONUT_SYMBOL=ROUNDED_SQUARE_DONUT_SYMBOL_PATTERN,
                                     RECT_DONUT_SYMBOL=RECT_DONUT_SYMBOL_PATTERN,
                                     ROUNDED_RECT_DONUT_SYMBOL=ROUNDED_RECT_DONUT_SYMBOL_PATTERN,
                                     OVAL_DONUT_SYMBOL=OVAL_DONUT_SYMBOL_PATTERN,
                                     HORIZONTAL_HEXAGON_SYMBOL=HORIZONTAL_HEXAGON_SYMBOL_PATTERN,
                                     VERTICAL_HEXAGON_SYMBOL=VERTICAL_HEXAGON_SYMBOL_PATTERN,
                                     BUTTERFLY_SYMBOL=BUTTERFLY_SYMBOL_PATTERN,
                                     SQUARE_BUTTERFLY_SYMBOL=SQUARE_BUTTERFLY_SYMBOL_PATTERN,
                                     TRIANGLE_SYMBOL=TRIANGLE_SYMBOL_PATTERN,
                                     HALF_OVAL_SYMBOL = HALF_OVAL_SYMBOL_PATTERN,
                                     ROUNDED_ROUND_THERMAL_SYMBOL=ROUNDED_ROUND_THERMAL_SYMBOL_PATTERN,
                                     SQAURED_ROUND_THERMAL_SYMBOL=SQAURED_ROUND_THERMAL_SYMBOL_PATTERN,
                                     SQUARE_THERMAL_SYMBOL = SQUARE_THERMAL_SYMBOL_PATTERN,
                                     SQUARE_THERMAL_OPEN_CORNERS_SYMBOL = SQUARE_THERMAL_OPEN_CORNERS_SYMBOL_PATTERN,
                                     LINE_THERMAL_SYMBOL = LINE_THERMAL_SYMBOL_PATTERN,
                                     SQUARE_ROUND_THERMAL_SYMBOL = SQUARE_ROUND_THERMAL_SYMBOL_PATTERN,
                                     RECT_THERMAL_SYMBOL = RECT_THERMAL_SYMBOL_PATTERN,
                                     RECT_THERMAL_OPEN_CORNERS_SYMBOL = RECT_THERMAL_OPEN_CORNERS_SYMBOL_PATTERN,   
                                     ROUNDED_SQUARE_THERMAL_SYMBOL = ROUNDED_SQUARE_THERMAL_SYMBOL_PATTERN,
                                     ROUNDED_SQUARE_THERMAL_OPEN_CORNERS_SYMBOL = ROUNDED_SQUARE_THERMAL_OPEN_CORNERS_SYMBOL_PATTERN,
                                     ROUNDED_RECT_THERMAL_SYMBOL = ROUNDED_RECT_THERMAL_SYMBOL_PATTERN,
                                     OVAL_THERMAL_SYMBOL = OVAL_THERMAL_SYMBOL_PATTERN,
                                     OBLONG_THERMAL_SYMBOL = OBLONG_THERMAL_SYMBOL_PATTERN,
                                     HOME_PLATE_SYMBOL =HOME_PLATE_SYMBOL_PATTERN,
                                     INVERTED_HOME_PLATE_SYMBOL = INVERTED_HOME_PLATE_SYMBOL_PATTERN,
                                     FLAT_HOME_PLATE_SYMBOL = FLAT_HOME_PLATE_SYMBOL_PATTERN,
                                     RADIUS_INVERTED_HOME_PLATE_SYMBOL = RADIUS_INVERTED_HOME_PLATE_SYMBOL_PATTERN,
                                     RADIUS_HOME_PLATE_SYMBOL = RADIUS_HOME_PLATE_SYMBOL_PATTERN,
                                     CROSS_SYMBOL = CROSS_SYMBOL_PATTERN,
                                     DOGBONE_SYMBOL = DOGBONE_SYMBOL_PATTERN,
                                     DPACK_SYMBOL = DPACK_SYMBOL_PATTERN,
                                     ECLIPSE_SYMBOL = ECLIPSE_SYMBOL_PATTERN,
                                     MOIRE_SYMBOL=MOIRE_SYMBOL_PATTERN,
                                     HOLE_SYMBOL = HOLE_SYMBOL_PATTERN,
                                     NONE_GRAPHIC_SYMBOL = NONE_GRAPHIC_SYMBOL_PATTERN
                                     )

def symbol_parse(symbol_str):
    for key in RECOGNIZE_PATTERN_DICT:
        match = RECOGNIZE_PATTERN_DICT[key].match(symbol_str)
        if match:
            return key, match.groups()
    else:
        return 'USER_DEFINED', symbol_str


