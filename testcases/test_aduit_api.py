"""
======================
Author: ss
Time: 2020-11-17
Project: test_aduit_api
Company: 软件自动化测试
======================
"""

# 执行审核测试用例

import os
import unittest

from common.handle_data import set_dataclass_attr_from_resp,Data
from common.myddt import ddt,data
from common.handle_excel import HandleExcel
from common.handle_requests import HandleRequests
from common.handle_replace import relace_case_with_re_v2
from common.handle_path import testdata_dir
from common.handle_assert import HandleAssert

excel_path = os.path.join(testdata_dir, "api_cases.xlsx")
he = HandleExcel(excel_path, "审核")
cases = he.get_all_data()

@ddt
class TestAduit(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.hr = HandleRequests()
        cls.hassert = HandleAssert()  # 打开数据库连接

    @data(*cases)
    def test_aduit(self, case):
        # 替换
        case = relace_case_with_re_v2(case)

        # 判断是否有token值
        if hasattr(Data, "token"):
            resp = self.hr.send_request(case["method"], case["url"], case["request_data"], token=getattr(Data, "token"))
        else:
            resp = self.hr.send_request(case["method"], case["url"], case["request_data"])

        # 响应结果转化成字典
        resp = resp.json()

        # 判断是否有提取字段
        if case["extract"]:
            set_dataclass_attr_from_resp(resp, case["extract"])

        # 判断是否有期望值，进行比对
        if case["expected"]:
            self.hassert.get_json_compare_res(case["expected"], resp)
        # 判断是否有数据库校验
        if case["check_sql"]:
            self.hassert.init_sql_conn()
            self.hassert.get_multi_sql_compare_resp(case["check_sql"])
            self.hassert.close_sql_conn()

        # 最终结果
        self.hassert.assert_result()