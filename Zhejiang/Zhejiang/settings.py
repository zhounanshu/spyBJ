# -*- coding: utf-8 -*-

# Scrapy settings for Zhejiang project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'Zhejiang'

SPIDER_MODULES = ['Zhejiang.spiders']
NEWSPIDER_MODULE = 'Zhejiang.spiders'
LOG_ENABLED = True

MYSQL_HOST = 'localhost'
MYSQL_DBNAME = 'shfd'
MYSQL_USER = 'root'
MYSQL_PASSWD = 'marvinzns'

ITEM_PIPELINES = {
    'Zhejiang.pipelines.MySQLPipeline': 300,
}
