# -*- coding: utf-8 -*-
import scrapy
from ..items import NanhaiItem
import re

class NanhaiSpider(scrapy.Spider):
    name = "nanhai"
    allowed_domains = ["data.nanhai.gov.cn"]
    start_urls = (
        'http://data.nanhai.gov.cn/cms/sites/sjzy/folder.jsp',
    )
    item = NanhaiItem()

    def parse(self, response):
        baseURL = "http://data.nanhai.gov.cn/cms/sites/sjzy/load_sj_theme.jsp?tid=all&page="
        for i in xrange(1, 19):
            pageURL = baseURL + str(i)
            yield scrapy.Request(pageURL, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        # //*[@id="my_table"]/tbody/tr[2]/td[1]/a
        # //*[@id="my_table"]/tbody/tr[4]/td[1]/a
        for i in xrange(1, len(response.xpath('//*[@id="my_table"]').xpath('./tr'))):
            dataURL = response.xpath(
                '//*[@id="my_table"]').xpath('./tr[' + str(i + 1) + ']/td[1]/a/@href').extract()
            if len(dataURL) > 0:
                dataURL = response.urljoin(dataURL[0])
            else:
                continue
            self.item['data_id'] = dataURL.split('=')[-1]
            yield scrapy.Request(dataURL,
                                 callback=self.parse_articles_follow_next_page)

    def getDetail(self, response, xpath):
        temp = response.xpath(xpath).extract()
        if len(temp) > 0:
            temp = temp[0]
        else:
            temp = ''
        return temp

    def getTable(self, response, table, tr):
        temp = response.xpath(table).xpath(tr).extract()
        if len(temp) > 0:
            temp = temp[0]
        else:
            temp = ''
        return temp

    def parse_articles_follow_next_page(self, response):
        self.item['title'] = self.getDetail(response,
                                            '/html/body/div[3]/div[2]/div[1]/div[1]/span/text()')
        self.item['descr'] = self.getDetail(response,
                                            '/html/body/div[3]/div[2]/div[1]/div[4]/div[2]/text()')
        self.item['tag'] = self.getDetail(response,
                                          '//*[@id="infotable"]/tr[4]/td[2]/text()')
        self.item['category'] = self.getDetail(response,
            '//*[@id="infotable"]/tr[5]/td[2]/text()')
        self.item['orgnization'] = self.getDetail(response,
            '//*[@id="infotable"]/tr[1]/td[2]/text()')
        self.item['num_of_download'] = re.findall(r'\d+', self.getDetail(response,
            '//*[@id="infotable"]/tr[3]/td[2]/text()'))
        self.item['updated_date'] = self.getDetail(response,
            '//*[@id="infotable"]/tr[7]/td[2]/text()')
        self.item['format'] = self.getDetail(response,
            '//*[@id="infotable"]/tr[2]/td[2]/text()')
        self.item['publication_date'] = self.getDetail(response,
            '//*[@id="infotable"]/tr[6]/td[2]/text()')
        self.item['update_frequency'] = ''
        self.item['update_on_time'] = ''
        self.item['updated_on_time_value'] = ''
        self.item['publication_type'] = ''
        self.item['num_of_files'] = ''
        self.item['num_of_visits'] = ''
        yield self.item
