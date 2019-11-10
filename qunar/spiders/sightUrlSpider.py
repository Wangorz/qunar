# -*- coding: utf-8 -*-
import scrapy
import re
import urllib.parse

from scrapy_redis.spiders import RedisSpider

from qunar.items import UrlItem

class SightUrlSpider(RedisSpider):

    """
    手动lpush城市链接到redis的list里面，start_url就是城市链接。
    框架自动取出城市链接，然后再发请求，把得到的小景点链接当做item交给管道处理
    self.redis_db.lpush(sight_url)
    """

    name = 'qunar'
    custom_settings = {
        'ITEM_PIPELINES': {'qunar.pipelines.SightUrlRedisPipeline': 300}
    }
    redis_key = 'qunar:start_urls'

    def parse(self, response):
        request_url = urllib.parse.unquote(response.url)
        pat = re.compile(r'([\u4e00-\u9fa5]+)')
        city = pat.findall(request_url)[0]
        # print(type(response))
        subject_list = response.xpath('//*[@id="subject-list"]/dd/a/span/text()').extract()
        for sub_item in subject_list:
            if '不限' in sub_item:
                continue
            else:
                subject = sub_item.split('(')[0]
            for page in range(1, 3):
                sub_url = 'https://piao.qunar.com/ticket/list.htm?keyword=' + city + '&region=&from=' \
                          'mpl_search_suggest&subject=' + subject + '&page=' + str(page) + '&sku='
            # print(sub_url)
                yield scrapy.Request(sub_url, meta={'subject': subject}, callback=self.parse_subject)

    def parse_subject(self, response):
        subject = response.meta['subject']
        sight_url_list = response.xpath('//*[@id="search-list"]/div/div/div[2]/h3/a/@href').extract()
        for url in sight_url_list:
            item = UrlItem()
            url = url.split('?')[0]
            sight_url = 'https://piao.qunar.com' + url + '?subject=' + subject
            item['url'] = sight_url
            # lpush存入景点url
            yield item










