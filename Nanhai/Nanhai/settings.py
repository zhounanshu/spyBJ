# -*- coding: utf-8 -*-

# Scrapy settings for Nanhai project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'Nanhai'

SPIDER_MODULES = ['Nanhai.spiders']
NEWSPIDER_MODULE = 'Nanhai.spiders'
LOG_ENABLED = False

#    mysql configration
MYSQL_HOST = 'localhost'
MYSQL_DBNAME = 'shfd'
MYSQL_USER = 'root'
MYSQL_PASSWD = 'marvinzns'

ITEM_PIPELINES = {
    'Nanhai.pipelines.MySQLPipeline': 300,
}
