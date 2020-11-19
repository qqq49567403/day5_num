# test_register_api.py
# 执行注册测试用例

import unittest
import os
from common.myddt import ddt, data
from time import sleep

from common.handle_replace import relace_case_with_re_v2
from common.handle_excel import HandleExcel
from common.handle_logger import logger
from common.handle_path import testdata_dir
from common.handle_requests import HandleRequests
from common.handle_assert import HandleAssert

excel_path = os.path.join(testdata_dir, 'api_cases.xlsx')
he = HandleExcel(excel_path, '注册')
cases = he.get_all_data()


@ddt
class TestApiRegister(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.hr = HandleRequests()
        cls.hassert = HandleAssert()

    @data(*cases)
    def test_register(self, case):
        logger.info("=====  开始执行第一个测试用例  =====")
        logger.info("从excel中读取的测试数据为：{}".format(case))
        logger.info("从excel中读取的测试数据为：{}".format(type(case)))

        # 替换数据
        case = relace_case_with_re_v2(case)

        # 发起一次http请求
        resp = self.hr.send_request(case["method"], case["url"], case["request_data"])

        resp = resp.json()

        if case["expected"]:
            self.hassert.get_json_compare_res(case["expected"], resp)

        sleep(0.2)
        if case["check_sql"]:
            self.hassert.init_sql_conn()
            self.hassert.get_multi_sql_compare_resp(case["check_sql"])
            self.hassert.close_sql_conn()
