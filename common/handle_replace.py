"""
======================
Author: ss
Time: 2020-11-11
Project: handle_replace
Company: 软件自动化测试
======================
"""

import re

from common.handle_logger import logger
from common.handle_data import Data
from common.handle_phone import get_new_phone


def relace_case_with_re_v2(case_dict):
    case_str = str(case_dict)
    # 正则提取
    data_mark_list = re.findall("#(\w+)#", case_str)

    # 若有phone字段，则先生成一个新的手机号码，并设置到Data类的phone属性
    if "phone" in data_mark_list:
        logger.info("有phone字段，需要先生成一个新的手机号码，并设置到Data类的phone属性")
        get_new_phone()

    if data_mark_list:  # 列表不为空
        for mark in data_mark_list:  # 遍历列表里的值
            case_str = case_str.replace(f"#{mark}#", getattr(Data, mark))
            logger.info(f"替换mark：#{mark}#，替换后的mark值为：{getattr(Data, mark)}")
    logger.info(f"替换完成之后的用例数据为：\n {case_str}")
    return eval(case_str)
