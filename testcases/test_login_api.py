# test_login_api.pyn
# 执行登录测试用例

import os
import unittest
from common.myddt import ddt, data

from common.handle_excel import HandleExcel
from common.handle_path import testdata_dir
from common.handle_phone import get_new_phone
from common.handle_requests import HandleRequests


case_path = os.path.join(testdata_dir, 'api_cases.xlsx')
he = HandleExcel(case_path, '登陆')
cases = he.get_all_data()
# print(cases)

@ddt
class TestLogin(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.hr = HandleRequests()

    @data(*cases)
    def test_login(self, case):
        # 替换
        if case["request_data"].find("#phone#") != -1:
            phone = get_new_phone()
            case["request_data"] = case["request_data"].replace("#phone#", phone)

        # 发起一次http请求
        resp = self.hr.send_request(case["method"], case["url"], case["request_data"])


