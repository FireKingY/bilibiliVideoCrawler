#!/usr/bin/python3
# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy import Request
from bilibiliVideoCrawler.items import VideoItem
import json
import logging


class VideoSpider(Spider):
    name = 'video'
    url = 'https://api.bilibili.com/x/web-interface/archive/stat?callback=jQuery172009960371419769554_1503303631466&aid='
    c_aid = 500000
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

    def start_requests(self):
        for i in range(0, 1):
            self.c_aid += 1
        yield Request(self.url + str(self.c_aid), headers=self.header)

    def parse(self, res):
        item = VideoItem()
        try:
            data = json.loads(res.body.decode('utf-8'))['data']
        except Exception as e:
            logging.error('Failed to parse, url:%s' % res.url)
            logging.error(res.body.decode('utf-8'))
            raise e
            return

        item['aid'] = data['aid']
        item['view'] = data['view']
        item['danmaku'] = data['danmaku']
        item['favorite'] = data['favorite']
        item['coin'] = data['coin']
        item['share'] = data['share']
        yield item
