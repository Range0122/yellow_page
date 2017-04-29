# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs


class YellowPagePipeline(object):
    # def __init__(self):
    #     self.file = codecs.open('name_list.txt', 'a', encoding='utf-8')
    #     # self.file = codecs.open('url_list.txt', 'a', encoding='utf-8')
    #     self.file.truncate()
    #     self.file.close()

    def process_item(self, item, spider):
        # with codecs.open('name_list.txt', 'a', encoding='utf-8') as f:
        #     for name in item['name']:
        #         f.write(str(name.text) + '\r')
        with codecs.open('url_list.txt', 'a', encoding='utf-8') as f:
            for url in item['url']:
                f.write(url + '\r')
