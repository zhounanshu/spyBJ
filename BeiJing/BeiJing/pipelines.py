# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
# import MySQLdb
# import MySQLdb.cursors
# from twisted.enterprise import adbapi
# from scrapy import log
# class BeijingPipeline(object):
#     def process_item(self, item, spider):
#         return item


class MongoPipeline(object):

    collection_name = 'scrapy_items'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert(dict(item))
        return item


# class MySQLStoreCnblogsPipeline(object):
#     def __init__(self, dbpool):
#         self.dbpool = dbpool

#     @classmethod
#     def from_settings(cls, settings):
#         dbargs = dict(
#             host=settings['MYSQL_HOST'],
#             db=settings['MYSQL_DBNAME'],
#             user=settings['MYSQL_USER'],
#             passwd=settings['MYSQL_PASSWD'],
#             charset='utf8',
#             cursorclass=MySQLdb.cursors.DictCursor,
#             use_unicode=True,
#         )
#         dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
#         return cls(dbpool)

#     # pipeline默认调用
#     def process_item(self, item, spider):
#         d = self.dbpool.runInteraction(self._do_upinsert, item, spider)
#         d.addErrback(self._handle_error, item, spider)
#         d.addBoth(lambda _: item)
#         return d
#     # 将每行更新或写入数据库中

#     def _do_upinsert(self, conn, item, spider):
#         conn.execute("""insert into beijing(data_id, title, descr,\
#                     tag, category, orgnization, \
#                     num_of_download, updated_date, format, \
#                     publication_date,update_frequency,update_on_time, \
#                     updated_on_time_value, publication_type,\
#                     num_of_files, num_of_visits) values(%s, %s,%s,\
#                     %s, %s,%s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s)""",
#                      (item['data_id'], item['title'], item['descr'],
#                       item['tag'], item['category'], item['orgnization'],
#                       item['num_of_download'], item['updated_date'],
#                       item['format'], item['publication_date'],
#                       item['update_frequency'], item['update_on_time'],
#                       item['updated_on_time_value'], item['publication_type'],
#                       item['num_of_files'], item['num_of_visits']))

#     def _handle_error(self, failure, item, spider):
#         log.err(failure)
