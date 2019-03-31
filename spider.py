#!/usr/bin/env python3


# file   : spider.py
# author : AI_39
# version: v0.0
# date   : 2019/01/01
# coding : utf-8
# brief  : bilibili动画信息爬虫的爬虫对象模块


import time
import json
import lxml
import pymongo
from storage import Mongo
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup
from request import Request
from request_queue import RedisQueue
from config import *


class Spider:
    def __init__(self, start_url, redis_key, mongo_database, mongo_collection):
        """"""
        self.base_url = start_url                                                   # 初始化爬取链接的前缀
        self.mongo = Mongo(database=mongo_database, collection=mongo_collection)    # 初始化存储对象
        self.request_queue = RedisQueue(redis_key=redis_key)                        # 初始化调度队列对象
        options = webdriver.ChromeOptions()                                         # 初始化浏览器对象
        options.add_argument('--headless')                                          # 设置无界面模式
        self.browser = webdriver.Chrome(chrome_options=options)

    def start(self, page_start, page_stop):
        """
        开始工作，将所有要爬取的链接放入任务队列
        :return: None
        """
        self.request_queue.clear()  # 清空历史任务列表
        page = page_start
        while page <= page_stop:
            request_url = '{url}{num}'.format(url=self.base_url, num=page)
            bilibili_request = Request(url=request_url)
            self.request_queue.add(bilibili_request)
            page += 1

    def stop(self):
        """
        结束工作，关闭浏览器
        :return: None
        """
        self.browser.close()                                         # 关闭浏览器

    def get_html(self, request, waited_element):
        """
        获取url对应的网页信息
        :param url: 网页链接
        :param waited_element: 等待的元素
        :return: 页面信息
        """
        try:
            print("正在爬取" + request.url)
            self.browser.get(request.url)
            # time.sleep(1)
            wait = WebDriverWait(self.browser, MAX_WAITED_TIME)      # 指定最长等待时间
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, waited_element)))
            html = self.browser.page_source
        except TimeoutException:                                     # 页面加载超时异常处理
            html = None
        return html

    def error(self, bilibili_request):
        """
        错误处理
        :param  :
        :return: None
        """
        bilibili_request.fail_time += 1
        print('Request Failed', bilibili_request.fail_time, 'Times', bilibili_request.url)
        if bilibili_request.fail_time < MAX_FAILED_TIME:
            self.request_queue.add(bilibili_request)
        else:
            print('Request Failed',  bilibili_request.url)


class Spider0(Spider):
    def __init__(self, start_url, mongo_database, mongo_collection, redis_key):
        super().__init__(start_url, mongo_database, mongo_collection, redis_key)

    def parse_detail(self, html):
        """
        解析页面信息，获取完结动画的相关信息
        :param html: 页面信息
        :return: 完结动画的相关信息
        """
        soup = BeautifulSoup(html, "lxml")
        page_tag = soup.find('ul', class_="vd-list mod-2")
        page_list = page_tag.find_all('li')
        for i in page_list:
            a_tag = i.find('a', class_='title')
            span_tag_list = i.find_all('span', class_='v-info-i')
            title = a_tag['title']
            href = 'https:' + a_tag['href']
            value_a = span_tag_list[0].get_text(strip=True)
            if '--' == value_a:                                      # 特殊处理开始
                a = '0'
                history_dict = {
                        "title": title,
                        "href": href,
                        "观看总数": value_a,
                    }
                with open("old_task.txt", "a", encoding="utf-8") as file:
                    file.write(json.dumps(history_dict, ensure_ascii=False) + '\n')
            elif '.' in value_a:
                a_list = value_a.split('.')
                if '万' in a_list[1]:
                    a = "{}".format(int(a_list[0] + a_list[1].strip('万')) * 1000)
                elif '亿' in a_list[1]:
                    a = "{}".format(int(a_list[0] + a_list[1].strip('亿')) * 10000000)
                else:
                    a = value_a
            else:
                a = value_a
            video_dict = {
                "title": title,
                "href": href,
                "观看总数": int(a),
            }
            yield video_dict

    def schedule(self, cycle=SCHEDULE_CYCLE):
        """
        调度请求
        :return: None
        """
        while not self.request_queue.empty():
            bilibili_request = self.request_queue.pop()
            print('Schedule', bilibili_request.url)
            response = super().get_html(bilibili_request, '#videolist_box .vd-list-cnt li > .l-item')
            if response:
                try:
                    results = list(self.parse_detail(response))
                    if results:
                        for result in results:
                            if isinstance(result, dict):
                                self.mongo.save(result, 'title')
                    else:
                        super().error(bilibili_request)
                except Exception as e:
                    print(e)
                    super().error(bilibili_request)
            else:
                super().error(bilibili_request)
        # time.sleep(cycle)

    def run(self):
        """
        入口
        :return: None
        """
        # self.request_queue.clear()  # 清空历史任务列表
        super().start(PAGE_START_0, PAGE_STOP_0)
        self.schedule()
        super().stop()


class Spider1(Spider):
    def __init__(self, start_url, mongo_database, mongo_collection, redis_key):
        super(Spider1, self).__init__(start_url, mongo_database, mongo_collection, redis_key)

    def parse_detail(self, html):
        """
        解析页面信息，获取完结动画的相关信息
        :param html: 页面信息
        :return: 完结动画的相关信息
        """
        soup = BeautifulSoup(html, "lxml")
        page_tag = soup.find('ul', class_="bangumi-list clearfix")
        page_list = page_tag.find_all('li')
        for i in page_list:
            a_tag = i.find('a', class_='bangumi-title')
            div_tag = i.find('div', class_='shadow')
            title = a_tag.get_text(strip=True)
            href = 'https:' + a_tag['href']
            value_a = div_tag.get_text(strip=True)
            if '--' == value_a:  # 特殊处理开始
                a = 0
                history_dict = {
                    "title": title,
                    "href": href,
                    "观看总数": value_a,
                }
                with open("old_task.txt", "a", encoding="utf-8") as file:
                    file.write(json.dumps(history_dict, ensure_ascii=False) + '\n')
            elif '.' in value_a:
                a_list = value_a.split('.')
                if '万' in a_list[1]:
                    a = int("{}".format(int(a_list[0] + a_list[1].strip('万次播放')) * 1000))
                elif '亿' in a_list[1]:
                    a = int("{}".format(int(a_list[0] + a_list[1].strip('亿次播放')) * 10000000))
                else:
                    a = 0
            else:
                if '万' in value_a:
                    a = int("{}".format(int(value_a.strip('万次播放')) * 10000))
                elif '亿' in value_a:
                    a = int("{}".format(int(value_a.strip('亿次播放')) * 100000000))
                else:
                    a = int(value_a)
            video_dict = {
                "title": title,
                "href": href,
                "观看总数": a,
            }
            yield video_dict

    def schedule(self, cycle=SCHEDULE_CYCLE):
        """
        调度请求
        :return: None
        """
        while not self.request_queue.empty():
            bilibili_request = self.request_queue.pop()
            print('Schedule', bilibili_request.url)
            response = super().get_html(bilibili_request, '.filter-body')
            if response:
                try:
                    results = list(self.parse_detail(response))
                    if results:
                        for result in results:
                            if isinstance(result, dict):
                                pass
                                self.mongo.save(result, 'title')
                    else:
                        super().error(bilibili_request)
                except Exception as e:
                    print(e)
                    super().error(bilibili_request)
            else:
                super().error(bilibili_request)
        # time.sleep(cycle)

    def run(self):
        """
        入口
        :return: None
        """
        # self.request_queue.clear()  # 清空历史任务列表
        super().start(PAGE_START_1, PAGE_STOP_1)
        self.schedule()
        super().stop()
