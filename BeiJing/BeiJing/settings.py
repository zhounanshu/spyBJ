# -*- coding: utf-8 -*-

# Scrapy settings for BeiJing project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'BeiJing'

SPIDER_MODULES = ['BeiJing.spiders']
NEWSPIDER_MODULE = 'BeiJing.spiders'

#    mongodb configration
MONGO_URI = 'mongodb://localhost:27017'
MONGO_DATABASE = 'beijing'

#    mysql configration
MYSQL_HOST = 'localhost'
MYSQL_DBNAME = 'shfd'
MYSQL_USER = 'root'
MYSQL_PASSWD = 'marvinzns'

ITEM_PIPELINES = {
    # 'cnblogs.pipelines.JsonWithEncodingCnblogsPipeline': 300,
    # 'cnblogs.pipelines.MySQLStoreCnblogsPipeline': 300,
    'BeiJing.pipelines.MongoPipeline': 300,
}
