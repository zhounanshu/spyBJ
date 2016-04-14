# -*- coding: utf-8 -*-
import scrapy
import json
import re
from ..items import HaishuItem
import urllib2


class SpiderSpider(scrapy.Spider):
    name = "spider"
    allowed_domains = ["data.haishu.gov.cn"]
    start_urls = (
        'http://data.haishu.gov.cn/webContent_ajaxcatalogDetails?catalog_id=-1',
    )
    relationURL = ''
    relation_id = ''
    category = ''

    def parse(self, response):
        baseURL = 'http://data.haishu.gov.cn/webContent_ajaxcatalogDetails?catalog_id='
        for ele in json.loads(response.body)["listdata2"]:
            pageURL = baseURL + ele['UUID']
            request =  scrapy.Request(pageURL, callback=self.parse_dir_contents, meta={'item': ele['CATALOG_NAME']})
            yield request


    def parse_dir_contents(self, response):
        baseURL = 'http://data.haishu.gov.cn/hs_main4.action?&easy=yes&catalog_id=zyml&catalog_id2=mljg&relation_id='
        chgURL = 'http://data.haishu.gov.cn/webContent_ajaxcatalogDetails?catalog_id='
        URLs = []
        for ele in json.loads(response.body)['listdata2']:
            if ele.has_key('RELATION_ID'):
                self.relationURL = baseURL + ele['RELATION_ID']
                URLs.append(self.relationURL)
            else:
                request = urllib2.Request(chgURL + ele['UUID'])
                request.add_header("User-Agent", 'Mozilla 5.10')
                dLists = json.loads(
                    urllib2.urlopen(request).read())['listdata2']
                for ele in dLists:
                    self.relationURL = baseURL + ele['RELATION_ID']
                    URLs.append(self.relationURL)
        for URL in URLs:
            item = {}
            item['category'] = response.meta['item']
            item['data_id'] = URL.split('=')[-1]
            request = scrapy.Request(URL,
                                 callback=self.parse_articles_follow_next_page, meta={'item': item})
            yield request

    def noSpace(self, response, xpath):
        result = re.findall(r'\S+',
                            response.xpath(xpath).extract()[0])[0]
        return result

    def parse_articles_follow_next_page(self, response):
        item = HaishuItem()
        result = response.meta['item']
        item['data_id'] = result['data_id']
        item['category'] = result['category']
        if item['category'] is None:
            print item['data_id']
        item['title'] = self.noSpace(response,
                                          '/html/body/table/tr[2]/td/table[2]/tr/td/table[3]/tr/td[2]/table[1]/tr/td/text()')
        item['descr'] = self.noSpace(response,
                                          '/html/body/table/tr[2]/td/table[2]/tr/td/table[3]/tr/td[2]/table[3]/tr/td[2]/table[2]/tr/td/table[2]/tr/td/text()')
        item['tag'] = self.noSpace(
            response, '/html/body/table/tr[2]/td/table[2]/tr/td/table[3]/tr/td[2]/table[3]/tr/td[1]/table[3]/tr/td/table/tr[2]/td[3]/text()')
        item['orgnization'] = self.noSpace(
            response, '/html/body/table/tr[2]/td/table[2]/tr/td/table[3]/tr/td[2]/table[3]/tr/td[1]/table[3]/tr/td/table/tr[1]/td[3]/text()')
        item['num_of_download'] = self.noSpace(
            response, '/html/body/table/tr[2]/td/table[2]/tr/td/table[3]/tr/td[2]/table[3]/tr/td[1]/table[1]/tr/td[2]/table[1]/tr[3]/td[2]/text()')
        item['num_of_visits'] = ''
        item['format'] = self.noSpace(response,
                                           '/html/body/table/tr[2]/td/table[2]/tr/td/table[3]/tr/td[2]/table[3]/tr/td[1]/table[1]/tr/td[2]/table[1]/tr[1]/td[2]/text()')
        item['publication_date'] = ''
        item['updated_date'] = self.noSpace(
            response, '/html/body/table/tr[2]/td/table[2]/tr/td/table[3]/tr/td[2]/table[3]/tr/td[1]/table[1]/tr/td[2]/table[1]/tr[4]/td[2]/text()')
        item['update_frequency'] = self.noSpace(
            response, '/html/body/table/tr[2]/td/table[2]/tr/td/table[3]/tr/td[2]/table[3]/tr/td[1]/table[3]/tr/td/table/tr[4]/td[3]/text()')
        item['publication_type'] = self.noSpace(
            response, '/html/body/table/tr[2]/td/table[2]/tr/td/table[3]/tr/td[2]/table[3]/tr/td[1]/table[3]/tr/td/table/tr[3]/td[3]/text()')
        item['update_on_time'] = ''
        item['updated_on_time_value'] = ''
        item['num_of_files'] = '1'
        yield item

