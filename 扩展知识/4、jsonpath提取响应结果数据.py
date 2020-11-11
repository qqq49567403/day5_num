"""
======================
Author: 柠檬班-小简
Time: 2020/11/1 21:35
Project: day8
Company: 湖南零檬信息技术有限公司
======================
"""
from jsonpath import jsonpath

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

member_id = jsonpath(resp,"$..id")[0]
print(member_id)

token = jsonpath(resp,"$..token")[0]
print(token)