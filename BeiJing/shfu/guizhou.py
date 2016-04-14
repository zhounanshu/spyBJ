#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
import MySQLdb


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

startURL = 'https://www.gzdata.com.cn/sj/'
host = 'https://www.gzdata.com.cn'
request = urllib2.Request(startURL)
request.add_header('User-Agent', 'Mozilla 5.10')
response = urllib2.urlopen(request).read()
soup = BeautifulSoup(response, 'lxml')
dataURL = soup.find_all(class_='li_bg01')
URLs = []
for URL in dataURL:
    URLs.append(startURL + URL.get('href')[1:])
temp = URLs[2: 4]
temp.append(URLs[5])
temp.append('https://www.gzdata.com.cn/sj/sjxz/list_1.html')
error_buf = []
for i in range(1):
    request = urllib2.Request(temp[i])
    request.add_header('User-Agent', 'Mozilla 5.10')
    response = urllib2.urlopen(request).read()
    soup = BeautifulSoup(response, 'lxml')
    titles = soup.select('body > div > div.erji_main > ul > li > a')
    source = soup.select(
        'body > div > div.erji_main > ul > li > span.art_from.doctext')
    upda_dates = soup.select(
        'body > div > div.erji_main > ul > li > span.time')
    for i in range(len(titles)):
        title = titles[i].get_text()
        file_name = titles[i].get('href')
        organization = source[i].get_text()
        upda_date = upda_dates.get_text()
        if not upload_data(data_id, title, desc,
                           tag, category, orgnization,
                           num_of_download, updated_date, format,
                           publication_date, update_frequency, update_on_time,
                           '', publication_type, num_of_files, num_of_visits):
            print "insert error!"
            error_buf.append(temp[i])
for error_url in error_buf:
    print error_url




