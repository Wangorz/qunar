import json
import time
import requests
import pymysql

def sort_ip():
    response_time = {}
    file = open('../tools/iplist.txt')
    ipnum = 0
    for line in file.readlines():
        count = 0
        ipJson = json.loads(line)
        if ipJson['type'] == 'http':
            continue
        ip = ipJson['type'] + '://' + ipJson['host'] + ':' + str(ipJson['port'])
        print(str(ipnum) + '  ' + ip)
        ipnum += 1
        url = 'http://piao.qunar.com/ticket/list.htm?keyword=上海&region=上海&from=mpshouye_hotcity'
        proxies = {ipJson['type']: ip}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
        }
        try:
            start = time.time()
            response = requests.get(url=url, headers=headers, proxies=proxies, timeout=1)
            count += 1
            response = requests.get(url=url, headers=headers, proxies=proxies, timeout=1)
            count += 1
            end = time.time()
            print(end - start)
            if count == 2:
                response_time[ip] = end - start
        except requests.exceptions.RequestException as e:
            print(e)
        except requests.exceptions.ReadTimeout as e:
            print(e)
    return response_time

def test():
    connection = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='dy123456',
        db='proxy_ip',
        charset='utf8mb4'
    )
    cursor = connection.cursor()
    ip = 'http://1.1.1.1:8888'
    sql = 'insert into proxy_ip values ("{0}")'.format(ip)
    cursor.execute(sql)
    connection.commit()
    cursor.close()
    connection.close()

if __name__ == "__main__":

    # test()
    response_time = sort_ip()
    sorted_ip = sorted(response_time)
    connection = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='dy123456',
        db='proxy_ip',
        charset='utf8mb4'
    )
    cursor = connection.cursor()
    for ip in sorted_ip[:30]:
        print(ip + '   ' + str(response_time[ip]/2))
        sql = 'insert into proxy_ip values ("{0}")'.format(ip)
        cursor.execute(sql)
        connection.commit()
    cursor.close()
    connection.close()
