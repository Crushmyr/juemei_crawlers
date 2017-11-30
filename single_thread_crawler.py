#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import requests
import urllib
import sys
import re
import os
from docopt import docopt


def scan_url(url, url_to_scan_patt, img_to_down_patt):
    url_to_scan_lst = []
    img_to_down_lst = []
    try:
        req = requests.get(url)
        if req.status_code == 200:
            url_to_scan_lst = re.findall(url_to_scan_patt, req.text)
            url_to_scan_lst = [urllib.parse.urljoin(url, i)
                               for i in url_to_scan_lst]
            img_to_down_lst = re.findall(img_to_down_patt, req.text)
    except Exception as e:
        pass
    return (list(set(url_to_scan_lst)), list(set(img_to_down_lst)))


def down_img(url, path):
    if not os.path.isdir(path):
        os.mkdir(path)
    filename = url.split('/')[-1]
    fullname = os.path.join(path, filename)
    print('down_picture from url:{0}'.format(url))
    try:
        req = requests.get(url)
        if req.status_code == 200:
            with open(fullname, 'wb') as f:
                f.write(req.content)
    except Exception as e:
        print(e)


def main():
    doc = """
爬虫->http://www.juemei.com/mm/上->美女图片

Usage:
    mm_crawler.py [-n THREAD_NUM] [-o OUTPUT] [-l LIMIT]
    mm_crawler.py -h | --help

Options:
    -h, --help     查看程序运行帮助.
    -n THREAD_NUM  指定并发线程数（默认10个）[default: 10].
    -o OUTPUT      图片存储目录 [default: ./pics].
    -l LIMIT       限制爬多少图片就结束（默认不限制）[default: None].

Example:
    python mm_crawler.py -n 20 -o ~/Downloads -l 100
"""
    arguments = docopt(doc)
    path = arguments['-o']
    if not os.path.isdir(path):
        try:
            os.mkdir(path)
        except Exception as e:
            print('请输入正确的目录路径')
            sys.exit()

    try:
        limit = int(arguments['-l'])
    except Exception as e:
        print('-l 后面的参数必须是数字')
        sys.exit()

    start_url = 'http://www.juemei.com/mm/'
    url_to_scan_patt = r'/mm/[^"\']+'
    img_to_down_patt = (r'http://img\.juemei\.com/\w+/'
                        r'\d{4}-\d{2}-\d{2}/\w{13}\.jpg')

    url_to_scan_set = set(start_url)
    url_to_scan_set = set()
    img_to_down_set = set()
    url_to_scan_lst_temp, img_to_down_lst_temp = scan_url(start_url,
                                                          url_to_scan_patt,
                                                          img_to_down_patt)

    have_url_to_scan = True
    have_img_to_down = True

    while have_url_to_scan and have_img_to_down:
        have_url_to_scan = False
        url_to_scan_lst = url_to_scan_lst_temp
        img_to_down_lst = img_to_down_lst_temp
        url_to_scan_lst_temp = []
        img_to_down_lst_temp = []

        for url_item in url_to_scan_lst:
            if url_item not in url_to_scan_set:
                have_url_to_scan = True
                url_to_scan_set.add(url_item)
                a, b = scan_url(url_item, url_to_scan_patt, img_to_down_patt)
                for i in a:
                    url_to_scan_lst_temp.append(i)
                for i in b:
                    img_to_down_lst_temp.append(i)

        for img_item in img_to_down_lst:
            if img_item not in img_to_down_set:
                down_img(img_item, path)
                img_to_down_set.add(img_item)
            if len(img_to_down_set) >= limit:
                have_img_to_down = False
                break


if __name__ == '__main__':
    main()
