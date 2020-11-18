# handle_requests.py
# 封装发送接口请求

import requests
import json

from common.handle_logger import logger
from common.handle_conf import conf


class HandleRequests:
    def __init__(self):
        self.headers = {"X-Lemonban-Media-Type": "lemonban.v2"}

    # 处理请求头信息-token
    def __deal_token(self, token=None):
        if token is not None:
            self.headers["Authorization"] = "Bearer {}".format(token)

    # 处理请求数据
    def __deal_data(self, data):
        if isinstance(data, str):
            self.data = json.loads(data)
        else:
            self.data = data
        logger.info("请求数据为：{}".format(self.data))

    # 处理url地址
    def __deal_url(self, url):
        # 从配置文件读取baseurl
        base_url = conf.get("server", 'baseurl')
        # 拼接，拼接除的斜杠在配置文件中处理，excel当中不能/开头
        url = base_url + url
        return url

    # 发送一次http请求
    def send_request(self, method, url, data=None, token=None):
        logger.info("=====  发送一次http请求  =====")
        logger.info("请求的mehtod为：{}".format(method))
        logger.info("请求的url为：{}".format(url))
        # 请求url地址处理
        url = self.__deal_url(url)
        # 处理请提头部信息
        self.__deal_data(data)
        # 处理请求数据
        self.__deal_token(token)
        # 发送一次http请求，传入method，url，data，token信息
        if method.upper() == "GET":
            response = requests.get(url, params=self.data, headers=self.headers)
        elif method.upper() == "POST":
            response = requests.post(url, json=self.data, headers=self.headers)
        else:
            response = requests.patch(url, json=self.data, headers=self.headers)
        logger.info("响应的code为：{}".format(response.status_code))
        logger.info("响应的msg为：{}".format(response.json()))
        return response



if __name__ == '__main__':
    ss = HandleRequests()
    url = "http://api.lemonban.com/futureloan/member/login"
    data = {"mobile_phone": "18557519118", "pwd": "123456789"}
    resq = ss.send_request("post", url, data)
    resq_dict = resq.json()
    print(resq_dict)
