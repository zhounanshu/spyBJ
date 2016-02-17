#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import requests
import urllib2
import MySQLdb


def delete_white(arg):
    pattern = re.compile('\s+')
    new_str = re.sub(pattern, '', arg)
    return new_str


def get_href(arg):
    pattern = re.compile(r'href="(.*?)">')
    temp = re.findall(pattern, arg)
    return temp


def get_ids(html):
    pattern = re.compile('"(\d+).htm')
    temp = re.findall(pattern, html)
    return temp
# 文件格式, 文件数


def get_foramt(html):
    reg = r'lblFileName">(.*)</span>'
    pattern = re.compile(reg)
    temp = re.findall(pattern, html)
    num_of_files = len(temp)
    file_format = ''
    for t in temp:
        file_format += t.split('.')[1]
        file_format += ','
    if file_format != '':
        file_format = file_format[:-1]
    return file_format, num_of_files


def get_downloads(data_id):
    article_url = "http://www.bjdata.gov.cn/cms/web/count.jsp?articleID=" + \
        str(data_id)
    r = requests.post(article_url).text.encode('utf-8')
    pattern = re.compile('\'(.*)\'')
    nums = re.findall(pattern, r)
    num = 0
    if len(nums) != 0:
        num = nums[0]
    return num


def get_update(html):
    pattern = re.compile('上传日期：</b>(.*?)</span>')
    temp = re.findall(pattern, html)
    publish_time = ''
    if len(temp) != 0:
        publish_time = delete_white(temp[0])
    return publish_time


def get_des(html):
    pattern = re.compile(
        'Description" class="indent">(.*?)</span>')
    temp = re.findall(pattern, html)
    result = ''
    if len(temp) != 0:
        result = delete_white(temp[0].decode('utf8'))
    return result


def get_tag(html):
    pattern = re.compile(
        'Keywords" class="indent">(.*)</span>')
    temp = re.findall(pattern, html)
    result = ''
    if len(temp) != 0:
        result = delete_white(temp[0])
    return result


def get_org(html):
    pattern = re.compile(
        'Organization" class="indent">(.*)</span>')
    temp = re.findall(pattern, html)
    result = ''
    if len(temp) != 0:
        result = delete_white(temp[0])
    return result


def get_cate(html):
    pattern = re.compile(
        'TopicClass" class="indent">(.*)</span>')
    temp = re.findall(pattern, html)
    result = ''
    if len(temp) != 0:
        result = delete_white(temp[0])
    return result


def get_title(html):
    pattern = re.compile(
        r'Name" class="lblTitle">(.*)</span>')
    temp = re.findall(pattern, html)
    result = ''
    if len(temp) != 0:
        result = delete_white(temp[0])
    return result


def get_test(html):
    pattern = re.compile(
        r'<span class="lblListTitle">(.*)</span>')
    temp = re.findall(pattern, html)
    result = ''
    if len(temp) != 0:
        result = delete_white(temp[0])
    return result


def text_url(html):
    pattern = re.compile('/docs(.*?)txt"')
    temp = re.findall(pattern, html)
    result = ''
    if len(temp) != 0:
        result = delete_white(temp[0])
    return result


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


def upload_data(data_id, title, desc,
                tag, category, orgnization,
                num_of_download, updated_date, format,
                publication_date, update_frequency, update_on_time,
                updated_on_time_value, publication_type,
                num_of_files, num_of_visits):
    try:
        conn = MySQLdb.connect(host='localhost',
                               port=3306,
                               user='root',
                               passwd='marvinzns',
                               db='shfd',
                               charset='utf8')
        cur = conn.cursor()
        sql = "insert into beijing(data_id, title, descr,\
                    tag, category, orgnization, \
                    num_of_download, updated_date, format, \
                    publication_date,update_frequency,update_on_time, \
                    updated_on_time_value, publication_type,\
                    num_of_files, num_of_visits) values(%s, %s,%s,\
                    %s, %s,%s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s)"
        param = (data_id, title, desc,
                 tag, category, orgnization,
                 num_of_download, updated_date, format,
                 publication_date, update_frequency,
                 update_on_time, updated_on_time_value,
                 publication_type, num_of_files, num_of_visits)
        cur.execute(sql, param)
        conn.commit()
        cur.close()
        conn.close()
        return True
    except:
        return False
reg = r'<ul class="tree-two"(.*?)</ul>'
pattern = re.compile(reg, re.S)
r = requests.post(
    'http://www.bjdata.gov.cn/zyml/azt/lyzs/zs/xjjd/index.htm').text.encode('utf-8')
temp = re.findall(pattern, r)
urls = []
error_buf = []
for i in range(len(temp)):
    buf = get_href(delete_white(temp[i]))
    urls.extend(buf)
hrefs = []
for url in urls:
    buf = ''
    count = len(url.split('..'))
    if count == 1:
        buf = '/lyzs/zs/xjjd/index.htm'
    if count == 2:
        buf = '/lyzs/zs' + url.split('..')[-1]
    if count == 3:
        buf = '/lyzs' + url.split('..')[-1]
    if count == 4:
        buf = url.split('..')[-1]
    hrefs.append(buf)
base_url = 'http://www.bjdata.gov.cn/zyml/azt/'
data_ids = []
data_urls = []
for item in hrefs:
    url = base_url + item
    r = requests.post(url).text.encode('utf-8')
    for item in get_ids(r):
        data_urls.append(url.replace('index', item))
    data_ids.extend(get_ids(r))
for item in data_urls:
    response = urllib2.urlopen(item)
    r = response.read()
    data_id = filter(str.isdigit, item)
    num_of_download = get_downloads(data_id)
    updated_date = get_update(r)
    response = urllib2.urlopen('http://www.bjdata.gov.cn/docs' + text_url(r) + 'txt')
    html = response.read()
    html = unicode(html, "gb18030").encode("utf8")
    title = get_detail(html, '资源名称')
    desc = get_detail(html, '资源摘要')
    tag = get_detail(html, '关键字说明')
    category = get_detail(html, '资源分类')
    orgnization = get_detail(html, '资源所有权单位')
    format = get_detail(html, '资源类型')
    publication_date = get_detail(html, '资源出版日期')
    update_frequency = get_detail(html, '资源更新周期')
    update_on_time = ''
    num_of_files = get_foramt(r)[1]
    num_of_visits = ''
    publication_type = get_detail(html, '数据安全限制分级')
    if not upload_data(data_id, title, desc,
                       tag, category, orgnization,
                       num_of_download, updated_date, format,
                       publication_date, update_frequency, update_on_time,
                       '', publication_type, num_of_files, num_of_visits):
        print "insert error!"
        error_buf.append(url)
for error_url in error_buf:
    print error_url
