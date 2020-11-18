"""
======================
Author: ss
Time: 2020-11-12
Project: test_business_flow
Company: 软件自动化测试
======================
"""
# 业务流程

import os
import unittest

from common.handle_path import testdata_dir
from common.handle_replace import relace_case_with_re_v2
from common.handle_requests import HandleRequests
from common.handle_assert import HandleAssert
from common.handle_data import set_dataclass_attr_from_resp, Data
from common.handle_excel import HandleExcel
from common.myddt import ddt, data

excel_path = os.path.join(testdata_dir, "api_cases.xlsx")
he = HandleExcel(excel_path, "业务流")
cases = he.get_all_data()

@ddt
class TestBusinessFlow(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.hr = HandleRequests()  # 实例化HandleRequests类
        cls.ha = HandleAssert()  # 连接数据库

    @classmethod
    def tearDownClass(cls) -> None:
        cls.ha.close_sql_conn()  # 关闭数据库连接

    @data(*cases)
    def test_business_flow(self, case):
        # 替换
        case = relace_case_with_re_v2(case)

        # 发起http请求
        if hasattr(Data, "token"):
            resp = self.hr.send_request(case["method"], case["url"], case["request_data"], token=getattr(Data, "token"))
        else:
            resp = self.hr.send_request(case["method"], case["url"], case["request_data"])

        resp = resp.json()

        # 如果有提取字段，在响应结果中提取对应的数据，要设置为Data.token
        if case['extract']:
            set_dataclass_attr_from_resp(resp, case["extract"])
