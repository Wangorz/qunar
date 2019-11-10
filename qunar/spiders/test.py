import scrapy

class TestSpider(scrapy.Spider):
    name = "test"
    allowed_domains = ["httpbin.org"]
    start_urls = (
        # 请求的链接
        "https://httpbin.org/get?show_env=1",
    )

    def parse(self, response):
        # 打印出相应结果
        print(response.text)

if __name__ == '__main__':
    from scrapy import cmdline
    cmdline.execute("scrapy crawl test".split())
