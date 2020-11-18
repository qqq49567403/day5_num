# handle_logger.py
# 封装日志输出功能

import logging
import os
from common.handle_conf import conf
from common.handle_path import log_dir


class HandleLogger(logging.Logger):
    def __init__(self):
        super().__init__(conf.get('log', 'name'))
        self.setLevel(conf.get('log', 'level'))

        # 设置日志输出格式
        fmt = "%(asctime)s %(name)s %(levelname)s %(filename)s [第%(lineno)d行] %(message)s"
        formatter = logging.Formatter(fmt)

        # 设置日志输出格式-控制台
        handle1 = logging.StreamHandler()
        handle1.setFormatter(formatter)

        # 设置日志输出格式-文件
        log_path = os.path.join(log_dir, conf.get('log', 'file'))
        handle2 = logging.FileHandler(log_path, encoding="utf-8")
        handle2.setFormatter(formatter)

        # 添加渠道到日志收集器中
        self.addHandler(handle1)
        self.addHandler(handle2)


logger = HandleLogger()
logger.info("hello world!")
