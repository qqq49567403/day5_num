
"""
1、从excel当中读取登陆接口的测试数据   recharge
2、编写测试类，继承unittest.TestCase
3、使用ddt，读取每一组测试数据
   3、前置处理：token,member_id
   4、在发起http请求之前，是否要替换数据
   5、发起http请求
   6、如果有期望结果，则要比对实现与期望
   7、如果有数据库校验，则要做数据库校验
"""

import os
import unittest

from common.myddt import ddt, data
from common.handle_excel import HandleExcel
from common.handle_path import testdata_dir
from common.handle_requests import HandleRequests
from common.handle_replace import relace_case_with_re_v2
from common.handle_data import Data,set_dataclass_attr_from_resp
from common.handle_assert import HandleAssert

case_path = os.path.join(testdata_dir, "api_cases.xlsx")
he = HandleExcel(case_path, "充值")
cases = he.get_all_data()


@ddt
class TestRecharge(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        # 实例化HandleRequests类，
        cls.hr = HandleRequests()
        cls.ha = HandleAssert()  # 有去连接数据库

    @classmethod
    def tearDownClass(cls) -> None:
        cls.ha.close_sql_conn()  # 有关闭数据库连接

    @data(*cases)
    def test_recharge(self, case):
        # 替换
        case = relace_case_with_re_v2(case)

        # 并发起http请求
        # 判断是否要传递token值。
        if hasattr(Data, "token"):
            resp = self.hr.send_request(case["method"], case["url"], case["request_data"], token=getattr(Data, "token"))
        else:
            resp = self.hr.send_request(case["method"], case["url"], case["request_data"])

        resp = resp.json()
        print(resp)
        # 如果有提取字段，那么需要从响应结果当中，提取对应的数据。要设置为Data.token
        if case["extract"]:
            set_dataclass_attr_from_resp(resp, case["extract"])

        # # 如果有数据库校验，则要做数据库校验
        if case["check_sql"]:
            self.ha.assert_sql(case["check_sql"])
