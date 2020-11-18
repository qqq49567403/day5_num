"""
======================
Author: ss
Time: 2020-11-17
Project: test_setup
Company: 软件自动化测试
======================
"""

# 前置数据处理

import os
import unittest

from common.handle_path import testdata_dir
from common.myddt import ddt, data
from common.handle_excel import HandleExcel
from common.handle_requests import HandleRequests
from common.handle_replace import relace_case_with_re_v2
from common.handle_logger import logger

# 获取excel路径
excel_path = os.path.join(testdata_dir, "api_cases.xlsx")
he = HandleExcel(excel_path, "全局前置操作")
cases = he.get_all_data()

@ddt
class TestSetup(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.hr = HandleRequests()

    @data(*cases)
    def test_setup(self, case):
        logger.info("=====开始执行前置操作=====")
        logger.info("从excel当中，读取的测试用例为：{}".format(case))
        # 替换
        case = relace_case_with_re_v2(case)

        # 发起http请求
        resp = self.hr.send_request(case["method"], case["url"], case["request_data"])
