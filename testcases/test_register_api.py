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
        cls.ha = HandleAssert()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.ha.close_sql_conn()

    @data(*cases)
    def test_register(self, case):
        logger.info("=====  开始执行第一个测试用例  =====")
        logger.info("从excel中读取的测试数据为：{}".format(case))

        # 替换数据
        case = relace_case_with_re_v2(case)

        # 发起一次http请求
        resp = self.hr.send_request(case["method"], case["url"], case["request_data"])

        if case["expected"]:
            # 响应结果的字典类型
            actual = resp.json()
            # 期望结果的字典类型
            expected_json = eval(case["expected"])
            logger.info("期望结果为： \n {}".format(expected_json))
            logger.info("实际结果为： \n {}".format(actual))

            # 断言
            try:
                assert actual["code"] == expected_json["code"]
                assert actual["msg"] == expected_json["msg"]
            except AssertionError:
                logger.exception("断言失败")
                raise
            except:
                logger.exception("除断言以外的其他失败")
                raise

        sleep(1)
        if case["check_sql"]:
            self.ha.assert_sql(case["check_sql"])
