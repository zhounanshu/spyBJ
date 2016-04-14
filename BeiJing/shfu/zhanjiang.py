#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import MySQLdb
from bs4 import BeautifulSoup
import urllib2


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
        sql = "insert into zhanjiang(data_id, title, descr,\
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


def getNum(arg):
    temp = re.findall(r'(\d+)', arg)
    if len(temp) > 0:
        temp = temp[0]
    else:
        temp = ''
    return temp

base_url = 'http://data.zhanjiang.gov.cn/plus/list.php?tid='
host = 'http://data.zhanjiang.gov.cn/'
# 数据产品、数据应用、社会专栏、地理信息
url = base_url + str(2)
response = urllib2.urlopen(url)
html = response.read()
soup = BeautifulSoup(html, "lxml")
s = soup.find_all(id='pageSpan')[0]
soup = BeautifulSoup(str(s), "lxml")
hrefs = set()
for link in soup.find_all('a'):
    if link.get('href'):
        href = host + link.get('href')
        hrefs.add(href)
hrefs.add(
    'http://data.zhanjiang.gov.cn//plus/list.php?tid=2&TotalResult=29&PageNo=1')
hrefs.add('http://data.zhanjiang.gov.cn/plus/list.php?tid=3')
hrefs.add('http://data.zhanjiang.gov.cn/plus/list.php?tid=7')
socialURL = "http://data.zhanjiang.gov.cn/plus/list.php?tid=6"
error_buf = []
for href in hrefs:
    html = urllib2.urlopen(href).read()
    soup = BeautifulSoup(html, 'lxml')
    dataListCons = soup.find_all(class_="dataListCon")
    for dataListCon in dataListCons:
        soup = BeautifulSoup(str(dataListCon), 'lxml')
        s = soup.select('dl > dt > h5 > span')
        updated_date = s[5].get_text()
        category = s[3].get_text()
        s = soup.select('dl > dt > h4 > a')
        dataURL = host + s[0].get('href')
        data_id = dataURL.split('/')[-1].split('.')[0]
        dataPage = urllib2.urlopen(dataURL).read()
        soup = BeautifulSoup(dataPage, 'lxml')
        # get datatable
        dataTable = soup.find(class_='data')
        soup = BeautifulSoup(dataPage, 'lxml')
        title = re.findall(r'\S+', soup.find('caption').get_text())[0]
        details = soup.select('td')
        buf = []
        for detail in details:
            temp = ''
            if detail.script is not None:
                nums = urllib2.urlopen(host + detail.script.get('src')).read()
                temp = getNum(nums)
            else:
                if len(re.findall(r'\S+', detail.get_text())) > 0:
                    temp = re.findall(r'\S+', detail.get_text())[0]
                else:
                    temp = ''
            buf.append(temp)
        format = 'zip'
        desc = buf[1]
        tag = buf[2]
        num_of_visits = buf[3]
        num_of_download = buf[4]
        update_frequency = buf[5]
        publication_date = buf[6]
        orgnization = buf[7]
        publication_type = buf[11]
        if not upload_data(data_id, title, desc,
                           tag, category, orgnization,
                           num_of_download, updated_date, format,
                           publication_date, update_frequency, '',
                           '', publication_type, '1', num_of_visits):
            print "insert error!"
            error_buf.append(dataURL)


html = urllib2.urlopen(socialURL).read()
soup = BeautifulSoup(html, 'lxml')
dataListCons = soup.find_all(class_="dataListCon")
for dataListCon in dataListCons:
    soup = BeautifulSoup(str(dataListCon), 'lxml')
    s = soup.select('dl > dt > h5 > span')
    updated_date = s[3].get_text()
    category = ''
    s = soup.select('dl > dt > h4 > a')
    dataURL = host + s[0].get('href')
    data_id = dataURL.split('/')[-1].split('.')[0]
    dataPage = urllib2.urlopen(dataURL).read()
    soup = BeautifulSoup(dataPage, 'lxml')
    # get datatable
    dataTable = soup.find(class_='data')
    soup = BeautifulSoup(dataPage, 'lxml')
    title = re.findall(r'\S+', soup.find('caption').get_text())[0]
    details = soup.select('td')
    buf = []
    for detail in details:
        temp = ''
        if detail.script is not None:
            nums = urllib2.urlopen(host + detail.script.get('src')).read()
            temp = getNum(nums)
        else:
            if len(re.findall(r'\S+', detail.get_text())) > 0:
                temp = re.findall(r'\S+', detail.get_text())[0]
            else:
                temp = ''
        buf.append(temp)
    format = 'html'
    desc = buf[1]
    tag = buf[2]
    num_of_visits = buf[3]
    num_of_download = buf[4]
    update_frequency = buf[5]
    publication_date = buf[6]
    orgnization = buf[7]
    publication_type = '普通公开'
    if not upload_data(data_id, title, desc,
                       tag, category, orgnization,
                       num_of_download, updated_date, format,
                       publication_date, update_frequency, '',
                       '', publication_type, '1', num_of_visits):
        print "insert error!"
        error_buf.append(dataURL)

for error_url in error_buf:
    print error_url



