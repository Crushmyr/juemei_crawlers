#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys
import os
import time
from docopt import docopt

import spider
from config import *


# 将输入的参数中的线程数和限制数转化为int类型
def str2_int(var):
    try:
        var = int(var)
        return var
    except Exception as e:
        print('-l 或者 -n 后面的参数必须是数字')
        sys.exit()


def main():
    start = time.time()
    doc = """
爬虫->http://www.juemei.com/mm/上->美女图片

Usage:
    mm_crawler.py [-n THREAD_NUM] [-o OUTPUT] [-l LIMIT]
    mm_crawler.py -h | --help

Options:
    -h, --help     查看程序运行帮助.
    -n THREAD_NUM  指定并发线程数（默认10个）[default: 10].
    -o OUTPUT      图片存储目录 [default: ./pics].
    -l LIMIT       限制爬多少图片就结束（默认不限制）[default: 0].

Example:
    python mm_crawler.py -n 20 -o ~/Downloads -l 100
"""
    args = docopt(doc)
    path = args['-o']
    if not os.path.isdir(path):
        try:
            os.mkdir(path)
        except Exception as e:
            print('请输入正确的目录路径')
            sys.exit()

    args['-l'] = str2_int(args['-l'])
    args['-n'] = str2_int(args['-n'])

    func = spider.DownloadImageThread.scan_url
    thread_pool = spider.ThreadPool(args)
    thread_pool.add_job(func, START_URL)
    thread_pool.start_job()
    thread_pool.wait()
    print('Finished in {0:.2f} seconds'.format(time.time() - start))


if __name__ == '__main__':
    main()
