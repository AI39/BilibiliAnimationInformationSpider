#!/usr/bin/env python3


# file   : request.py
# author : AI_39
# version: v0.0
# date   : 2019/01/01
# coding : utf-8
# brief  : bilibili动画信息爬虫的请求对象模块


from config import *


class Request:
    def __init__(self, url=None, fail_time=0):
        self.url = url                                               # 请求链接
        self.fail_time = fail_time                                   # 失败次数
