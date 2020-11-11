# handle_conf.py
# 读取配置文件

from configparser import ConfigParser
from common.handle_path import conf_dir


class HandleConf(ConfigParser):

    def __init__(self, filename):
        super().__init__()  # 继承父类的初始化方法
        self.read(filename, encoding="utf-8")  # 读取配置文件，格式设置为utf-8


conf = HandleConf(conf_dir)  # 设置调用日志读取的类对象
