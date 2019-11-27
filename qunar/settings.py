# -*- coding: utf-8 -*-

# Scrapy settings for qunar project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'qunar'

SPIDER_MODULES = ['qunar.spiders']
NEWSPIDER_MODULE = 'qunar.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'qunar (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'qunar.middlewares.QunarSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'qunar.middlewares.QunarDownloaderMiddleware': 543,
    'qunar.middlewares.ProxyMiddleware': 544,
    'qunar.middlewares.RandomUserAgentMiddleware': 545,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
}
DOWNLOAD_DELAY = 0.2

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'qunar.pipelines.SightUrlRedisPipeline': 300,
    'qunar.pipelines.SightInfoMongodbPipeline': 301,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html

# AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


IPLIST = ['http://193.178.50.49:3128', 'http://188.136.222.1:9090', 'http://36.91.183.249:8080',
          'http://186.211.176.190:38934', 'http://27.111.38.133:39850', 'http://102.65.157.113:8080',
          'https://206.246.75.169:3129', 'https://163.204.240.89:9999', 'https://115.42.33.47:8080',
          'https://27.152.90.211:9999', 'https://183.166.86.189:9999', 'https://117.30.113.160:9999']


# """ scrapy-redis配置 """
# # Enables scheduling storing requests queue in redis.
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# # Ensure all spiders share same duplicates filter through redis.
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
#
REDIS_HOST = '47.97.198.174'
REDIS_PORT = 6379


LOG_FILE = "mySpider.log"
LOG_LEVEL = "INFO"

# CRITICAL - 严重错误(critical)
# ERROR - 一般错误(regular errors)
# WARNING - 警告信息(warning messages)
# INFO - 一般信息(informational messages)
# DEBUG - 调试信息(debugging messages)
