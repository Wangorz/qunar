# -*- coding: utf-8 -*-
import scrapy
import re
import urllib.parse

from scrapy_redis.spiders import RedisSpider

from qunar.items import UrlItem

class SightUrlSpider(RedisSpider):

    name = 'qunar'
    custom_settings = {
        'ITEM_PIPELINES': {'qunar.pipelines.SightUrlRedisPipeline': 300}
    }
    redis_key = 'qunar:start_urls'

    def parse(self, response):
        request_url = urllib.parse.unquote(response.url)
        prefix = request_url.split('&subject=')[0]
        subject_list = response.xpath('//*[@id="subject-list"]/dd/a/span/text()').extract()
        for sub_item in subject_list:
            if '不限' in sub_item:
                continue
            else:
                subject = sub_item.split('(')[0]
                pageNum = int(int(sub_item.split('(')[1][:-1])/15) + 1
            for page in range(1, pageNum+1):
                sub_url = prefix + '&subject=' + subject + '&page=' + str(page)
                yield scrapy.Request(sub_url, meta={'subject': subject}, callback=self.parse_subject)

    def parse_subject(self, response):
        # request_url = urllib.parse.unquote(response.url)
        subject = response.meta['subject']
        sight_url_list = response.xpath('//*[@id="search-list"]/div/div/div[2]/h3/a/@href').extract()
        for url in sight_url_list:
            item = UrlItem()
            url = url.split('?')[0]
            sight_url = 'https://piao.qunar.com' + url + '?subject=' + subject
            item['url'] = sight_url
            # print(request_url.split('ect=')[1] + " -> " + sight_url)
            # lpush存入景点url
            yield item










