"""
======================
Author: 柠檬班-小简
Time: 2020/11/6 15:35
Project: day11-2
Company: 湖南零檬信息技术有限公司
======================
"""
import re

from common.handle_phone import get_new_phone
from common.handle_data import Data
from common.handle_logger import logger
from common.handle_yaml import HandleYaml


def relace_case_with_re_v2(case_dict):
    """
    1、遍历case每一个key-value。如果value当中匹配到了"#(\w+)#"，提取出来。
    2、将Data类当中，对应的数据替换到value当中。
    3、全部替换完成之后，给case[key]重新赋值。
    :param case: 从excel当中读取出来的一个用例数据。字典类型。
    :return: case。全部替换完成之后的case
    """
    # 实例化HandleYaml类，读取data.yaml中的数据
    global_data = HandleYaml("data.yaml").data

    case_str = str(case_dict)
    # 正则提取
    data_mark_list = re.findall("#(\w+)#", case_str)  # 列表
    logger.info("从测试用例中，正则提取之后的结果：{}".format(data_mark_list))
    # 若有phone字段，则先生成一个未注册的手机号码，并设置为Data类的phone属性
    if "phone" in data_mark_list:
        logger.info("有phone字段，需要生成一个新的尚未注册的手机号，并设置到Data类的phone属性")
        get_new_phone()
    if data_mark_list:  # 列表不为空
        for mark in data_mark_list:  # 遍历列表里的值
            # mark可能在数据配置文件data.yaml当中，也有可能在Data当中。
            if mark in global_data.keys():
                case_str = case_str.replace(f"#{mark}#", str(global_data[mark]))
                logger.info(f"从data.yaml中取数据，替换mark: #{mark}#，替换后mark值为：{global_data[mark]}")
            else:
                # 从Data类当中，用对应的数据，去替换。
                case_str = case_str.replace(f"#{mark}#", getattr(Data, mark))
                logger.info(f"从Data类中取数据，替换mark: #{mark}#，替换后mark值为：{getattr(Data, mark)}")
    logger.info(f"替换完成之后的用例数据(字符串类型)为：\n {case_str}")
    return eval(case_str)




