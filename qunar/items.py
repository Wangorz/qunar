# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class QunarItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class SightItem(scrapy.Item):
    _id = scrapy.Field()                # mongodb
    sightId = scrapy.Field()            # 识别码
    province = scrapy.Field()		    # 省
    city = scrapy.Field()			    # 市
    name = scrapy.Field()			    # 景点名称
    imgUrls = scrapy.Field()			# 图片url
    location = scrapy.Field()		    # 景点地点
    point = scrapy.Field()			    # 景点评分
    level = scrapy.Field()              # 景点评级
    description = scrapy.Field()    	# 景点描述
    introduction = scrapy.Field()		# 景点介绍
    coordinate = scrapy.Field()         # 坐标
    subject = scrapy.Field()            # 主题
    comments = scrapy.Field()           # 评论

class UrlItem(scrapy.Item):
    url = scrapy.Field()                # 景点url

class TicketsItem(scrapy.Item):
    name = scrapy.Field()           # 门票名称
    type = scrapy.Field()           # 门票类型
    state = scrapy.Field()          # 门票说明
    price = scrapy.Field()          # 价钱
    bookingSites = scrapy.Field()   # 预订网站
    bookingUrl = scrapy.Field()     # 网站URL
