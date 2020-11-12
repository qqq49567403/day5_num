# handle_assert.py
# 封装断言方法

from decimal import Decimal

from common.handle_db import HandleDb
from common.handle_logger import logger


class HandleAssert:

    def __init__(self):
        self.sql_comp_res = {}  # 存储sql语句查询之后的比较结果
        self.db = HandleDb()

    def assert_sql(self, check_sql_str):
        self.__get_sql_compare_res(check_sql_str)

        if False in self.sql_comp_res.values():
            logger.error("断言失败，存在数据库比对不成功！")
            raise AssertionError
        else:
            logger.info("数据库断言成功！")

    def __get_sql_compare_res(self, check_sql_str):
        check_sql_dict = eval(check_sql_str)
        logger.info("数据库校验为：\n {}".format(check_sql_dict))

        if check_sql_dict["check_type"] == "value":
            logger.info("比较sql语句查询之后的值。sql查询结果为字典，将字典当中的每一个都进行比较")
            sql_res = self.db.get_one_data(check_sql_dict["check_sql"])
            logger.info("执行sql：{}".format(check_sql_dict["check_sql"]))
            logger.info("查询结果：{}".format(sql_res))
            logger.info("期望结果：{}".format(check_sql_dict["expected"]))

            # 执行的结果进行比较  -- sql_res是字典类型，key-value键值对
            for key, value in check_sql_dict["expected"].items():
                if key in sql_res.keys():  # 实际sql查询结果里面，有期望的key
                    if isinstance(sql_res[key], Decimal):
                        sql_res[key] = float(sql_res[key])  # 将Decimal值转换成float
                        logger.info("将Decimal类型转换成float，转换后的值：{}".format(sql_res[key]))
                    if value == sql_res[key]:
                        self.sql_comp_res[key] = True  # 比较成功，存储到sql_comp_res中
                    else:
                        self.sql_comp_res[key] = False  # 比较失败，存储到sql_comp_res中
                else:
                    logger.error("sql查询的结果里面，没有对应的列名：{}，请检查期望结果与语句".format(key))
        # 对比sql语句查询之后的条数
        elif check_sql_dict["check_type"] == "count":
            logger.info("比较sql语句查询之后的条数，sql查询结果为整数，只要对比数据即可")
            # 执行sql，获取结果条数
            sql_res = self.db.get_count(check_sql_dict["check_sql"])
            logger.info("执行sql：{}".format(check_sql_dict["check_sql"]))
            logger.info("查询结果：{}".format(sql_res))
            logger.info("期望结果：{}".format(check_sql_dict["expected"]))
            # 比较
            if sql_res == check_sql_dict["expected"]["count"]:
                self.sql_comp_res["count"] = True
            else:
                self.sql_comp_res["count"] = False

    def close_sql_conn(self):
        self.db.close()


if __name__ == '__main__':
    check_sql_str = '{"check_type":"value",' \
                    '"check_sql":"select leave_amount,mobile_phone from member where id=17",' \
                    '"expected":{"leave_amount":float(0.00)+2000,"mobile_phone":"13212072994"}}'

    ha = HandleAssert()
    ha.assert_sql(check_sql_str)
