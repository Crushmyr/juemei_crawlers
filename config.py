#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 开始爬取图片的网址（一般为主站）
START_URL = 'http://www.juemei.com/mm/'
# 需要爬取的网址的正则表达式
URL_TO_SCAN_PATT = r'/mm/[^"\']+'
# 需要下载的图片的正则表达式
IMG_TO_DOWN_PATT = (r'http://img\.juemei\.com/\w+/'
                    r'\d{4}-\d{2}-\d{2}/\w{13}\.jpg')
