"""
======================
Author: ss
Time: 2020-11-10
Project: 3、mysql数据库操作
Company: 软件自动化测试
======================
"""

import pymysql

# 1、建立连接
conn = pymysql.connect(host="api.lemonban.com",
                       user="future",
                       password="123456",
                       database="futureloan",
                       port=3306,
                       charset="utf8",
                       cursorclass=pymysql.cursors.DictCursor)

# 2、建立游标
cur = conn.cursor()

# 3、执行sql语句--查
# new_phone = {"phone":18557519118}
# sql = "select * from futureloan.member where mobile_phone=%(phone)s;"
# res = cur.execute(sql,new_phone)
# print(res)

sql = "SELECT * from futureloan.member LIMIT 10;"
cur.execute(sql)

# 4、获取查询结果
data = cur.fetchone()  # 获取一行数据
print(data)
data = cur.fetchall()  # 获取所有数据
print(data)
data = cur.fetchmany(3)
print(data)

# 5、释放数据库连接
cur.close()
conn.close()