# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
import redis
import pymongo

class SightUrlRedisPipeline(object):

    def __init__(self):
        self.redis_db = redis.Redis(host='47.97.198.174', port=6379, db=0)

    def process_item(self, item, spider):
        # print('here')
        self.redis_db.lpush('qunar:sight_urls', item['url'])
        # print('insert successfully.')
        return item


class SightInfoMongodbPipeline(object):

    def __init__(self):
        self.client = pymongo.MongoClient(host='47.97.198.174', port=27017)
        self.db = self.client.qunar
        self.collection = self.db.sight

    def process_item(self, item, spider):
        try:
            self.collection.insert_one(item)
        except pymongo.errors.DuplicateKeyError:
            condition = {'_id': item['_id']}
            select_result = self.collection.find_one(condition)
            if item['subject'] not in select_result['subject']:
                update_subject = select_result['subject'] + ',' + item['subject']
                select_result['subject'] = update_subject
                self.collection.update(condition, select_result)
            else:
                print(item['subject'] + 'already exists.')
        return item










    # def __init__(self):
    #     self.connection = pymysql.connect(
    #         host='127.0.0.1',
    #         port=3306,
    #         user='root',
    #         password='dy123456',
    #         database='qunar',
    #         charset='utf8mb4'
    #     )
    #     self.cursor = self.connection.cursor()
    #     self.count = 0
    #
    # def process_item(self, item, spider):
    #     # print(item)
    #     print('we are here')
    #     insert_sql = "insert into sight values ('{0}', '{1}', '{2}', '{3}', '{4}'," \
    #                  " '{5}', '{6}', '{7}', '{8}', '{9}', '{10}', '{11}', '{12}')"
    #     try:
    #         self.cursor.execute(insert_sql.format(item['sightId'], item['province'], item['city'],
    #                                               item['name'], item['imgUrls'], item['location'], item['point'],
    #                                               item['level'], item['description'], item['introduction'],
    #                                               item['coordinate'], item['subject'], item['comments']))
    #         self.connection.commit()
    #         self.count += 1
    #         print(str(self.count) + ': ' + 'insert ' + item['name'] + ' successfully.')
    #     except pymysql.err.IntegrityError:
    #         select_sql = "select subject from sight where sightId = '{0}'"
    #         update_sql = "update sight set subject = '{0}' where sightId = '{1}'"
    #         result = self.cursor.execute(select_sql.format(item['sightId']))
    #         subject = self.cursor.fetchone()[0]
    #         subject += ',' + item['subject']
    #         self.cursor.execute(update_sql.format(subject, item['sightId']))
    #         self.connection.commit()
    #     return item
    #
    # def __del__(self):
    #     self.cursor.close()
    #     self.connection.close()
