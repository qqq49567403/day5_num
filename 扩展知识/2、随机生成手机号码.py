"""
======================
Author: ss
Time: 2020-11-10
Project: 2、随机生成手机号码
Company: 软件自动化测试
======================
"""

from random import randint

prefix = [133, 149, 153, 173, 177, 180, 181, 189, 199,
          130, 131, 132, 145, 155, 156, 166, 171, 175, 176, 185, 186, 166,
          134, 135, 136, 137, 138, 139, 147, 150, 151, 152, 157, 158, 159, 172, 178, 182, 183, 184, 187, 188]


def __gen_phone():
    # 前三位
    index = randint(0,len(prefix)-1)
    three_phone = prefix[index]
    # 后八位
    eight_phone = ""
    for _ in range(8):
        num = randint(0, 9)
        eight_phone += str(num)
    new_phone = str(three_phone) + eight_phone
    return new_phone

a = __gen_phone()
print(a)

