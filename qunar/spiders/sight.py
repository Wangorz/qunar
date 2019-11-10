# -*- coding: utf-8 -*-
import json
import re
import traceback
import scrapy
import urllib.parse
from qunar.items import SightItem

class ScenicSpider(scrapy.Spider):
    name = 'sight'
    allowed_domains = ['piao.qunar.com']
    start_url = 'https://piao.qunar.com'

    def __init__(self):
        self.city = '上海'
        self.url = 'https://piao.qunar.com/ticket/list.htm?keyword=' + self.city + '&region=' + self.city + '&from=mpshouye_hotcity'
        # 除了主页，后面的二级链接都可以用http

    def start_requests(self):
        yield scrapy.Request(self.url, callback=self.parse)

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
            sight_url = 'https://piao.qunar.com' + url
            # 景点url如果重复说明他是有多个类别的，这里运行他重复，设置dont_filter=True，下一层抓评论也要改。
            yield scrapy.Request(sight_url, meta={'subject': subject}, callback=self.parse_sight, dont_filter=True)

    def parse_sight(self, response):
        flag = False
        item = SightItem()
        imgUrls = {}
        imgUrlList = []


        try:
            item['subject'] = response.meta['subject']
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
            imgUrlList += response.xpath('//*[@id="mp-slider-content"]/div/img/@src').extract()
            imgUrlList += response.xpath('//*[@class="mp-charact-event"]/div/img/@src').extract()
            for index, imgUrl in enumerate(imgUrlList):
                imgUrls[index] = imgUrl
                if index == 9:
                    break
            item['imgUrls'] = json.dumps(imgUrls)

            sightId = response.xpath('//*[@id="mp-tickets"]/@data-sightid').extract()[0]
            commentUrl = 'https://piao.qunar.com/ticket/detailLight/sightCommentList.json?sightId='\
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


        # item['subject'] = response.meta['subject']
        # if len(response.xpath('/html/body/div[2]/div[2]/div[2]/div[1]/span[1]/@title').extract()) > 0:
        #     item['name'] = response.xpath('/html/body/div[2]/div[2]/div[2]/div[1]/span[1]/@title').extract()[0]
        #     flag = True
        # if len(response.xpath('/html/body/div[2]/div[2]/div[2]/div[3]/span[3]/@title').extract()) > 0:
        #     item['location'] = response.xpath('/html/body/div[2]/div[2]/div[2]/div[3]/span[3]/@title').extract()[0]
        # if len(response.xpath('/html/body/div[2]/div[2]/div[2]/div[1]/span[2]/text()').extract()) > 0:
        #     item['level'] = response.xpath('/html/body/div[2]/div[2]/div[2]/div[1]/span[2]/text()').extract()[0]
        # else:
        #     item['level'] = ' '
        # if len(response.xpath('/html/body/div[2]/div[2]/div[2]/div[2]/text()').extract()) > 0:
        #     item['description'] = response.xpath('/html/body/div[2]/div[2]/div[2]/div[2]/text()').extract()[0]
        # if len(response.xpath('//*[@id="mp-charact"]/div[1]/div[1]/div[1]/p/text()').extract()) > 0:
        #     item['introduction'] = response.xpath('//*[@id="mp-charact"]/div[1]/div[1]/div[1]/p/text()').extract()[0]
        # if len(response.xpath('//*[@id="mp-description-commentscore"]/span/text()').extract()) > 0:
        #     item['point'] = response.xpath('//*[@id="mp-description-commentscore"]/span/text()').extract()[0]
        # if len(response.xpath('/html/head/meta[4]/@content').extract()) > 0:
        #     loc_details = response.xpath('/html/head/meta[4]/@content').extract()[0]
        #     # print(loc_details)
        #     split_item = re.split('[=;]', loc_details)
        #     item['province'] = split_item[1]
        #     item['city'] = split_item[3]
        #     item['coordinate'] = split_item[5]
        # if len(response.xpath('//*[@id="mp-tickets"]/@data-sightid').extract()) > 0:
        #     item['sightId'] = response.xpath('//*[@id="mp-tickets"]/@data-sightid').extract()[0]
        # if len(response.xpath('//*[@id="mp-slider-content"]/div/img').extract()) > 0:
        #     imgUrlList += response.xpath('//*[@id="mp-slider-content"]/div/img/@src').extract()
        # if len(response.xpath('//*[@class="mp-charact-event"]/div/img').extract()) > 0:
        #     imgUrlList += response.xpath('//*[@class="mp-charact-event"]/div/img/@src').extract()
        # for index, imgUrl in enumerate(imgUrlList):
        #     imgUrls[index] = imgUrl
        # item['imgUrls'] = json.dumps(imgUrls)
        # sightId = response.xpath('//*[@id="mp-tickets"]/@data-sightid').extract()[0]
        # commentUrl = 'https://piao.qunar.com/ticket/detailLight/sightCommentList.json?sightId='\
        #              + sightId + '&index=1&page=1&pageSize=10&tagType=0'
        # item['comments'] = commentUrl