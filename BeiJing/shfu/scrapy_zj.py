#!/usr/bin/env pyhton
# -*- coding: utf-8 -*-
import re
import urllib2
import requests
import datetime
import MySQLdb


def getHtml(url):
    page = urllib2.urlopen(url)
    html = page.read()
    return html


def totalPages(html):
    # 获取numPerPage
    numPerPage_reg = r'name="numPerPage" value="(.*)"'
    numPerPage_re = re.compile(numPerPage_reg)
    numPerPage = re.findall(numPerPage_re, html)
    # 获取total page
    pages_reg = r'id="total"  value="(.*)"'
    pages_re = re.compile(pages_reg)
    pages = re.findall(pages_re, html)
    if len(numPerPage) != 1 and len(pages) != 1:
        print "get totalPages wrong......"
    return int(numPerPage[0]) * int(pages[0])


def data_herfs(html):
    herfs = None
    herf_reg = r'href=\'(.*)\'\"'
    herf_re = re.compile(herf_reg)
    herfs = re.findall(herf_re, html)
    return herfs


def get_format(f):
    if '.' in f and f.rsplit('.', 1)[1]:
        return '.' in f and f.rsplit('.', 1)[1]
    else:
        return ''


def paser(html):
    # 文件名
    file_reg = r'class="cy666" title="(.*)"'
    file_re = re.compile(file_reg)
    file_names = re.findall(file_re, html)
    # 下载次数
    downloads_reg = r'下载次数：(.*)<'
    downloads_re = re.compile(downloads_reg)
    downloads = re.findall(downloads_re, html)
    # 更新时间
    update_reg = r'上传时间：(.*)<'
    update_re = re.compile(update_reg)
    updates = re.findall(update_re, html)
    # title
    title_reg = r'wftop2lftop1_2 sj18">(.*)<'
    title_re = re.compile(title_reg)
    title = re.findall(title_re, html)
    # 获取desc, tag, orgnization, publication date, update frequency
    mi_reg = r'wftop2lftop3_2 sjjk12">(.*?)<'
    mi_re = re.compile(mi_reg, re.S)
    mi = re.findall(mi_re, html)
    mix = []
    for m in mi:
        if m is not None:
            reg = re.compile('\s+')
            new_string = re.sub(reg, '', m)
            mix.append(new_string)
    key_reg = r'wftop2lftop3_1 sj14">(.*)：<'
    key_re = re.compile(key_reg)
    keys = re.findall(key_re, html)
    temp = dict(zip(keys, mix))
    result = []
    if len(file_names) != 0:
        buf = {}
        for i in range(len(file_names)):
            buf['file_name'] = str(file_names[i])
            buf['desc'] = temp['资源摘要']
            if temp.has_key('关键字'):
                buf['tag'] = temp['关键字']
            else:
                buf['tag'] = ''
            buf['publication_date'] = temp['信息资源发布日期']
            buf['orgnization'] = '浙江' + temp['信息资源提供方']
            if temp.has_key('更新频率'):
                buf['update_freq'] = temp['更新频率'].split('&')[0]
            else:
                buf['update_freq'] = ''
            buf['file_format'] = get_format(file_names[i])
            buf['downloads'] = downloads[i]
            buf['update_date'] = updates[i][:4] + '-' + \
                updates[i][4: 6] + '-' + updates[i][6:]
            buf['title'] = title[0]
            buf['num_of_files'] = '1'
            result.append(buf)
    else:
        buf = {}
        file_name_reg = r'href="(.*)">http:'
        file_name_re = re.compile(file_name_reg)
        file_name = re.findall(file_name_re, html)
        buf['file_name'] = str(file_name)
        buf['desc'] = temp['资源摘要']
        if temp.has_key('关键字'):
            buf['tag'] = temp['关键字']
        else:
            buf['tag'] = ''
        buf['publication_date'] = temp['信息资源发布日期']
        buf['orgnization'] = '浙江' + temp['信息资源提供方']
        if temp.has_key('更新频率'):
            buf['update_freq'] = temp['更新频率'].split('&')[0]
        else:
            buf['update_freq'] = ''
        buf['file_format'] = get_format(file_name)
        buf['downloads'] = None
        buf['update_date'] = None
        buf['title'] = title[0]
        buf['num_of_files'] = None
        result.append(buf)
    return result


def get_id(html):
    id_reg = r'resid=(.*)&'
    id_re = re.compile(id_reg)
    id = re.findall(id_re, html)
    if len(id) == 0:
        print "no data id....."
    return id[0]


def get_category(html):
    category_reg = r'resid=(.*)&'
    category_re = re.compile(category_reg)
    category = re.findall(category_re, html)
    if len(category) == 0:
        print "no data id....."
    return category[0]


def update_ontime(time, publish):
    now = datetime.datetime.now().strftime("%y-%m-%d")
    if time == now:
        return 'yes'
    else:
        if time == publish:
            return 'no'
        else:
            return 'future check'


def upload_data(data_id, title, desc,
                tag, category, orgnization,
                num_of_download, updated_date, format,
                publication_date, update_frequency, update_on_time,
                updated_on_time_value, publication_type,
                num_of_files, num_of_visits, file_name):
    try:
        conn = MySQLdb.connect(host='localhost',
                               port=3306,
                               user='root',
                               passwd='marvinzns',
                               db='shfd',
                               charset='utf8')
        cur = conn.cursor()
        sql = "insert into zhejiang_api(data_id, title, descr,\
                    tag, category, orgnization, \
                    num_of_download, updated_date, format, \
                    publication_date,update_frequency,update_on_time, \
                    updated_on_time_value, publication_type,\
                    num_of_files, num_of_visits, file_name) values(%s, %s,%s,\
                    %s, %s,%s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s)"
        param = (data_id, title, desc,
                 tag, category, orgnization,
                 num_of_download, updated_date, format,
                 publication_date, update_frequency,
                 update_on_time, updated_on_time_value,
                 publication_type, num_of_files, num_of_visits,
                 file_name)
        cur.execute(sql, param)
        conn.commit()
        cur.close()
        conn.close()
        return True
    except:
        return False

catecodes = ['SJLY001', 'SJLY002', 'SJLY003', 'SJLY004', 'SJLY005',
             'SJLY006', 'SJLY007', 'SJLY008', 'SJLY009', 'SJLY010']
categories = ['经济建设', '社会发展', '资源环境', '城市建设',
              '文化休闲', '教育科技', '卫生健康', '民生服务', '道路交通', '机构团体']
hrefs = []
for catecode in catecodes:
    # 进入分类目录
    payload = {'catecode': catecode}
    headers = {'User-Agent': 'Mozilla/5.1'}
    r = requests.post(
        "http://data.zjzwfw.gov.cn/toCate.action", data=payload, headers=headers)
    numPerPage = totalPages(r.text.encode('utf-8'))
    # 获取总的数据集个数
    if numPerPage is not None:
        print "the page num is " + str(numPerPage)
        # 获取单个数据集页面url
        payload = {
            'catecode': catecode, 'pageNum': '1', 'numPerPage': numPerPage}
        r = requests.post(
            "http://data.zjzwfw.gov.cn/toCate.action", data=payload)
        hrefs.extend(data_herfs(r.text.encode('utf-8')))
# 获取关键参数
url_base = 'http://data.zjzwfw.gov.cn/'
# url_base = 'http://data.zjzwfw.gov.cn/interfacelist.action'
pageURL = 'http://data.zjzwfw.gov.cn/interfacelist.action?deptName=&frontcode=&pageNum=1&numPerPage=160'
hrefs = data_herfs(requests.post(pageURL).text.encode('utf-8'))
i = 0
error_buf = []
for href in hrefs:
    url = url_base + href
    data_id = get_id(url)
    category = categories[int(url[-3:]) - 1]
    r = requests.post(url).text.encode('utf-8')
    data_list = paser(r)
    for k in data_list:
        i += 1
        desc = k['desc']
        tag = k['tag']
        title = k['title']
        orgnization = k['orgnization']
        num_of_download = k['downloads']
        updated_date = k['update_date']
        format = k['file_format']
        publication_date = k['publication_date']
        update_frequency = k['update_freq']
        update_on_time = update_ontime(k['update_date'], k['publication_date'])
        num_of_files = k['num_of_files']
        file_name = k['file_name']
        print k
        if not upload_data(data_id, title, desc,
                           tag, category, orgnization,
                           num_of_download, updated_date, format,
                           publication_date, update_frequency, update_on_time,
                           '', '', num_of_files, '', file_name):
            print "insert error!"
            error_buf.append(url)
for error_url in error_buf:
    print error_url
