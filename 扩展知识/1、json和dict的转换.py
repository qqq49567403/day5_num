"""
======================
Author: ss
Time: 2020-11-10
Project: 1、json和dict的转换
Company: 软件自动化测试
======================
"""

import json

# json_str = '{"mobile_phone":"18600001112","pwd":"123456789","type":null,"reg_name":"美丽可爱的小简"}'
#
# json_dict = json.loads(json_str)
# # print(json_dict)
# # print(type(json_dict))
#
# json_str = json.dumps(json_dict, ensure_ascii=False)
# print(json_str)
# print(type(json_str))
# print(eval(json_str))

# json.loads是不能够计算的。
sss = '{"code":0,"msg":"OK","leave_amount":int(2500)+2000}'
# s = json.loads(sss)
s = eval(sss)
print(s)