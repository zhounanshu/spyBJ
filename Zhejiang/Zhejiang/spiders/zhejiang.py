# -*- coding: utf-8 -*-
import scrapy
import re
from ..items import ZhejiangItem


class ZhejiangSpider(scrapy.Spider):
    name = "zhejiang"
    allowed_domains = ["data.zjzwfw.gov.cn"]
    start_urls = (
        'http://data.zjzwfw.gov.cn/toCate.action',
    )

    def parse(self, response):
        cates = response.xpath('/html/body/div/div/div/div/div/a')
        for cate in cates:
            cateURL = response.urljoin(cate.xpath('./@href').extract()[0])
            category = cate.xpath('./div/text()').extract()[0]
            cateTemp = {}
            cateTemp['category'] = category
            cateTemp['catecode'] = cateURL.split('=')[-1]
            request = scrapy.Request(
                cateURL, callback=self.parse_dir_contents,
                meta={'item': cateTemp})
        cateTemp['category'] = 'api'
        cateURL = 'http://data.zjzwfw.gov.cn/interfacelist.action'
        request = scrapy.Request(
            cateURL, callback=self.parse_dir_contents,
            meta={'item': cateTemp})
        yield request

    def parse_dir_contents(self, response):
        # pageBase = 'http://data.zjzwfw.gov.cn/toCate.action?numPerPage=15&catecode='
        pageBase = 'http://data.zjzwfw.gov.cn/interfacelist.action?&numPerPage=15&pageNum='
        page = response.xpath('//*[@id="pagerForm"]/div/ul/li[6]').extract()
        if len(page) > 1:
            pageNums = len(page) - 1
        else:
            pageNums = len(page)
        for i in xrange(1, pageNums + 1):
            cateTemp = response.meta['item']
            # catecode = cateTemp['catecode']
            # pageURL = pageBase + catecode + '&pageNum=' + str(i)
            pageURL = pageBase + str(i)
            request = scrapy.Request(
                pageURL, callback=self.parse_data_pages,
                meta={'item': cateTemp['category']})
            yield request

    def parse_data_pages(self, response):
        baseURL = 'http://data.zjzwfw.gov.cn/'
        draftURLs = response.xpath('//*[@id="pagerForm"]/div/div[1]').extract()
        category = response.meta['item']
        for draftURL in draftURLs:
            dataURL = baseURL + re.findall(r'href=\'(.*?)\'', draftURL)[0]
            result = {}
            result['data_id'] = re.findall(r'resid=(.*?)&amp', dataURL)[0]
            result['category'] = category
            result['url'] = dataURL
            request = scrapy.Request(
                dataURL, callback=self.parse_articles_follow_next_page,
                meta={'item': result})
            yield request

    def get_format(self, f):
        if '.' in f and f.rsplit('.', 1)[1]:
            return '.' in f and f.rsplit('.', 1)[1]
        else:
            return ''

    def paser(self, html):
        # 文件名
        file_reg = r'class="cy666" title="(.*)"'
        file_re = re.compile(file_reg)
        file_names = re.findall(file_re, html)
        # 下载次数
        downloads_reg = r'下载次数：(.*)<'
        downloads_re = re.compile(downloads_reg)
        downloads = re.findall(downloads_re, html)
        # 更新时间
        update_reg = r'上传时间：(.*)<'
        update_re = re.compile(update_reg)
        updates = re.findall(update_re, html)
        # title
        title_reg = r'wftop2lftop1_2 sj18">(.*)<'
        title_re = re.compile(title_reg)
        title = re.findall(title_re, html)
        # 获取desc, tag, orgnization, publication date, update frequency
        mi_reg = r'wftop2lftop3_2 sjjk12">(.*?)<'
        mi_re = re.compile(mi_reg, re.S)
        mi = re.findall(mi_re, html)
        mix = []
        for m in mi:
            if m is not None:
                reg = re.compile('\s+')
                new_string = re.sub(reg, '', m)
                mix.append(new_string)
        key_reg = r'wftop2lftop3_1 sj14">(.*)：<'
        key_re = re.compile(key_reg)
        keys = re.findall(key_re, html)
        temp = dict(zip(keys, mix))
        result = []
        if len(file_names) != 0:
            buf = {}
            for i in range(len(file_names)):
                if (len(file_names[i])) > 0:
                    buf['file_name'] = file_names[i][0]
                else:
                    buf['file_name'] = file_names[i]
                buf['desc'] = temp['资源摘要']
                if temp.has_key('关键字'):
                    buf['tag'] = temp['关键字']
                else:
                    buf['tag'] = ''
                buf['publication_date'] = temp['信息资源发布日期']
                buf['orgnization'] = '浙江' + temp['信息资源提供方']
                if temp.has_key('更新频率'):
                    buf['update_freq'] = temp['更新频率'].split('&')[0]
                else:
                    buf['update_freq'] = ''
                buf['file_format'] = self.get_format(file_names[i])
                buf['downloads'] = downloads[i]
                buf['update_date'] = updates[i][:4] + '-' + \
                    updates[i][4: 6] + '-' + updates[i][6:]
                buf['title'] = title[0]
                buf['num_of_files'] = '1'
                result.append(buf)
        else:
            buf = {}
            file_name_reg = r'href="(.*)">http:'
            file_name_re = re.compile(file_name_reg)
            file_name = re.findall(file_name_re, html)
            buf['file_name'] = str(file_name)
            buf['desc'] = temp['资源摘要']
            if temp.has_key('关键字'):
                buf['tag'] = temp['关键字']
            else:
                buf['tag'] = ''
            buf['publication_date'] = temp['信息资源发布日期']
            buf['orgnization'] = '浙江' + temp['信息资源提供方']
            if temp.has_key('更新频率'):
                buf['update_freq'] = temp['更新频率'].split('&')[0]
            else:
                buf['update_freq'] = ''
            buf['file_format'] = self.get_format(file_name)
            buf['downloads'] = None
            buf['update_date'] = None
            buf['title'] = title[0]
            buf['num_of_files'] = None
            result.append(buf)
        return result

    def parse_articles_follow_next_page(self, response):
        item = ZhejiangItem()
        result = response.meta['item']
        item['data_id'] = result['data_id']
        item['category'] = result['category']
        ks = self.paser(response.body)
        for k in ks:
            item['title'] = k['title']
            item['descr'] = k['desc']
            item['tag'] = k['tag']
            item['orgnization'] = k['orgnization']
            item['num_of_download'] = k['downloads']
            item['num_of_visits'] = ''
            item['format'] = k['file_format']
            item['publication_date'] = k['publication_date']
            item['updated_date'] = k['update_date']
            item['update_frequency'] = k['update_freq']
            item['publication_type'] = ''
            item['update_on_time'] = ''
            item['updated_on_time_value'] = ''
            item['num_of_files'] = k['num_of_files']
            item['file_name'] = k['file_name']
            yield item
