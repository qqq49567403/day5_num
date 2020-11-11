# handle_data.py
# 存放数据，动态设置此类的属性

from jsonpath import jsonpath
import re


class Data:
    pass


def set_dataclass_attr_from_resp(resp, extract):
    """"
    resp:请求的响应结果的字典类型
    extract:从excel当中读取的，要从响应结果当中提取的key-value，字符串类型
    """
    # 将字符串转换成字典类型
    data_dict = eval(extract)
    # 遍历key，value。将每一个jsonpath的表达式，替换成对应的数据
    for key, value in data_dict.items():
        # 将每一个jsonpath的表达式，替换成对应的数据
        real_value = jsonpath(resp, value)
        if real_value:
            # 给Date类，动态添加属性和value
            setattr(Data, key, str(real_value[0]))


def relace_case_with_re(case_dict):
    """
    :param case_dict: 从excel当中读取出来的用例数据。字典类型
    :return: 全部替换完成之后的case
    """
    # case是从excel当中读取出来的用例-字典，包含了exce当中的多个key
    for key, value in case_dict.items():
        if isinstance(value, str):
            # 正则提取
            res = re.findall("#(\w+)#", value)  # 列表
            if res:  # 列表不为空
                for item in res:  # 遍历列表里的值
                    print(item)
                    # 从Data类中，添加对应的数据去替换
                    value = value.replace(f"#{item}#", getattr(Data, item))  # 更新value
                    print(value)
                case_dict[key] = value
    return case_dict


def relace_case_with_re_v2(case_dict):
    """
    :param case_dict: 从excel当中读取出来的用例数据。字典类型
    :return: 全部替换完成之后的case
    """
    case_str = str(case_dict)
    # 正则提取
    res = re.findall("#(\w+)#", value)  # 列表
    if res:  # 列表不为空
        for item in res:  # 遍历列表里的值
            print(item)
            # 从Data类中，添加对应的数据去替换
            value = value.replace(f"#{item}#", getattr(Data, item))  # 更新value
            print(value)
    return eval(case_str)
