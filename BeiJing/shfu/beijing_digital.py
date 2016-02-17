#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib2

response = urllib2.urlopen('http://www.bjdata.gov.cn/zyml/dzwj/rjyxxfwy/index.htm')
html = response.read()
soup = BeautifulSoup(html)
for s in soup.find_all('option', text='htm'):
    print s['value']

