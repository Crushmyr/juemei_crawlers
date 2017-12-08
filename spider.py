#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading
import queue
import requests
import re
import os
import urllib
from config import *

URL_TO_SCAN_SET = set()
IMG_TO_DOWN_SET = set()


# 线程池类
class ThreadPool(object):
    def __init__(self, args):
        self.args = args
        self.work_queue = queue.Queue()
        self.threads = []
        self.thread_num = self.args['-n']
        self.success_num = 0
        self.running_num = 0
        self.init_pool()

    # 启动线程
    def init_pool(self):
        for i in range(self.thread_num):
            self.threads.append(DownloadImageThread(self, self.args))

    # 添加工作任务
    def add_job(self, func, url):
        self.work_queue.put((func, url))

    # 获取工作任务
    def get_job(self):
        return self.work_queue.get()

    # 工作任务完成
    def job_done(self):
        self.work_queue.task_done()

    # 获取成功下载图片的个数
    def get_success_num(self):
        return self.success_num

    # 增加成功下载图片的个数
    def increase_success_num(self):
        self.success_num += 1

    def get_running_num(self):
        return self.running_num

    def increase_running_num(self):
        self.running_num += 1

    def decrease_running_num(self):
        self.running_num -= 1

    # 开始工作
    def start_job(self):
        for job in self.threads:
            job.start()

    # 等待所有工作完成
    def wait(self):
        for job in self.threads:
            if job.isAlive():
                job.join()


# 下载图片类
class DownloadImageThread(threading.Thread):

    def __init__(self, pool, args):
        threading.Thread.__init__(self)
        self.thread_pool = pool
        self.limit = args['-l']
        self.path = args['-o']

    # 爬取网页
    def scan_url(self, url):
        url_to_scan_lst = []
        img_to_down_lst = []
        try:
            req = requests.get(url)
            if req.status_code == 200:
                # 匹配需要爬取的网址
                url_to_scan_lst = re.findall(URL_TO_SCAN_PATT, req.text)
                url_to_scan_lst = [urllib.parse.urljoin(url, i)
                                   for i in url_to_scan_lst]
                # 匹配需要下载的图片
                img_to_down_lst = re.findall(IMG_TO_DOWN_PATT, req.text)
        except Exception as e:
            pass
        return (list(set(url_to_scan_lst)), list(set(img_to_down_lst)))

    # 下载图片
    def down_img(self, url):
        filename = url.split('/')[-1]
        fullname = os.path.join(self.path, filename)
        print('down_picture from url:{0}'.format(url))
        try:
            req = requests.get(url)
            if req.status_code == 200:
                with open(fullname, 'wb') as f:
                    f.write(req.content)
                return True
            return False
        except Exception as e:
            print(e)
            return False

    def run(self):
        global URL_TO_SCAN_SET
        global IMG_TO_DOWN_SET
        while True:
            try:
                func, url = self.thread_pool.get_job()
                self.thread_pool.increase_running_num()
                # if not url.endswith('.jpg'):
                if func is DownloadImageThread.scan_url:
                    url_to_scan_lst, img_to_down_lst = self.scan_url(url)
                    for url_item in url_to_scan_lst:
                        # 该网址是非已经爬取过了
                        if url_item not in URL_TO_SCAN_SET:
                            URL_TO_SCAN_SET.add(url_item)
                            self.thread_pool.add_job(
                                DownloadImageThread.scan_url, url_item)
                    for img_item in img_to_down_lst:
                        # 该图片是否已经在队列中或者已下载
                        if img_item not in IMG_TO_DOWN_SET:
                            IMG_TO_DOWN_SET.add(url)
                            self.thread_pool.add_job(
                                DownloadImageThread.down_img, img_item)
                elif func is DownloadImageThread.down_img:
                    success_num = self.thread_pool.get_success_num()
                    # 判断成功下载的个数有没有超出限制量
                    if self.limit and success_num >= self.limit:
                        while self.thread_pool.get_running_num() >= 0:
                            self.thread_pool.decrease_running_num()
                        return None
                    success = self.down_img(url)
                    if success:
                        self.thread_pool.increase_success_num()
                self.thread_pool.decrease_running_num()
                self.thread_pool.job_done()
            except queue.Empty:
                if self.thread_pool.get_running_num() <= 0:
                    break
            except Exception as e:
                print(e)
                break
