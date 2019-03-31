#!/usr/bin/env python3


# file   : main.py
# author : AI_39
# version: v0.0
# date   : 2019/01/01
# coding : utf-8
# brief  : bilibili动画信息爬虫的主函数


from spider import *


def main():
    try:
        spider0 = Spider0(START_URL_0, REDIS_KEY_0, MONGO_DB, MONGO_COLLECTION)
        spider0.run()
        spider1 = Spider1(START_URL_1, REDIS_KEY_1, MONGO_DB, MONGO_COLLECTION)
        spider1.run()
    except:
       main()


if __name__ == '__main__':
    main()
