#!/usr/bin/env python3


# file   : storage.py
# author : AI_39
# version: v0.0
# date   : 2019/01/01
# coding : utf-8
# brief  : bilibili动画信息爬虫的存储模块


import pymongo
from config import *


class Mongo:
    def __init__(self, host=MONGO_HOST, port=MONGO_PORT, database=MONGO_DB, collection=MONGO_COLLECTION):
        """
        MySQL初始化
        :param host      : MONGO数据库地址
        :param port      : MONGO数据库端口
        :param database  : MONGO数据库数据表
        :param collection: MONGO数据库数据表中的集合
        :return          : None
        """
        self.client = pymongo.MongoClient(host, port)                # 创建MongoDB的连接对象
        self.db = self.client[database]                              # 指定需要操作的数据库数据表
        self.collection = self.db[collection]                        # 指定数据库数据表中需要操作的集合

    def save(self, dict, key):
        """
        通过调用pymongo库存储数据到mongo数据库
        :param dict: 字典格式的数据
        :return    : None
        """
        if dict:
            old = self.collection.find_one({key: dict[key]})
            try:
                if old == None:
                    self.collection.insert_one(dict)
                    print("存储到MongoDB成功")
                else:
                    condition = {key: dict[key]}
                    self.collection.update_one(condition, {'$set': dict})
                    print("更新到MongoDB成功")
            except Exception as e:
                print("存储到MongoDB失败，失败原因：", e)
        else:
            print("dict数据为空，无法存储到MongoDB")

    def delete(self):
        """
        删除集合中的所有数据
        :return: None
        """
        self.collection.delete_many({})
        print("删除MongoDB集合所有数据成功")

    def drop(self):
        """
        删除数据表里的集合
        :return: None
        """
        if self.collection.drop():
            print("删除MongoDB集合成功")
        else:
            print("MongoDB集合不存在")
