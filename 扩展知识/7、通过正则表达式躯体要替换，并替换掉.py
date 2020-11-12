"""
======================
Author: ss
Time: 2020-11-11
Project: 7、通过正则表达式躯体要替换，并替换掉
Company: 软件自动化测试
======================
"""

import re


class Data:
    pass


setattr(Data, "member_id", "17")
setattr(Data, "money", str(2000))

case = {"method": "post",
        "request_data": '{"member_id":"#member_id#","amount":2000,"leave_amount":#money#}',
        "expected": '{"code":0,"msg":"OK","leave_amount":float(#money#)+2000}'}

for key,value in case.items():
    res = re.findall("#(\w+)#",value)
    if res:
        for item in res:
            value = value.replace(f"#{item}#", getattr(Data,item))
            print(value)
        case[key] = value

for key,value in case.items():
    print(key,value)