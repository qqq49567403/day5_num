# handle_path.py
# 存放项目使用到的路径
import os
# 项目根目录
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 配置文件目录
conf_dir = os.path.join(root_dir, 'conf')
# 日志输出目录
log_dir = os.path.join(root_dir, 'output', 'log')
# 报告输出目录
report_dir = os.path.join(root_dir, 'output', 'report')
# 测试数据目录
testdata_dir = os.path.join(root_dir, 'testdatas')
# 测试用例目录
testcases_dir = os.path.join(root_dir, 'testcases')