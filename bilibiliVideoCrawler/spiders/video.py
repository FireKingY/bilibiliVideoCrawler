#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import logging
import threading

from scrapy import Request, Spider

from bilibiliVideoCrawler import proxyCrawler
from bilibiliVideoCrawler.items import VideoItem

logging.basicConfig(level=logging.DEBUG)


class VideoSpider(Spider):
    name = 'video'
    url = 'https://api.bilibili.com/x/web-interface/archive/stat?aid='
    c_aid = 123456
    header = {
        'Host':
        'api.bilibili.com',
        'Connection':
        'keep-alive',
        'User-Agent':
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Upgrade-Insecure-Requests':
        '1',
        'Accept':
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding':
        'gzip, deflate, br',
        'Accept-Language':
        'zh',
    }
    proxy_pool = proxyCrawler.proxyPool()
    auto_get = threading.Thread(
        target=proxy_pool.auto_get, name='auto_get thread')

    def __init__(self):
        self.auto_get.start()
        self.auto_get.join(5)

    def start_requests(self):
        for i in range(0, 5):
            self.c_aid += 1
            yield Request(
                self.url + str(self.c_aid),
                callback=self.parse,
                errback=self.errback,
                headers=self.header)

    def parse(self, res):
        item = VideoItem()
        try:
            data = json.loads(res.body.decode('utf-8'))['data']
        except Exception as e:
            logging.error('Failed to parse, url:%s' % res.url)
            logging.error(res.body.decode('utf-8'))
            return

        item['aid'] = data['aid']
        item['view'] = data['view']
        item['danmaku'] = data['danmaku']
        item['favorite'] = data['favorite']
        item['coin'] = data['coin']
        item['share'] = data['share']
        yield item

    def errback(self, err):
        logging.debug(
            'Failed to crawl page:%s' % err.request.url.split('=')[-1])
        yield Request(
            err.request.url,
            callback=self.parse,
            errback=self.errback,
            dont_filter=True,
            headers=self.header)
