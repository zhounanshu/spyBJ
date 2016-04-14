# -*- coding: utf-8 -*-

# Scrapy settings for Haishu project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'Haishu'

SPIDER_MODULES = ['Haishu.spiders']
NEWSPIDER_MODULE = 'Haishu.spiders'
LOG_ENABLED = False

MYSQL_HOST = 'localhost'
MYSQL_DBNAME = 'shfd'
MYSQL_USER = 'root'
MYSQL_PASSWD = 'marvinzns'

ITEM_PIPELINES = {
    'Haishu.pipelines.MySQLPipeline': 300,
}
