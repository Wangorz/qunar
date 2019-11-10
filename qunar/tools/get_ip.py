import requests
from scrapy.selector import Selector
import pymysql
import random

class GetProxyIP(object):

    # def getRandomIp(self):
    #     for ip in self.IpList:
    #         if self.judge_ip(ip):
    #             return random.choice(self.IpList)

    def __init__(self):
        self.connection = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='dy123456',
            database='proxy_ip',
            charset='utf8mb4'
        )
        self.cursor = self.connection.cursor()

    def get_random_ip(self):
        # 从数据库中随机获取一个可用ip
        random_sql = 'SELECT * FROM proxy_ip ORDER BY RAND() LIMIT 1'
        result = self.cursor.execute(random_sql)
        for proxy_ip in self.cursor.fetchall():
            ip = proxy_ip[0]
            return ip

    def judge_ip(self, proxy_ip):
        try:
            proxy_dict = {'http': proxy_ip}
            target_url = 'https://piao.qunar.com'
            # print('Testing proxy url: ' + proxy_ip)
            response = requests.get(target_url, proxies=proxy_dict)
            if response.status_code == 200:
                # print('Success! ' + proxy_ip)
                return True
            else:
                # print('Fail!    ' + proxy_ip)
                return False
        except:
            # print('Fail!    ' + proxy_ip)
            return False

    def delete_ip(self, ip):
        # 删除无效的ip
        delete_sql = "delete from proxy_ip where proxy_ip = '{0}'".format(ip)
        self.cursor.execute(delete_sql)
        self.connection.commit()

    def __del__(self):
        self.cursor.close()
        self.connection.close()


if __name__ == '__main__':
    getIp = GetProxyIP()
    print(getIp.get_random_ip())




