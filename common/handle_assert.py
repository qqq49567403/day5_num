# handle_assert.py
# 封装断言方法
from jsonpath import jsonpath
from decimal import Decimal

from common.handle_db import HandleDb
from common.handle_logger import logger


class HandleAssert:

    def __init__(self):
        self.sql_comp_res = None  # 存储sql语句查询之后的比较结果
        self.json_compare_res = {}  # 存储响应结果比对的结果

    # 打开数据库连接
    def init_sql_conn(self):
        self.db = HandleDb()

    def assert_result(self):
        sql_com_res_flag = True
        json_com_res_flag = True

        # json响应结果比对中，如果没有False，则全部比对通过，否则，表示比对失败
        if self.json_compare_res and False in self.json_compare_res.values():
            logger.info("sql断言失败，用例失败！请检查sql比对结果为False的！")
            sql_com_res_flag = False

        # 判断sql_com_res_flag不为空，说明有sql比对
        if self.sql_comp_res:
            # self.sql_com_res_flag为列表，说明有多条sql语句进行比对结果，则需要一个个确认是否有False
            if isinstance(self.sql_comp_res, list):
                for res in self.sql_comp_res:
                    if False in res.values():
                        sql_com_res_flag = False
            # self.sql_com_res_flag为字典，则说明有一条sql语句比对结果，只需要确认是否为False
            if isinstance(self.sql_comp_res, dict):
                if False in self.sql_comp_res.values():
                    sql_com_res_flag = False
            if sql_com_res_flag is False or json_com_res_flag is False:
                logger.info("sql语句断言失败或者json响应数据段断言失败！")
                logger.error(f"sql语句断言结果为：{sql_com_res_flag}")
                logger.error(f"json响应结果断言结果为：{json_com_res_flag}")
            else:
                logger.info("用例执行通过！")


    # 多条sql语句比较
    def get_multi_sql_compare_resp(self, check_sql_str):

        # 将期望结果的sql表达式转成python对象
        check_sql_obj = eval(check_sql_str)
        # 判断是否是列表，多个sql语句对比，一条一条进行比对
        if isinstance(check_sql_obj, list):
            # 储存每条sql的对比结果
            self.sql_comp_res = []
            for check_sql_dict in check_sql_obj:
                one_sql_comp_res = self.__get_one_compare_res(check_sql_dict)
                self.sql_comp_res.append(one_sql_comp_res)
        elif isinstance(check_sql_obj,dict):
            one_sql_comp_res = self.__get_one_compare_res(check_sql_obj)
            # 字典类型
            self.sql_comp_res = one_sql_comp_res
        else:
            self.sql_comp_res = None

    # 单条sql语句断言
    def __get_one_compare_res(self,check_sql_dict):
        one_sql_comp_res = {}
        logger.info("数据库校验开始！")

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
                        one_sql_comp_res[key] = True  # 比较成功，存储到sql_comp_res中
                        logger.info('比对成功！')
                    else:
                        one_sql_comp_res[key] = False  # 比较失败，存储到sql_comp_res中
                        logger.info("比对失败！")
                else:
                    logger.error("sql查询的结果里面，没有对应的列名：{}，请检查期望结果与语句".format(key))
                    one_sql_comp_res[key] = False
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
                one_sql_comp_res["count"] = True
            else:
                one_sql_comp_res["count"] = False
        return one_sql_comp_res

    # 响应结果断言
    def get_json_compare_res(self, expeced_exprs_str, resp_dict):
        # 转成字典
        expeced_exprs_dict = eval(expeced_exprs_str)
        # 遍历字典，通过jsonpath，从resp_dcit当中提取对应的数据，更新字典值
        for key,value in expeced_exprs_dict.items():
            logger.info("提取表达式为：{}，期望结果值为：{}".format(key, value))
            # 将jsonpath表达式的key，通过jsonpath提取后，得到对应的值
            actual_value_list = jsonpath(resp_dict, key)

            # 将提取的表达式与期望的值做等值比较，没有提取到的值为false，提取到的是list
            if isinstance(actual_value_list,list):
                if actual_value_list[0] == value:
                    self.json_compare_res[f"jsonpath-{key}-actual-{value}-expected-{actual_value_list[0]}"] = True
                else:
                    self.json_compare_res[f"jsonpath-{key}-actual-{value}-expected-{actual_value_list[0]}"] = False
                logger.info("提取的值与期望值的比对结果为：{}".format(
                    self.json_compare_res[
                        "jsonpath-{}-actual-{}-expected-{}".format(key, value, actual_value_list[0])]))
            # jsonpath如果提取到对应的值是False
            else:
                logger.error("在响应结果当中，根据jsonpath表达式：{} 没有提取到值。提取结果为False".format(key))
                self.json_compare_res["jsonpath_{}_actual_{}_expected_{}".format(key, value, actual_value_list)] = False

        logger.info("所有实际结果与预期结果的比对情况：")
        for key,value in self.json_compare_res.items():
            logger.info("{}:{}".format(key, value))

    def close_sql_conn(self):
        self.db.close()


if __name__ == '__main__':
    check_sql_str = '{"check_type":"value",' \
                    '"check_sql":"select leave_amount,mobile_phone from member where id=17",' \
                    '"expected":{"leave_amount":float(0.00)+2000,"mobile_phone":"13212072994"}}'

    ha = HandleAssert()
    ha.get_multi_sql_compare_resp(check_sql_str)
