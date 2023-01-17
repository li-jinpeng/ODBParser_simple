from global_data import *
from utils import *
from file_parser import *

class ParserWorker():
    '''
    待解析项目输管理者
    '''
    def __init__(self,odb_project,mode):
        '''
        odb_project：带解析odb++文件所在文件夹
        mode：是否初始化输出文件夹
        '''
        self.odb_project = odb_project
        self.odb_project_path = os.path.join(assetsPath,odb_project)
        self.tgz_path = self.get_tgz_path(self.odb_project_path)
        self.output_path = os.path.join(outputPath,odb_project)
        self.init_output(self.output_path,mode)
        self.info_json = os.path.join(self.output_path,'info.json')
        self.output_pictures = os.path.join(self.output_path,'pictures')
        os.system(f"tar -xzf {self.tgz_path} -C {self.odb_project_path}")
        self.odb_dir = self.tgz_path[:-4]
        self.get_files()
        self.get_info()
        logging.info(f'待解析项目“{odb_project}”初始化完毕！')
    
    def get_info(self):
        odb_info = structured_parser(self.misc_file, miscID)
        if 'UNITS' not in odb_info:
            odb_info['UNITS'] = INCH
        json.dump(odb_info,open(self.info_json,'w'),indent=4,ensure_ascii=False)
        logging.info(f'待解析项目“{self.odb_project}”的项目信息解析完毕！')
    
    def get_files(self):
        # simple版待解析文件

        # 项目基本信息
        # misc/info
        self.misc_file = os.path.join(self.odb_dir,'misc','info')

        # 项目用户自定义symbol
        # symbols/<symbol_name>/features[|.Z]
        symbols_tmp_file = [os.path.join(self.odb_dir,'symbols',symbol_name,'features') for symbol_name in os.listdir(os.path.join(self.odb_dir,'symbols'))]
        self.symbols_file = []
        for symbol_file in symbols_tmp_file:
            if os.path.exists(symbol_file):
                self.symbols_file.append(symbol_file)
            else:
                self.symbols_file.append(f'{symbol_file}.Z')

        # 项目字体
        # fonts/[.*]
        self.fonts_file = [os.path.join(self.odb_dir,'fonts',font_name) for font_name in os.listdir(os.path.join(self.odb_dir,'fonts'))]

        # edit步绘图区域
        # steps/edit/profile
        self.edit_profile = os.path.join(self.odb_dir,'steps','edit','profile')

        # 顶层
        # steps/edit/layers/gtl/features[|.Z]
        self.edit_gtl = self.build_edit_layer_file('gtl')
        # 顶层阻焊层
        # steps/edit/layers/gts/features[|.Z]
        self.edit_gts = self.build_edit_layer_file('gts')
        # 顶层丝印层
        # steps/edit/layers/gto/features[|.Z]
        self.edit_gto = self.build_edit_layer_file('gto')
        # 底层
        # steps/edit/layers/gbl/features[|.Z]
        self.edit_gbl = self.build_edit_layer_file('gbl')
        # 底层阻焊层
        # steps/edit/layers/gbs/features[|.Z]
        self.edit_gbs = self.build_edit_layer_file('gbs')
        # 底层丝印层
        # steps/edit/layers/gbo/features[|.Z]
        self.edit_gbo = self.build_edit_layer_file('gbo')
        # 钻孔层
        # steps/edit/layers/ad1/features[|.Z]
        self.edit_ad1 = self.build_edit_layer_file('ad1')
        # 禁止布线区
        # steps/edit/layers/gko/features[|.Z]
        self.edit_gko = self.build_edit_layer_file('gko')

    def build_edit_layer_file(self,layer_name):
        layer_path = os.path.join(self.odb_dir,'steps','edit','layers',layer_name,'features')
        if os.path.exists(layer_path):
            return layer_path
        return f'{layer_path}.Z'

    def get_tgz_path(self,odb_project_path):
        files = os.listdir(odb_project_path)
        for file in files:
            if '.tgz' in file:
                return os.path.join(odb_project_path,file)
        logging.error(f'{odb_project_path}中未发现ODB++文件！')
        return Error
    
    def init_output(self,output_path,mode):
        if mode:
            if os.path.exists(output_path):
                self.delete_output(output_path)
        if os.path.exists(output_path):
            logging.info(f'输出文件夹{output_path}已存在。')
            return Success
        os.mkdir(output_path)
        os.mkdir(os.path.join(output_path,'pictures'))
        file = open(os.path.join(output_path,'info.json'),'w')
        file.close()

    def delete_output(self,output_path):
        shutil.rmtree(output_path)
        logging.info(f'输出文件夹{output_path}已被移除。')

