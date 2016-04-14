# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HaishuItem(scrapy.Item):
    # define the fields for your item here like:
    data_id = scrapy.Field()
    title = scrapy.Field()
    descr = scrapy.Field()
    tag = scrapy.Field()
    category = scrapy.Field()
    orgnization = scrapy.Field()
    num_of_download = scrapy.Field()
    updated_date = scrapy.Field()
    format = scrapy.Field()
    publication_date = scrapy.Field()
    update_frequency = scrapy.Field()
    update_on_time = scrapy.Field()
    updated_on_time_value = scrapy.Field()
    publication_type = scrapy.Field()
    num_of_files = scrapy.Field()
    num_of_visits = scrapy.Field()
    pass
