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
from jsonpath import jsonpath

from common.myddt import ddt,data
from common.handle_excel import HandleExcel
from common.handle_path import testdata_dir
from common.handle_requests import HandleRequests

case_path = os.path.join(testdata_dir,"api_cases.xlsx")
he = HandleExcel(case_path,"充值")
cases = he.get_all_data()

@ddt
class TestRecharge(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # 实例化HandleRequests类，
        cls.hr = HandleRequests()
        # 调用登陆接口，从响应结果当中，提取token,member_id
        resp = cls.hr.send_request("post",
                                    "http://api.lemonban.com/futureloan/member/login",
                                    {"mobile_phone":"15500000000","pwd":"12345678"})
        # 转换成字典，提取
        resp_dict = resp.json()
        # cls.member_id = resp_dict["data"]["id"]
        # cls.token = resp_dict["data"]["token_info"]["token"]
        # 通过jsonpath提取响应结果
        cls.member_id = jsonpath(resp_dict,"$..id")
        cls.token = jsonpath(resp_dict,"$..token")

    @data(*cases)
    def test_recharge(self,case):
        # 替换
        if case["request_data"].find("#member_id#") != -1:
            case["request_data"] = case["request_data"].replace("#member_id#",str(self.member_id))

        # 并发起http请求
        resp = self.hr.send_request(case["method"],case["url"],case["request_data"],token=self.token)
        print(resp.json())
        # 如果有期望结果，则要比对实现与期望


        # 7、如果有数据库校验，则要做数据库校验