#!/usr/bin/env python3


# file   : request_queue.py
# author : AI_39
# version: v0.0
# date   : 2019/01/01
# coding : utf-8
# brief  : bilibili动画信息爬虫的请求队列模块


import redis
from pickle import dumps, loads
from request import Request
from config import *


class RedisQueue:
    def __init__(self, redis_key, redis_host=REDIS_HOST, redis_port=REDIS_PORT, redis_password=REDIS_PASSWORD, redis_db=REDIS_DB):
        """
        初始化Redis
        """
        self.redis_key = redis_key              # 调度队列所对应的Redis数据库键值
        self.db = redis.Redis(host=redis_host, port=redis_port, password=redis_password, db=redis_db)

    def add(self, request):
        """
        向队列添加序列化后的Request
        :param request: 请求对象
        :return: 添加结果
        """
        if isinstance(request, Request):
            return self.db.rpush(self.redis_key, dumps(request))
        return False

    def pop(self):
        """
        取出下一个Request并反序列化
        :return: Request or None
        """
        if not self.empty():
            return loads(self.db.lpop(self.redis_key))
        else:
            return False

    def clear(self):
        self.db.delete(self.redis_key)

    def empty(self):
        return self.db.llen(self.redis_key) == 0
