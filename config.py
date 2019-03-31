#!/usr/bin/env python3


# file   : config.py
# author : AI_39
# version: v0.0
# date   : 2019/01/01
# coding : utf-8
# brief  : bilibili动画信息爬虫的设置


# request_queue.py
REDIS_HOST = '127.0.0.1'                                             # Redis数据库地址
REDIS_PORT = 6379                                                    # Redis数据库端口
REDIS_PASSWORD = 160493                                              # Redis数据库密码
REDIS_DB = 0                                                         # Redis数据库db值
REDIS_KEY_0 = 'bilibili_requests_0'                                  # Redis数据库键值0，用于存储要爬取的完结动画的请求
REDIS_KEY_1 = 'bilibili_requests_1'                                  # Redis数据库键值1，用于存储要爬取的番剧索引的请求


# spider.py
START_URL_0 = 'https://www.bilibili.com/v/anime/finish/?spm_id_from=333.110.b_7072696d6172795f6d656e75.9#/' +\
              'all/default/0/'                                       # 爬取完结动画的链接前缀
PAGE_START_0 = 1                                                     # 爬取完结动画网页的首页
PAGE_STOP_0 = 863                                                    # 爬取完结动画网页的尾页
START_URL_1 = 'https://www.bilibili.com/anime/index/?spm_id_from=333.110.b_7375626e6176.7#season_version=-1&' +\
              'area=-1&is_finish=-1&copyright=-1&season_status=-1&season_month=-1&' + \
              'pub_date=-1&style_id=-1&order=2&st=1&sort=0&page='    # 爬取番剧索引的链接前缀
PAGE_START_1 = 1                                                     # 爬取番剧索引网页的首页
PAGE_STOP_1 = 157                                                    # 爬取番剧索引网页的尾页
MAX_FAILED_TIME = 3
MAX_WAITED_TIME = 10
SCHEDULE_CYCLE = 1


# storage.py
MONGO_HOST = 'localhost'                                             # mongo数据库地址
MONGO_PORT = 27017                                                   # mongo数据库端口
MONGO_DB = 'bilibili'                                                # mongo数据库数据表
MONGO_COLLECTION = 'animations'                                      # mongo数据库数据表中的集合
