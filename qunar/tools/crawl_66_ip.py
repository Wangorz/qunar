import pymysql
import requests
from lxml import etree
from lxml import html


def get_proxy_ip():
    url = 'http://www.66ip.cn/'
    crawl_ip(url + 'index.html')
    for i in range(2, 11):
        crawl_ip(url + str(i) + '.html')

def crawl_ip(url):
    # url = 'http://www.66ip.cn/index.html'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.encoding = 'GBK'
    html = etree.HTML(response.text)
    ipList = html.xpath('//*[@id="main"]/div/div[1]/table//tr/td[1]/text()')
    portList = html.xpath('//*[@id="main"]/div/div[1]/table//tr/td[2]/text()')
    proxyList = []
    for i in range(1, len(ipList)):
        proxy_ip = 'http://' + ipList[i] + ':' + portList[i]
        if judge_ip(proxy_ip):
            proxyList.append(proxy_ip)
    store_ip(proxyList)

def judge_ip(proxy_ip):
    try:
        proxy_dict = {'http': proxy_ip}
        target_url = 'https://piao.qunar.com'
        print('Testing proxy url: ' + proxy_ip)
        response = requests.get(target_url, proxies=proxy_dict)
        if response.status_code == 200:
            print('Success! ' + proxy_ip)
            return True
        else:
            print('Fail!    ' + proxy_ip)
            return False
    except:
        print('Fail!    ' + proxy_ip)
        return False

def store_ip(proxyList):
    for proxy_ip in proxyList:
        cursor.execute(
            "insert into proxy_ip values ('{0}')".format(proxy_ip)
        )
        connection.commit()

if __name__ == '__main__':
    connection = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='dy123456',
        db='proxy_ip',
        charset='utf8mb4'
    )
    cursor = connection.cursor()
    get_proxy_ip()
    cursor.close()
    connection.close()

    # judge_ip('http://171.35.169.62:9999')

