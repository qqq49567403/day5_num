"""
======================
Author: ss
Time: 2020-11-17
Project: test_invest_api
Company: 软件自动化测试
======================
"""

# 执行投资测试用例

import os
import unittest

from common.handle_assert import HandleAssert
from common.handle_path import testdata_dir
from common.handle_replace import relace_case_with_re_v2
from common.handle_requests import HandleRequests
from common.handle_excel import HandleExcel
from common.myddt import ddt, data
from common.handle_data import set_dataclass_attr_from_resp, Data

excel_path = os.path.join(testdata_dir, "api_cases.xlsx")
he = HandleExcel(excel_path, "投资")
cases = he.get_all_data()


@ddt
class TestInvest(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.hr = HandleRequests()
        cls.hassert = HandleAssert()

    @data(*cases)
    def test_invest(self, case):
        # 替换数据
        case = relace_case_with_re_v2(case)

        # 判断是否有token值
        if hasattr(Data, "token"):
            resp = self.hr.send_request(case["method"], case["url"], case["request_data"], token=getattr(Data, "token"))
        else:
            resp = self.hr.send_request(case["method"], case["url"], case["request_data"])

        # 响应结果转成字典
        resp = resp.json()

        # 判断是否有提取字段
        if case["extract"]:
            set_dataclass_attr_from_resp(resp, case["extract"])

        # 判断是否有响应结果断言
        if case["expected"]:
            self.hassert.get_json_compare_res(case["expected"], resp)

        # 判断是否有数据库校验
        if case["check_sql"]:
            self.hassert.init_sql_conn()
            self.hassert.get_multi_sql_compare_resp(case["check_sql"])
            self.hassert.close_sql_conn()


