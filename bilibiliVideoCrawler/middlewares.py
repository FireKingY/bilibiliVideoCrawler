# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import logging
import time
import random


class BilibilivideocrawlerSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class RandProxy(object):
    def process_request(self, request, spider):
        proxy = spider.proxy_pool.rand_proxy()
        if proxy is not None:
            proxy = str(proxy[0]) + ':' + str(proxy[1])
        else:
            time.sleep(random.randint(0, 4) + 4)
        logging.debug('using proxy: %s' % proxy)
        request.meta['proxy'] = proxy


class RandUA(object):
    def __init__(self, ua_list):
        self.ua_list = ua_list

    @classmethod
    def from_crawler(cls, crawler):
        ua = crawler.settings['USER_AGENT_LIST']
        return cls(ua)

    def process_request(self, request, spider):
        if self.ua_list:
            ua = random.choice(self.ua_list)
            logging.debug('using UA:%s' % ua)
            request.headers.setdefault(b'User-Agent', ua)
