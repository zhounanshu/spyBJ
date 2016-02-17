# !/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import MySQLdb
import re
url_base = 'http://data.qingdao.gov.cn/data/gov/listView.htm?isWidget=true'


def delete_white(arg):
    pattern = re.compile('\s+')
    new_str = re.sub(pattern, '', arg)
    return new_str


def get_ids(html):
    reg = r'cata_id=(.*)" target="'
    pattern = re.compile(reg)
    ids = re.findall(pattern, html)
    return ids


def get_title(html):
    reg = r'detail_title">(.*)<'
    pattern = re.compile(reg)
    title = re.findall(pattern, html)[0]
    return title


def get_desc(html):
    reg = r'<span style="float: left;">(.*?)</span>'
    pattern = re.compile(reg, re.S)
    desc = re.findall(pattern, html)[0]
    return delete_white(desc)


def get_updates(html):
    reg = r'上次更新于(.*)<'
    pattern = re.compile(reg)
    updates = re.findall(pattern, html)[0]
    return updates


def get_format(html):
    reg = r'value="(.*)&nbsp'
    pattern = re.compile(reg)
    bufs = re.findall(pattern, html)
    temp = ''
    for buf in bufs:
        if buf is not None:
            reg1 = r'>&nbsp;(.*)'
            pattern = re.compile(reg1)
            updates = re.findall(pattern, buf)
            if len(updates) != 0:
                temp += updates[0]
                temp += ','
    return temp[:-1]

# list_cataview


def get_visits(html):
    reg = r'detail_cont">(.*)次访问</span>'
    pattern = re.compile(reg)
    temp = re.findall(pattern, html)
    return temp[0]


def get_downloads(html):
    reg = r'detail_cont">(.*)次下载</span>'
    pattern = re.compile(reg)
    temp = re.findall(pattern, html)
    return temp[0]
# 主题，部门


def categoty_org(html):
    reg = r'_blank">(.*)</a>'
    pattern = re.compile(reg)
    temp = re.findall(pattern, html)
    return temp


def get_tag(html):
    reg = r'stepCatalog\(\'(.*)\'\)"'
    pattern = re.compile(reg)
    temp = re.findall(pattern, html)
    result = ''
    if len(temp) != 0:
        result = temp[0]
    return result


def get_publish(html):
    reg = r'发布时间：</span>(.*)</span>'
    pattern = re.compile(reg)
    temp = re.findall(pattern, html)
    time = ''
    if len(temp) != 0:
        reg = r'>(.*)'
        pattern = re.compile(reg)
        time = re.findall(pattern, temp[0])
    return time


def get_freq(html):
    reg = r'更新周期：</span>(.*)</span>'
    pattern = re.compile(reg)
    temp = re.findall(pattern, html)
    time = ''
    if len(temp) != 0:
        reg = r'>(.*)'
        pattern = re.compile(reg)
        time = re.findall(pattern, temp[0])
    return time


def get_num_files(html):
    reg = r'class="button ">原始(.*)</a>'
    pattern = re.compile(reg)
    temp = re.findall(pattern, html)
    num = 1
    replace_format = ''
    if len(temp) != 0:
        reg = r'file_type_p(.*)</p>'
        pattern = re.compile(reg)
        temp = re.findall(pattern, html)
        buf = []
        for t in temp:
            pattern = re.compile(r'>(.*)')
            buf.extend(re.findall(pattern, t))
        replace_format = buf[0].split('.')[-1]
        num = len(buf)
    return num, replace_format


def get_cata_url(html):
    reg = r'list_cataview\', \'(.*)\'\)'
    pattern = re.compile(reg)
    temp = re.findall(pattern, html)
    return temp[0]


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
        sql = "insert into qingdao(data_id, title, descr,\
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

data_ids = []
error_buf = []
for i in xrange(1, 37):
    payload = {}
    index = i
    pagesize = 9
    count = 324
    payload = {'index': index, 'count': count, 'pagesize': payload}
    r = requests.post(url_base, payload).text.encode('utf-8')
    ids = get_ids(r)
    data_ids.extend(ids)
data_ids = [data_ids[i * 2] for i in range(len(data_ids) / 2)]
for data_id in data_ids:
    url = 'http://data.qingdao.gov.cn/data/gov/detail.htm?cata_id=' + \
        str(data_id)
    r = requests.post(url).text.encode('utf-8')
    url1 = get_cata_url(r)
    r1 = requests.post(url1).text.encode('utf-8')
    title = get_title(r)
    desc = get_desc(r)
    print url1
    tag = get_tag(r1)
    category = categoty_org(r1)[0]
    orgnization = categoty_org(r1)[1]
    num_of_download = get_downloads(r1)
    updated_date = get_updates(r)
    format = get_format(r)
    if format == '':
        format = get_num_files(r)[1]
    publication_date = get_publish(r1)
    update_on_time = None
    updated_on_time_value = None
    publication_type = ''
    num = get_num_files(r)[0]
    num_of_visits = get_visits(r1)
    update_frequency = get_freq(r1)
    if not upload_data(data_id, title, desc,
                       tag, category, orgnization,
                       num_of_download, updated_date, format,
                       publication_date, update_frequency, update_on_time,
                       '', '', num, num_of_visits):
        print "insert error!"
        error_buf.append(url)
for error_url in error_buf:
    print error_url
# r = requests.post('http://data.qingdao.gov.cn/data/gov/detail.htm?cata_id=9580001').text.encode('utf-8')
# format = get_format(r)
# print format
# if format == '':
#     format = get_num_files(r)[1]
# print format
# if not upload_data('1', '1', '1' , '1','1', '1', '1' , '1','1', '1', '1' , '1','1', '1', '1' , '1'):
#     print "insert error!"
