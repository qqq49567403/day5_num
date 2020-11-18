"""
======================
Author: ss
Time: 2020-11-11
Project: test_add_bid_api
Company: 软件自动化测试
======================
"""

import os
import unittest

from common.myddt import ddt, data
from common.handle_excel import HandleExcel
from common.handle_path import testdata_dir
from common.handle_requests import HandleRequests
from common.handle_replace import relace_case_with_re_v2
from common.handle_data import set_dataclass_attr_from_resp, Data
from common.handle_assert import HandleAssert

excel_path = os.path.join(testdata_dir, "api_cases.xlsx")
he = HandleExcel(excel_path, "加标")
cases = he.get_all_data()



@ddt
class TestAddBid(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.hr = HandleRequests()
        cls.hassert = HandleAssert()  # 连接数据库进行查询

    @classmethod
    def tearDownClass(cls) -> None:
        cls.hassert.close_sql_conn()  # 关闭数据库连接

    @data(*cases)
    def test_recharge(self, case):
        # 替换
        case = relace_case_with_re_v2(case)

        # 判断是否需要传递token值
        if hasattr(Data, "token"):
            resp = self.hr.send_request(case["method"], case["url"], case["request_data"], token=getattr(Data, "token"))
        else:
            resp = self.hr.send_request(case["method"], case["url"], case["request_data"])
        resp = resp.json()

        # 如果有提取字段，那么需要从响应结果当中，提取对应的数据，要设置为Data.token
        if case["extract"]:
            set_dataclass_attr_from_resp(resp, case["extract"])

            # 如果有期望结果，则要对比实际结果与期望结果
        if case["expected"]:
            self.hassert.get_json_compare_res(case["expected"], resp)

        # 判断是否需要做数据库校验
        if case["check_sql"]:
            self.hassert.init_sql_conn()
            self.hassert.get_multi_sql_compare_resp(case["check_sql"])
            self.hassert.close_sql_conn()


