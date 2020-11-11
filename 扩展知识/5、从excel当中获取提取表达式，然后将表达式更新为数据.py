"""
======================
Author: ss
Time: 2020-11-10
Project: 5、从excel当中获取提取表达式，然后将表达式更新为数据
Company: 软件自动化测试
======================
"""

from jsonpath import jsonpath
from common.handle_data import Data

# excel当中的数据
expr = '{"member_id":"$..id","token":"$..token"}'

resp = {'code': 0,
        'msg': 'OK',
        'data': {'id': 17,
                 'leave_amount': 607700.32,
                 'mobile_phone': '15500000000',
                 'reg_name': '蜜蜜236',
                 'reg_time': '2020-09-04 09:55:52.0',
                 'type': 0,
                 'token_info': {'token_type': 'Bearer',
                                'expires_in': '2020-11-01 21:05:44',
                                'token': 'eyJhbGciOiJIUzUxMiJ9.eyJtZW1iZXJfaWQiOjE3LCJleHAiOjE2MDQyMzU5NDR9.mD60GE-wQ8daI4-ZdzyQcuhRyuvBDX_GPN35MXFsRr9I4Ug9OMmsvXOC2QHUOKNa1FevFYZhUiwcuXXa6B_scw'}},
        'copyright': 'Copyright 柠檬班 © 2017-2020 湖南省零檬信息技术有限公司 All Rights Reserved'
        }

# token和member_id要给整个类通用
print("动态设置属性之前  的Data类：",Data.__dict__)
# 替换jsonpath表达式为实际数据
data_dict = eval(expr)
for key,value in data_dict.items():
    real_value = jsonpath(resp, value)[0]
    data_dict[key] = real_value
    setattr(Data,key,real_value)  # 给Data类，动态添加属性和value
print(data_dict)
print("动态设置属性完成之后的Data类：",Data.__dict__)
