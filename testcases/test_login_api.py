# test_login_api.py
# 执行登录测试用例

import os
import unittest
from common.myddt import ddt, data

from common.handle_excel import HandleExcel
from common.handle_path import testdata_dir
from common.handle_requests import HandleRequests
from common.handle_replace import relace_case_with_re_v2


case_path = os.path.join(testdata_dir, 'api_cases.xlsx')
he = HandleExcel(case_path, '登录')
cases = he.get_all_data()


@ddt
class TestLogin(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.hr = HandleRequests()

    @data(*cases)
    def test_login(self, case):
        # 替换
        case = relace_case_with_re_v2(case)

        # 发起一次http请求
        resp = self.hr.send_request(case["method"], case["url"], case["request_data"])

        # 将响应结果转成字典
        resp = resp.json()

        # 判断是否有期望结果，进行对比
        if case["expected"]:
            self.hassert.get_json_compare_res(case["expected"],resp)

