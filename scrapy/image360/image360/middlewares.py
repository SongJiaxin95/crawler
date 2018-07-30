# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import re

from scrapy import signals
from selenium import webdriver
from scrapy.http import HtmlResponse

class Image360SpiderMiddleware(object):
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


class Image360DownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request 下载器
        # - or return a Response object 到spider
        # - or return a Request object 到调度器，把新任务添加到任务列表
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        # request.meta['proxy'] =
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class TaobaoDownloaderMiddleWare(object):
    def __init__(self, timeout):
        self.timeout = timeout
        # ccproxy / tinyproxy  / spuid
        # 快代理 / 讯代理 / 阿布云代理
        # 代理池 - 管理和维护一系列的代理并每次提供随机的代理
        chrome_opt = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images":2}
        # chrome_opt.add_argument('--proxy-server=http://uid:pwd@:')
        chrome_opt.add_experimental_option("prefs", prefs)

        self.brower = webdriver.Chrome(executable_path='C://chromedriver.exe',options=chrome_opt)
        self.brower.set_window_size(1000, 600)
        self.brower.set_page_load_timeout(self.timeout)

    def __del__(self):
        self.brower.close()

    def process_request(self, request, spider):
        referer = request.url
        if referer:
            request.headers['referer'] = referer
        if re.match(r'https://s.taobao.com/search?',request.url):
            try:
                self.brower.get(request.url)
                body = self.brower.page_source
                return HtmlResponse(url=request.url, body=body, encoding="utf-8", request=request,status=200)
            except TimeoutError:
                return HtmlResponse(url=request.url,status=500,request=request)

    def process_response(self, request, response, spider):

        return response

    def process_exception(self, request, exception, spider):
        pass


    @classmethod
    def from_crawler(cls, crawler):
        # 依赖注入 - craler - 通过该对象可以操作整个项目
        return cls(timeout=10)