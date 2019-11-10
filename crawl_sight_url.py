# -*- coding: utf-8 -*-

from scrapy import cmdline
import redis
redis_db = redis.Redis(host='47.97.198.174', port=6379, db=0)
redis_db.lpush('qunar:start_urls', 'https://piao.qunar.com/ticket/list.htm?keyword=上海&region=上海&from=mpshouye_hotcity')
cmdline.execute('scrapy crawl qunar'.split())
