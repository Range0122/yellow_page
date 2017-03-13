# -*- coding:utf-8 -*-

import scrapy
from yellow_page.items import YellowPageItem
from scrapy.spiders import CrawlSpider
from lxml import etree
import math
import sys

reload(sys)
sys.setdefaultencoding('utf8')


class ZhSpider(CrawlSpider):
    name = 'yp_spider'
    start_urls = ['http://b2b.huangye88.com/qiye/']

    def parse(self, response):
        selector = etree.HTML(response.body)
        url_list_first = selector.xpath('//ul[@class="clearfix"]/li/a/@href')
        for url in url_list_first:
            requests = scrapy.Request(url, callback=self.parse_second)
            yield requests

    def parse_second(self, response):
        selector = etree.HTML(response.body)
        url_list_second = selector.xpath('//div[@class="main"]/div[1]/div[@class="ad_list"]/a/@href')
        for url in url_list_second:
            requests = scrapy.Request(url, callback=self.parse_third)
            yield requests

    def parse_third(self, response):
        selector = etree.HTML(response.body)
        url_list_third = selector.xpath('//ul[@class="cats_list qiyelist_cats_list"]/li/a/@href')

        n = selector.xpath('//div[@class="box"]/div[1]/span/em')[0].text
        if int(n) <= 20000:
            requests = scrapy.Request(response.url, callback=self.parse_pages)
            requests.meta['selector'] = selector
            yield requests
        elif url_list_third:
            for url in url_list_third:
                requests = scrapy.Request(url, callback=self.parse_forth)
                yield requests
        else:
            requests = scrapy.Request(response.url, callback=self.parse_pages)
            requests.meta['selector'] = selector
            yield requests

    def parse_forth(self, response):
        selector = etree.HTML(response.body)
        url_list_forth = selector.xpath('//ul[@class="cats_list qiyelist_cats_list"]/li/a/@href')
        if url_list_forth:
            for url in url_list_forth:
                requests = scrapy.Request(url, callback=self.parse_pages)
                yield requests

    def parse_pages(self, response):
        basic_url = response.url + 'pn'
        selector = etree.HTML(response.body)
        n = selector.xpath('//div[@class="box"]/div[1]/span/em')[0].text
        n = int(math.ceil(float(n)/20))
        for i in xrange(0, n):
            url = basic_url + str(n)
            requests = scrapy.Request(url, callback=self.parse_page)
            yield requests

    def parse_page(self, response):
        selector = etree.HTML(response.body)
        item = YellowPageItem()
        name = selector.xpath('//form[@id="jubao"]/dl/dt/h4/a')
        item['name'] = name
        yield item