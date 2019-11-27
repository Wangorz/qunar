# -*- coding: utf-8 -*-
import re
import json
import traceback
import urllib

import scrapy
from scrapy_redis.spiders import RedisSpider

from qunar.items import SightItem

class SightInfoSpider(RedisSpider):

    """
    自动从redis_key中取出链接
    """

    name = 'sight_info'
    redis_key = 'qunar:sight_urls'
    custom_settings = {
        'ITEM_PIPELINES': {'qunar.pipelines.SightInfoMongodbPipeline': 301}
    }

    # https://piao.qunar.com/ticket/detail_454305700.html?subject=文化古迹
    # https://piao.qunar.com/ticket/detail_454305700.html?subject=城市观光


    def parse(self, response):
        request_url = urllib.parse.unquote(response.url)
        pat = re.compile(r'([\u4e00-\u9fa5]+)')
        subject = pat.findall(request_url)[0]
        flag = False
        item = SightItem()
        imgUrls = {}
        imgUrlList = []
        try:
            item['subject'] = subject
            item['name'] = response.xpath('/html/body/div[2]/div[2]/div[2]/div[1]/span[1]/@title').extract()[0]
            item['location'] = response.xpath('/html/body/div[2]/div[2]/div[2]/div[3]/span[3]/@title').extract()[0]
            item['description'] = response.xpath('/html/body/div[2]/div[2]/div[2]/div[2]/text()').extract()[0]
            item['introduction'] = response.xpath('//*[@id="mp-charact"]/div[1]/div[1]/div[1]/p/text()').extract()[0]
            item['point'] = response.xpath('//*[@id="mp-description-commentscore"]/span/text()').extract()[0]
            if len(response.xpath('/html/body/div[2]/div[2]/div[2]/div[1]/span[2]/text()').extract()) > 0:
                item['level'] = response.xpath('/html/body/div[2]/div[2]/div[2]/div[1]/span[2]/text()').extract()[0]
            else:
                item['level'] = ' '
            loc_details = response.xpath('/html/head/meta[4]/@content').extract()[0]
            split_item = re.split('[=;]', loc_details)
            item['province'] = split_item[1]
            item['city'] = split_item[3]
            item['coordinate'] = split_item[5]
            item['sightId'] = response.xpath('//*[@id="mp-tickets"]/@data-sightid').extract()[0]
            item['_id'] = response.xpath('//*[@id="mp-tickets"]/@data-sightid').extract()[0]
            comment_count = response.xpath('/html/body/div[2]/div[2]/div[2]/div[4]/span[4]/a/text()').extract()[0]
            item['heat'] = re.findall(r'(\d+)', comment_count)[0]
            imgUrlList += response.xpath('//*[@id="mp-slider-content"]/div/img/@src').extract()
            imgUrlList += response.xpath('//*[@class="mp-charact-event"]/div/img/@src').extract()
            for index, imgUrl in enumerate(imgUrlList):
                imgUrls[index] = imgUrl
                if index == 9:
                    break
            item['imgUrls'] = json.dumps(imgUrls)
            sightId = response.xpath('//*[@id="mp-tickets"]/@data-sightid').extract()[0]
            commentUrl = 'https://piao.qunar.com/ticket/detailLight/sightCommentList.json?sightId=' \
                         + sightId + '&index=1&page=1&pageSize=10&tagType=0'
            # item['comments'] = commentUrl
            flag = True
        except:
            traceback.print_exc()
        if flag:
            # print(item)
            # yield item
            yield scrapy.Request(commentUrl, meta={'item': item}, callback=self.parse_comment, dont_filter=True)

    def parse_comment(self, response):
        comments = {}
        item = response.meta['item']
        comment_content = json.loads(response.text)
        data = comment_content['data']
        commentList = data['commentList']
        # item['comments'] = commentList
        for index, comment in enumerate(commentList):
            comments[index] = comment
        item['comments'] = json.dumps(comments)
        yield item

