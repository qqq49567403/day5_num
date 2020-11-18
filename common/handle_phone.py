# handle_phone.py
# 随机生成手机号码功能，校验数据库是否存在

from random import randint
from common.handle_db import HandleDb
from common.handle_data import Data

prefix = [133, 153, 173, 177, 180, 181, 189, 199,
          130, 131, 132, 145, 155, 156, 171, 175, 176, 185, 186,
          134, 135, 136, 137, 138, 139, 147, 150, 151, 152, 157, 158, 159, 172, 178, 182, 183, 184, 187, 188]


# 生成随机手机号码
def _get_phone():
    # 前三位
    index = randint(0, len(prefix) - 1)
    pre_three = prefix[index]
    # 后八位
    after_eight = ''
    for _ in range(8):
        new_num = str(randint(0, 9))
        after_eight += new_num
    new_phone = str(pre_three) + after_eight
    return new_phone


def get_new_phone():
    # 判断手机号码是否注册，如果已注册，重新生成手机号
    while True:
        phone = _get_phone()
        # 向数据库发送连接，查询手机号码是否存在
        hd = HandleDb()
        select_sql = f'select * from futureloan.member where mobile_phone={phone};'
        count = hd.get_count(select_sql)
        if count == 0:
            hd.close()
            setattr(Data, "phone", phone)
            return phone


