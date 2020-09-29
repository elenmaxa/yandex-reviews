# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst


class ReviewItem(scrapy.Item):
    companyName = scrapy.Field(output_processor=TakeFirst())
    reviewText = scrapy.Field(output_processor=TakeFirst())
    reviewAuthor = scrapy.Field(output_processor=TakeFirst())
    publishedDate = scrapy.Field(output_processor=TakeFirst())
    rating = scrapy.Field(output_processor=TakeFirst())
    comments = scrapy.Field(output_processor=TakeFirst())


class CommentItem(scrapy.Item):
    commentAuthor = scrapy.Field(output_processor=TakeFirst())
    publishedDate = scrapy.Field(output_processor=TakeFirst())
    commentText = scrapy.Field(output_processor=TakeFirst())
