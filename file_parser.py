from global_data import *
from utils import *

def line_record_parser(file_path):
    '''
    surface or feature
    line or text or pad or poly or arc or bar
    '''
    with open(file_path, 'rb') as f:
            file_bytes = f.read()
            if file_path[-2:] == '.Z':
                file_bytes = unlzw.unlzw(file_bytes)
    lines = file_bytes.decode("utf-8").split('\n')

    cmd_list = []

    surface_lines = []
    feature_symbol_dict = {}
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            continue  # skip empty lines
        if line[0] == '#':
            continue  # skip comment lines
        if line[0] == '$':
            idx, feature_symbol_str = line.split(' ')
            idx = int(idx[1:])
            feature_symbol_dict[idx] = feature_symbol_str
        elif line[0] == '@':
            pass
        elif line[0] == '&':
            pass
        elif line[0] == 'L':
            cmd_list.append({'type':'line','info':line})
        elif line[0] == 'P':
            cmd_list.append({'type':'pad','info':line})
        elif line[0] == 'A':
            cmd_list.append({'type':'arc','info':line})
        elif line[0] == 'T':
            cmd_list.append({'type':'text','info':line})
        elif line[0] == 'B':
            cmd_list.append({'type':'bar','info':line})
        elif line[:2] == 'S ':
            assert len(surface_lines) == 0
            surface_lines.append(line)
        elif line[0] == 'O':
            surface_lines.append(line)
        elif line[:2] == 'SE':
            surface_lines.append(line)
            cmd_list.append({'type':'poly','info':surface_lines})
            surface_lines = []
    
    return cmd_list,feature_symbol_dict

def structured_parser(file_path,file_id):
    file = open(file_path,'r')
    if file_id == miscID:
        info = {}
        for line in file.read().split('\n'):
            if line:
                info[line.split('=')[0]] = line.split('=')[1]
        return info
    else:
        raise NotImplementedError()

