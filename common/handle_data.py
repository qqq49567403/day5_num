# handle_data.py
# 存放数据，动态设置此类的属性

from jsonpath import jsonpath


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
