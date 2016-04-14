# -*- coding: utf-8 -*-
import scrapy
import re
from ..items import ShanghaiItem


class ShanghaiSpider(scrapy.Spider):
    name = "shanghai"
    allowed_domains = ["www.datashanghai.gov.cn"]
    start_urls = (
        'http://www.datashanghai.gov.cn/home!toHomePage.action',
    )
    item = ShanghaiItem()
    count = 0

    def parse(self, response):
        base_url = 'query!queryDataByField.action?currentPage='
        hrefs = []
        for i in xrange(1, 88):
            hrefs.append(base_url + str(i))
        for ele in hrefs:
            url = response.urljoin(ele)
            yield scrapy.Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        type_3 = "query!queryGdsInterfaceInfoById.action?dataId="
        tyep_4 = "query!queryMobileAppById.action?dataId="
        type_0 = "query!queryGdsDataInfoById.action?type="
        for i in range(len(response.xpath('//*[@id="content"]/dl/dt'))):
            sel = response.xpath('//*[@id="content"]/dl/dt[' +
                                 str(i + 1) + ']/a/@href').extract()[0]
            # query_param = sel.xpath('.//a/@href').extract()[0]
            data_id = re.findall(r"'(.*?)',", sel)[0]
            data_type = re.findall(r",'(.*?)'", sel)[0]
            if int(data_type) == 3:
                href = type_3 + data_id
            elif int(data_type) == 4:
                href = tyep_4 + data_id
            else:
                href = type_0 + data_type + "&dataId=" + data_id
            url = response.urljoin(href)
            update = response.xpath(
                '//*[@id="content"]/dl/dd[' + str(i + 1) +
                ']/span/text()').extract()[0]
            item = {}
            item['data_id'] = data_id
            item['data_type'] = data_type
            item['updated_date'] = '-'.join(re.findall(r'\d+', update))
            item['url'] = url
            request = scrapy.Request(url,
                                     callback=self.parse_articles_follow_next_page, meta={'item': item})
            yield request

    def noSpace(self, response, xpath):
        if len(response.xpath(xpath).extract()) > 0:
            result = re.findall(r'\S+',
                                response.xpath(xpath).extract()[0])[0]
        else:
            result = ''
        return result

    def parse_articles_follow_next_page(self, response):
        temp = response.meta['item']
        self.item['data_id'] = temp['data_id']
        self.data_type = temp['data_type']
        self.item['title'] = self.noSpace(response,
                                          '//*[@id="wrap"]/div/h2/text()')
        self.item['updated_date'] = temp['updated_date']
        if int(self.data_type) == 3:
            self.item['descr'] = self.noSpace(response,
                                              '//*[@id="wrap"]/div[1]/table[1]/tbody/tr[2]/td/text()')
            self.item['tag'] = self.noSpace(
                response, '//*[@id="wrap"]/div[1]/table[1]/tbody/tr[3]/td/text()')
            self.item['category'] = self.noSpace(
                response, '//*[@id="wrap"]/div[1]/table[1]/tbody/tr[4]/td/text()')
            # //*[@id="wrap"]/div/table/tbody/tr[4]/td

            self.item['orgnization'] = self.noSpace(
                response, '//*[@id="wrap"]/div[1]/table[1]/tbody/tr[8]/td/text()')
            self.item['num_of_download'] = re.findall(r'\S+', response.xpath(
                '//*[@id="wrap"]/div[1]/table[1]/tbody/tr[1]/td/text()').extract()[0])[-1]
            self.item['num_of_visits'] = re.findall(r'\S+', response.xpath(
                '//*[@id="wrap"]/div[1]/table[1]/tbody/tr[1]/td/text()').extract()[0])[0]
            self.item['format'] = self.noSpace(response,
                                               '//*[@id="wrap"]/div[1]/table[2]/tbody/tr[6]/td/em/a/span/text()')
            self.item['publication_date'] = ''
            self.item['update_frequency'] = ''
            self.item['publication_type'] = self.noSpace(
                response, '//*[@id="wrap"]/div[1]/table[1]/tbody/tr[6]/td/text()')
            self.item['update_on_time'] = ''
            self.item['updated_on_time_value'] = ''
            self.item['num_of_files'] = '1'
        elif int(self.data_type) == 4:
            self.item['descr'] = self.noSpace(
                response, '//*[@id="wrap"]/div/table/tbody/tr[5]/td/text()')
            self.item['num_of_download'] = re.findall(r'\S+', response.xpath(
                '//*[@id="wrap"]/div/table/tbody/tr[1]/td/text()').extract()[0])[-1]
            self.item['num_of_visits'] = re.findall(r'\S+', response.xpath(
                '//*[@id="wrap"]/div/table/tbody/tr[1]/td/text()').extract()[0])[0]
            self.item['format'] = self.noSpace(
                response, '//*[@id="s2"]/text()')
            temp = self.noSpace(
                response, '//*[@id="wrap"]/div/table/tbody/tr[2]/td/text()')
            self.item['publication_date'] = '-'.join(re.findall('\d+', temp))
            self.item['publication_type'] = "普通公开"
            self.item['update_on_time'] = ''
            self.item['updated_on_time_value'] = ''
            self.item['num_of_files'] = '1'
        else:
            self.item['descr'] = self.noSpace(
                response, '//*[@id="wrap"]/div/table/tbody/tr[2]/td/text()')
            self.item['tag'] = self.noSpace(
                response, '//*[@id="wrap"]/div/table/tbody/tr[3]/td/text()')
            self.item['category'] = self.noSpace(
                response, '//*[@id="wrap"]/div/table/tbody/tr[4]/td/text()')
            self.item['orgnization'] = self.noSpace(
                response, '//*[@id="wrap"]/div/table/tbody/tr[11]/td/text()')
            self.item['num_of_download'] = re.findall(r'\S+', response.xpath(
                '//*[@id="wrap"]/div/table/tbody/tr[1]/td/text()').extract()[0])[-1]
            self.item['num_of_visits'] = re.findall(r'\S+', response.xpath(
                '//*[@id="wrap"]/div/table/tbody/tr[1]/td/text()').extract()[0])[0]
            self.item['format'] = self.noSpace(
                response, '//*[@id="wrap"]/div/table/tbody/tr[13]/td/em/a/span/text()')
            self.item['publication_date'] = self.noSpace(
                response, '//*[@id="wrap"]/div/table/tbody/tr[9]/td/text()')
            self.item['update_frequency'] = self.noSpace(
                response, '//*[@id="wrap"]/div/table/tbody/tr[8]/td/text()')
            self.item['publication_type'] = self.noSpace(
                response, '//*[@id="wrap"]/div/table/tbody/tr[7]/td/text()')
            self.item['update_on_time'] = ''
            self.item['updated_on_time_value'] = ''
            self.item['num_of_files'] = '1'
        self.item['is_api_data'] = 1 if (int(self.data_type) == 3) else 0
        self.count += 1
        print str(self.count)
        yield self.item
