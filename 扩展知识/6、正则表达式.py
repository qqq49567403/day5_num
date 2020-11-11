"""
======================
Author: ss
Time: 2020-11-10
Project: 6、正则表达式
Company: 软件自动化测试
======================
"""

import re

ss = "abcRu122434$@@34WS3543*&122你好"

sss = '{"member_id":"#member_id#","amount":2000,"bid_id":"#bid_id#"}'

res = re.findall("#(\w*)#",sss)
print(res)