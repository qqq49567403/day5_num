# handle_db.py
# 连接数据库，提供数量统计、查询一条数据、查询所有数据、断开连接

import pymysql
from common.handle_conf import conf


class HandleDb:
    # 实例化连接
    def __init__(self):
        try:
            self.conn = pymysql.connect(host=conf.get('mysql', 'host'),
                                        user=conf.get('mysql', 'user'),
                                        password=conf.get('mysql', 'password'),
                                        database=conf.get('mysql', 'db'),
                                        port=conf.getint('mysql', 'port'),
                                        charset='utf8',
                                        cursorclass=pymysql.cursors.DictCursor)

            # 建立游标
            self.cur = self.conn.cursor()

        except:
            print("连接数据库失败！")
            raise

    # 获取查询的结果个数
    def get_count(self, sql, args=None):
        self.conn.commit()
        return self.cur.execute(sql, args)

    # 获取查询的一条数据
    def get_one_data(self, sql, args=None):
        self.conn.commit()
        self.cur.execute(sql, args)
        return self.cur.fetchone()

    # 查询获取所有数据
    def get_all_data(self, sql, args=None):
        self.conn.commit()
        self.cur.execute(sql, args)
        return self.cur.fetchall()

    # 关闭数据库连接
    def close(self):
        self.cur.close()
        self.conn.close()

if __name__ == '__main__':
    ss = HandleDb()
    count = ss.get_count('select * from futureloan.member where mobile_phone=17250364252;')
    print(count)
    ss.close()

