# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging


class VideoPipeline(object):
    def process_item(self, item, spider):
        if item['view'] is '--':
            item['view'] = 0
        logging.debug('passed pipeline')
        return item

    def close_spider(self, spider):
        spider.proxy_pool.terminate()
