## Overview

juemei_crawlers 用来爬取www.juemei.com/mm 的一个图片爬虫。

emmm, 就是模仿知道创宇原来的一个校招题目。。。


## Description

1. 不要把非相关的图片也爬了；
2. 你总该考虑多线程吧？或者协程；
3. 命令行-h可以查看程序运行帮助，-n可以指定并发线程数（默认10个），-o可以指定图片存储在哪个目录（默认当前运行目录的pics目录下），-l可以限制爬多少图片就结束（默认不限制）；
4. 思考个问题，如果下次我要爬其他的美女网站，你这个程序如何尽可能利于复用；
5. 把你的实现思路清晰记录在该爬虫项目的目录下：readme.txt；
6. 你可以用Python内置模块与第三方模块来加速你这个任务；


## Requirements

- Python 3.x
- Works on Linux, Windows, Mac OSX...

## Installation

``` bash
$ git clone https://github.com/Crushmyr/juemei_crawlers
```

然后用pip下载第三方库：
``` bash
$ pip install -r requirements.txt
```


## Help

```
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
```
