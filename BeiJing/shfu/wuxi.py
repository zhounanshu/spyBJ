#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import requests
import json
import MySQLdb


def delete_white(arg):
    pattern = re.compile('\s+')
    new_str = re.sub(pattern, '', arg)
    return new_str


def get_href(arg):
    pattern = re.compile(r'href="(.*)">')
    temp = re.findall(pattern, arg)
    return temp


def all_orgs(arg):
    pattern = re.compile(r'">(.*)</a>')
    temp = re.findall(pattern, arg)
    result = []
    for t in temp:
        pattern = re.compile(r'">(.*)')
        buf = re.findall(pattern, t)
        result.extend(buf)
    return result


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
        sql = "insert into wuxi(data_id, title, descr,\
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

reg = r'<div class="ziy_mulu">(.*?)</div>'
pattern = re.compile(reg, re.S)
r = requests.post(
    'http://opendata.wuxi.gov.cn/fzlm/zymllby/index.shtml').text.encode('utf-8')
temp = re.findall(pattern, r)
urls = []
orgs = []
error_buf = []
for i in range(len(temp)):
    buf = ''
    if temp[i] != '':
        buf = get_href(temp[i])
    urls.extend(buf)
    orgs.extend(all_orgs(temp[i]))
hrefs = []
orgs[-1] = '食药监局'
url_base = 'http://opendata.wuxi.gov.cn/intertidwebapp/opendata/data'
url_list = 'http://opendata.wuxi.gov.cn/intertidwebapp/opendata/listcount'
for org in orgs:
    payload = {'fbjg': org, 'pageIndex': 1}
    r = json.loads(
        requests.post(url_base, payload).text.encode('utf-8'))
    totalCount = r['totalCount']
    payload = {'fbjg': org, 'pageIndex': 1, 'pageSize': totalCount}
    r = requests.post(url_base, payload).text.encode('utf-8')
    datas = json.loads(r)['list']
    for data in datas:
        data_id = data['id']
        title = data['title']
        updated_date = data['writeTime']
        attriBute = json.loads(data['attriBute'])
        if attriBute.has_key('WJGS'):
            format = attriBute['WJGS']
        else:
            format = ''
        if attriBute.has_key('FILE_UPLOAD'):
            file_name = attriBute['FILE_UPLOAD']
        else:
            file_name = ''
        num_of_files = ''
        if format != '':
            num_of_visits = 1
        if format == '':
            if attriBute.has_key('WBZY'):
                f_n = attriBute['WBZY']
            else:
                f_n = ''
            file_name = f_n
            if file_name != '':
                format = 'html'
        if attriBute.has_key('FBJG'):
            o_a = attriBute['FBJG']
        else:
            o_a = ''
        if attriBute.has_key('SJTGFDW'):
            o_b = attriBute['SJTGFDW']
        else:
            o_b = ''
        orgnization = o_a + '|' + o_b
        if attriBute.has_key('FBRQ'):
            p_d = attriBute['FBRQ']
        else:
            p_d = ''
        publication_date = p_d
        if attriBute.has_key('ZTFL'):
            c_a = attriBute['ZTFL']
        else:
            c_a = ''
        if attriBute.has_key('ZTFL_A'):
            c_b = attriBute['ZTFL_A']
        else:
            c_b = ''
        if attriBute.has_key('ZTFL_R'):
            c_c = attriBute['ZTFL_R']
        else:
            c_c = ''
        category = c_a + ' ' + c_b + ' ' + c_c
        if attriBute.has_key('GXPD'):
            u_f = attriBute['GXPD']
        else:
            u_f = ''
        update_frequency = u_f
        if attriBute.has_key('GJC'):
            tg = attriBute['GJC']
        else:
            tg = ''
        tag = tg
        payload = {'contentId': data_id, 'siteId': 105}
        r = json.loads(
            requests.post(url_list, payload).text.encode('utf-8'))
        if len(r) == 0:
            num_of_visits = 0
        else:
            num_of_visits = r[0]['click']
        desc = ''
        num_of_download = ''
        update_on_time = ''
        if not upload_data(data_id, title, desc,
                           tag, category, orgnization,
                           num_of_download, updated_date, format,
                           publication_date, update_frequency, update_on_time,
                           '', '', num_of_files, num_of_visits, file_name):
            print "insert error!"
