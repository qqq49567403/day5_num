# main.py
# 接口自动化测试框架入口

import unittest
from datetime import datetime
from unittestreport import TestRunner

from common.handle_path import testcases_dir
from common.handle_path import report_dir

ss = unittest.TestLoader().discover(testcases_dir)

now_time = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
report_name = "nmb_py33_apitest_{}.html".format(now_time)
# br = BeautifulReport(ss)
# br.report("接口自动化测试报告", "py33-register-apitest", report_dir)

runner = TestRunner(ss,
                    filename=report_name,
                    report_dir=report_dir,
                    title="py33-register-apitest",
                    tester="ss",
                    desc="py33接口测试报告")
runner.run()
runner.send_email(host="smtp.163.com",
                  port=465,
                  user="songsheng920101@163.com",
                  password="ss920101",
                  to_addrs="1129126506@qq.com"
                  )


