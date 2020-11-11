# main.py
# 接口自动化测试框架入口

import unittest
from BeautifulReport import BeautifulReport
from common.handle_path import testcases_dir
from common.handle_path import report_dir

ss = unittest.TestLoader().discover(testcases_dir)

br = BeautifulReport(ss)
br.report("接口自动化测试报告", "py33-register-apitest", report_dir)
