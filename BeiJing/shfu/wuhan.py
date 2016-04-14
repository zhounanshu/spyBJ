#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import requests
import json
import MySQLdb


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
        sql = "insert into wuhan(data_id, title, descr,\
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


def getInfo(reg, arg):
    temp = re.findall(reg, arg)
    buf = ''
    for ele in temp:
        if ele != '':
            buf += ele + ','
    return buf[:-1]


base_url = 'http://www.wuhandata.gov.cn/whdata/resources_list.action?pageNum='
count = 0
for i in xrange(1, 50):
    url = base_url + str(i)
    items = json.loads(requests.post(url).text.encode('utf-8'))['list']
    result = {}
    for item in items:
        count += 1
        result['data_id'] = item['id']
        result['title'] = item['name']
        result['descr'] = item['description']
        result['tag'] = getInfo(
            r'KeyWords>(.*?)</KeyWords>', item['metadata'])
        result['category'] = getInfo(
            r'ResourceType>(.*?)</ResourceType>', item['metadata'])
        result['orgnization'] = getInfo(
            r'<OrganizationName>(.*?)</OrganizationName>', item['metadata'])
        result['num_of_download'] = 0
        result['updated_date'] = ''
        result['format'] = item['pathForDatabase'].split('.')[-1]
        if count == 695:
            result['format'] = 'html'
        result['publication_date'] = item['publicDate'][:10]
        result['update_frequency'] = ''
        result['update_on_time'] = ''
        result['updated_on_time_value'] = ''
        result['publication_type'] = '普通公开'
        result['num_of_files'] = '1'
        result['num_of_visits'] = item['visit']
        result['file_name'] = item['pathForDatabase']
        if not upload_data(result['data_id'], result['title'], result['descr'],
                           result['tag'], result['category'], result['orgnization'],
                           result['num_of_download'], result['updated_date'], result['format'],
                           result['publication_date'], result['update_frequency'], result['update_on_time'],
                           result['updated_on_time_value'] , result['publication_type'],
                           result['num_of_files'], result['num_of_visits'], result['file_name']):
            print "insert error: " + str(count)
        else:
            print count














