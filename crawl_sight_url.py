# -*- coding: utf-8 -*-

from scrapy import cmdline
import redis
redis_db = redis.Redis(host='47.97.198.174', port=6379, db=0)
redis_db.lpush('qunar:start_urls', 'https://piao.qunar.com/ticket/list.htm?keyword=中国&subject=自然风光&sort=&page=1')
redis_db.lpush('qunar:start_urls', 'https://piao.qunar.com/ticket/list.htm?keyword=中国&subject=文化古迹&sort=&page=1')
redis_db.lpush('qunar:start_urls', 'https://piao.qunar.com/ticket/list.htm?keyword=中国&subject=农家度假&sort=&page=1')
redis_db.lpush('qunar:start_urls', 'https://piao.qunar.com/ticket/list.htm?keyword=中国&subject=公园&sort=&page=1')
redis_db.lpush('qunar:start_urls', 'https://piao.qunar.com/ticket/list.htm?keyword=中国&subject=游乐场&sort=&page=1')
redis_db.lpush('qunar:start_urls', 'https://piao.qunar.com/ticket/list.htm?keyword=中国&subject=山川&sort=&page=1')
redis_db.lpush('qunar:start_urls', 'https://piao.qunar.com/ticket/list.htm?keyword=中国&subject=运动健身&sort=&page=1')
redis_db.lpush('qunar:start_urls', 'https://piao.qunar.com/ticket/list.htm?keyword=中国&subject=古建筑&sort=&page=1')
redis_db.lpush('qunar:start_urls', 'https://piao.qunar.com/ticket/list.htm?keyword=中国&subject=展馆&sort=&page=1')
redis_db.lpush('qunar:start_urls', 'https://piao.qunar.com/ticket/list.htm?keyword=中国&subject=温泉&sort=&page=1')
cmdline.execute('scrapy crawl qunar'.split())

