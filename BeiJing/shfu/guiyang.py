#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import re
import MySQLdb
from bs4 import BeautifulSoup


def delete_white(arg):
    pattern = re.compile('\s+')
    new_str = re.sub(pattern, '', arg)
    return new_str


def get_ids(html):
    reg = r'href="/detail\.jsp\?dataid=(.*)">'
    pattern = re.compile(reg)
    ids = re.findall(pattern, html)
    return ids


def get_title(html):
    reg = r'<title>(.*) -'
    pattern = re.compile(reg)
    title = re.findall(pattern, html)[0]
    return title


def get_desc(html):
    reg = r'摘要： </b>(.*?)<'
    pattern = re.compile(reg, re.S)
    desc = re.findall(pattern, html)[0]
    return delete_white(desc)


def get_category(html):
    soup = BeautifulSoup(html, 'lxml')
    s = soup.select('#content > div.toolbar > ol > li > a')
    category = ''
    if len(s) > 1:
        category = re.findall(r'\S+', s[1].get_text())[0]
    else:
        print "there is something wrong"
    return category


def get_downloads(html):
    reg = r'下载次数：(.*)'
    pattern = re.compile(reg)
    nums = re.findall(pattern, html)
    num = max(nums)
    return num


def updates_visits(html):
    reg = r'"color:#7d7d7d;float: left;">(.*?)<'
    pattern = re.compile(reg, re.S)
    bufs = re.findall(pattern, html)
    temp = []
    for buf in bufs:
        temp.append(delete_white(buf))
    return temp


def get_format(html):
    reg = r'数据格式：(.*) &'
    pattern = re.compile(reg)
    formats = re.findall(pattern, html)
    num_of_files = len(formats)
    temp = list(set(formats))
    for f in temp:
        f += ','
    return f[: -1], num_of_files


def get_cate(html):
    reg = r'<dd>(.*)</dd>'
    pattern = re.compile(reg)
    title = re.findall(pattern, html)
    return title


def get_tag(html):
    tag = ''
    reg = r'list\.jsp\?label_id=(.*)"'
    pattern = re.compile(reg)
    temp = re.findall(pattern, html)
    if len(temp) == 0:
        tag = ''
        return tag
    else:
        for t in temp:
            tag += t
            tag += ','
        return tag[:-1]


def get_organization(data_id):
    # 获取所有机构
    orgnization = ''
    orgs = ['水利部', '工信部', '国家地震科学数据共享中心',
            '汤森.路透',
            '行政机关—国务院—发改委',
            '行政机关—国务院—国家税务总局',
            '测试',
            '行政机关—国务院—工信部',
            '行政机关—国务院—食药监',
            '行政机关—国务院—银监会',
            '行政机关—国务院—环保部',
            '行政机关—国务院—国土资源部',
            '贵阳互金产投公司科技金融部',
            '证监会',
            '行政机关—国务院—商务部',
            '数据堂',
            '国家农业科学数据共享中心',
            '全国银行间同业拆借中心',
            '贵州省统计局',
            '工商局',
            '运维部',
            '行政机关—国务院—国家安全生产监管管理总局',
            '机构AAAA',
            '国家统计局',
            '外汇管理局',
            '质检总局',
            '行政机关—国务院—国家认监委',
            '行政机关—国务院—海关总']
    pages = ['1', '1', '1', '1', '1', '2', '1', '3', '20', '2', '13', '2', '1',
             '2', '26', '4', '4', '1', '46', '1', '1', '1', '1', '2', '1', '1', '2', '1']
    url_base = 'http://www.datagy.cn/list.jsp?'
    for i in xrange(len(orgs)):
        page = int(pages[i]) / 10 + 1
        org = orgs[i]
        url = url_base + "pageno=" + str(page) + 'org=' + org
        r = requests.post(url).text.encode('utf-8')
        ids = get_ids(r)
        if data_id in ids:
            orgnization = org
            break
    return orgnization


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
        sql = "insert into guiyang(data_id, title, descr,\
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

url_base = 'http://www.datagy.cn/'
data_ids = []
error_buf = []
for i in xrange(15):
    url = url_base + 'list.jsp?pageno=' + str(i + 1)
    r = requests.post(url).text.encode('utf-8')
    data_ids.extend(get_ids(r))
count = 0
for data_id in data_ids:
    count += 1
    url = url_base + 'detail.jsp?dataid=' + data_id
    r = requests.post(url).text.encode('utf-8')
    category = get_category(r)
    title = get_title(r)
    desc = get_desc(r)
    tag = get_tag(r)
    orgnization = get_organization(data_id)
    num_of_download = get_downloads(r)
    updated_date = updates_visits(r)[0]
    format = get_format(r)[0]
    publication_date = ''
    update_frequency = ''
    update_on_time = 'future check'
    publication_type = ''
    num_of_files = get_format(r)[1]
    num_of_visits = updates_visits(r)[1]
    if not upload_data(data_id, title, desc,
                       tag, category, orgnization,
                       num_of_download, updated_date, format,
                       publication_date, update_frequency, update_on_time,
                       '', '', num_of_files, num_of_visits):
        print "insert error!"
        error_buf.append(url)
for error_url in error_buf:
    print error_url
