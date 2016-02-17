#!/usr/bin/env python
# -*- coding: utf-8 -*-
# import requests
# import re
# payload = {'index': 1, 'count':324, 'pagesize': 9}
# r = requests.post('http://data.qingdao.gov.cn/data/template/list_simpletableview.htm?isWidget=true&cata_id=1184953&meta_id=1185071')
# f = open('test.txt', "wb")
# f.write(r.text.encode('utf-8'))
# f.close
# f = open('gy_org.txt', 'r')
# ff = f.read()
# reg = r'name = "(.*)"'
# pattern = re.compile(reg)
# orgs = re.findall(pattern, ff)
# for org in orgs:
#     print org
# f.close()

# l = ['', '/', '/', '/hjyzybh/tdqyhjbh/rwsthjbh/index.htm']
# print len(l)
# url = 'http://www.bjdata.gov.cn/zyml/azt//lyzs/zs/xjjd/index.htm'
# b = url.replace('index', '3284')
# c = filter(str.isdigit, b)
# print b,c

import re


def delete_white(arg):
    pattern = re.compile('\s+')
    new_str = re.sub(pattern, '', arg)
    return new_str


def get_infor(html, key):
    pattern = re.compile(key + '(.*)')
    temp = re.findall(pattern, html)
    result = ''
    if len(temp) != 0:
        result = temp[0]
    return result


def get_detail(html, key):
    f = open('test.txt', 'wb')
    f.write(html)
    f.close()
    f = open('test.txt', 'r')
    for line in f.readlines():
        buf = get_infor(delete_white(line), key)
        if buf != '':
            break
    return buf

import urllib2
url = 'http://www.bjdata.gov.cn/docs/机场班车站点.txt'
response = urllib2.urlopen(url)
html = response.read()
html = unicode(html, "gb2312").encode("utf8")
print get_detail(html, '资源摘要')
