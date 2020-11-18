"""
======================
Author: ss
Time: 2020-11-17
Project: handle_yaml
Company: 软件自动化测试
======================
"""

# 封装提取yaml数据


import yaml
import os

from common.handle_path import conf_dir

class HandleYaml:

    def __init__(self,filename):
        filepath = os.path.join(conf_dir,filename)
        with open(filepath,encoding="utf-8") as fs:
            self.data = yaml.load(fs,yaml.FullLoader)



