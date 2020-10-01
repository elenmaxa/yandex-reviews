# Scrapy settings for review_scraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import os
from dotenv import load_dotenv

load_dotenv()


BOT_NAME = 'review_scraper'

SPIDER_MODULES = ['review_scraper.spiders']
NEWSPIDER_MODULE = 'review_scraper.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3

# Disable cookies (enabled by default)
COOKIES_ENABLED = True
COOKIES_DEBUG = True

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'review_scraper.middlewares.ReviewScraperDownloaderMiddleware': 543,
   'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': 700,
   # 'scrapy_splash.SplashCookiesMiddleware': 723,
   # 'scrapy_splash.SplashMiddleware': 725,
   # 'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}
# SPIDER_MIDDLEWARES = {
# 'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
# }
# SPLASH_URL = 'http://localhost:8050'

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'review_scraper.pipelines.MongoPipeline': 10,
}

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
HTTPERROR_ALLOWED_CODES = [400]

MONGODB_URI = os.environ['MONGODB_URI']
MONGODB_DB = os.environ['MONGODB_DB']
