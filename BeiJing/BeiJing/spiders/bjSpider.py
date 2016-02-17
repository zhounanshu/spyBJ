# -*- coding: utf-8 -*-
import scrapy
from ..items import BeijingItem


class BjspiderSpider(scrapy.Spider):
    name = "bjSpider"
    allowed_domains = ["www.bjdata.gov.cn"]
    start_urls = (
        'http://www.bjdata.gov.cn/zyml/azt/lyzs/zs/xjjd/index.htm',
    )

    def parse(self, response):
        hrefs = []
        for sel in response.xpath('//*[@id="ess_ctr473_contentpane"]/ul/li'):
            href = sel.xpath('.//ul/li/ul/li/a/@href').extract()
            hrefs.extend(href)
        for ele in hrefs:
            url = response.urljoin(ele)
            yield scrapy.Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        hrefs = []
        for sel in response.xpath('//*[@id="ess_ctr474_CategoriesList_DgdData_ctl02_HylName"]'):
            href = sel.xpath('@href').extract()
            hrefs.extend(href)
        for href in hrefs:
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.parse_articles_follow_next_page)

    def parse_articles_follow_next_page(self, response):
        item = BeijingItem()
        item['name'] = response.xpath('//*[@id="ess_ctr505_CategoriesDetailInfo_LblFileSize"]/text()').extract()[0]
        item['desc'] = response.xpath('//*[@id="ess_ctr505_CategoriesDetailInfo_LblDescription"]/text()').extract()[0]
        item['keyWords'] = response.xpath('//*[@id="ess_ctr505_CategoriesDetailInfo_LblKeywords"]/text()').extract()[0]
        item['date'] = response.xpath('//*[@id="ess_ctr505_CategoriesDetailInfo_LblUpdateTime"]/text()').extract()[0]
        yield item
