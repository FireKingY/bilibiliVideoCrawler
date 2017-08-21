#!/usr/bin/python3
# -*- coding: utf-8 -*-

import scrapy


class VideoItem(scrapy.Item):
    aid = scrapy.Field()
    view = scrapy.Field()
    danmaku = scrapy.Field()
    favorite = scrapy.Field()
    coin = scrapy.Field()
    share = scrapy.Field()
