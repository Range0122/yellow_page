# -*- coding:utf-8 -*-

import scrapy
import codecs
from yellow_page.items import YellowPageItem
from scrapy.spiders import CrawlSpider
import re
import sys

reload(sys)
sys.setdefaultencoding('utf8')


class Page_Spider(CrawlSpider):
    name = 'page_spider'
    start_urls = ['http://b2b.huangye88.com']

    def parse(self, response):
        with codecs.open('url_test.txt', 'r', encoding='utf-8') as f:
            for line in f.readlines():
                item = YellowPageItem()
                item["name"] = []
                url = str(line.replace('\r', '').replace('\n', '').replace('=', ''))
                requests = scrapy.Request(url, meta={"item": item}, callback=self.parse_page)
                yield requests

    def parse_page(self, response):
        item = response.meta["item"]
        name = response.selector.xpath('//form[@id="jubao"]/dl/dt/h4/a/text()').extract()
        name = item["name"] + name
        item["name"] = name
        next_url = re.findall(r'<a href=\"([a-zA-z]+://[^\s]*)\">下一页', response.body)
        if len(next_url) > 0:
            request = scrapy.Request(url=next_url[0], meta={"item": item}, callback=self.parse_page)
            yield request
        else:
            yield item
