#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
爬虫->http://www.juemei.com/mm/上->美女图片

Usage:
  naval_fate.py [-n THREAD_NUM] [-o OUTPUT] [-l LIMIT]
  naval_fate.py -h | --help

Options:
  -h, --help     查看程序运行帮助.
  -n THREAD_NUM  指定并发线程数（默认10个）[default: 10].
  -o OUTPUT      图片存储目录 [default: ./pics].
  -l LIMIT       限制爬多少图片就结束（默认不限制）[default: None].
"""

from docopt import docopt
from pprint import pprint


if __name__ == '__main__':
    arguments = docopt(__doc__)
    pprint(arguments)
