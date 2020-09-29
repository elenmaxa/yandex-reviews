from datetime import datetime
import json
from scrapy.spiders import Spider
from scrapy.loader import ItemLoader
from scrapy import Request
from review_scraper.items import ReviewItem, CommentItem
import re
import urllib


class ReviewSpider(Spider):

    name = 'review'

    def __init__(self, company_name=None, company_id=None, force=None, *args, **kwargs):

        super(ReviewSpider, self).__init__(*args, **kwargs)
        self.allowed_domains = ['yandex.by']
        self.company_name = company_name
        self.company_id = company_id
        self.force = force
        self.start_urls = [f'https://yandex.by/maps/org/{company_name}/{company_id}/reviews/']

    def start_requests(self):
        yield Request(self.start_urls[0], self.parse, meta={})

    def parse(self, response):
        """
        This function takes the content from contents and map them according to the
        items from items.py. If the key exists in content, then Scrapy will aggregate
        the rest of the items and combine them.

        Each content will have "[0]" to indicate the first listing from the array.
        """
        token = re.search(r'\"csrfToken\":\"(?P<token>.+?)\"', response.text).group('token')
        session_id = re.search(r'\"sessionId\":\"(?P<session_id>.+?)\"', response.text).group('session_id')
        req_id = re.search(r'\"requestId\":\"(?P<req_id>.+?)\"', response.text).group('req_id')
        reviews_count = re.search(r'\"count\":(?P<count>\d+?),\"loaded', response.text).group('count')

        params = {
            'ajax': 1,
            'businessId': self.company_id,
            'csrfToken': token,
            'page': 1,
            'pageSize': reviews_count,
            'ranking': 'by_time',
            'reqId': req_id,
            # 's': 3764912524,
            'sessionId': session_id
        }
        url = f'https://yandex.by/maps/api/business/fetchReviews?{urllib.parse.urlencode(params)}'
        yield Request(url=url, callback=self.parse_item)

    def parse_item(self, response):
        self.logger.info('You are now crawling: %s', response.url)

        json_response = self.get_json_response(response)
        reviews = json_response.get('data', {}).get('reviews')
        old_reviews = list(self.db['reviews'].find({}, {'_id': 0, 'text': 1}))
        for review in reviews:
            if self.force or review.get('text') not in old_reviews:
                yield self.parse_review(response, review)

    def parse_review(self, response, review):
        item_loader = ItemLoader(item=ReviewItem(), selector=response)
        review_text = review.get('text')
        review_author = review.get('author', {}).get('name')
        date = review.get('updatedTime')
        published_date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ')
        rating = review.get('rating')
        has_comments = review.get('hasComments')

        item_loader.add_value('companyName', self.company_name)
        item_loader.add_value('reviewText', review_text)
        item_loader.add_value('reviewAuthor', review_author)
        item_loader.add_value('publishedDate', published_date)
        item_loader.add_value('rating', rating)
        if has_comments:
            entity_id = review.get('reviewId')
            item_loader.add_value('comments', True)

            params = {
                'stats': {
                    "l": "ru",
                    "m": "wide",
                    "r": "16.8.4",
                    "s": "ugc_maps",
                    "t": "maps",
                    "v": "2.19.1",
                    "dnt": "1"
                },
                'entityId': entity_id,
                # 'sid': '',
                'allowAbsent': True,
                'supplierServiceSlug': 'ugc'
            }
            url = f'https://yandex.by/comments/api/v1/tree?{urllib.parse.urlencode(params)}'
            item = item_loader.load_item()
            return Request(url, callback=self.parse_comment_page, cb_kwargs=dict(item=item))
        return item_loader.load_item()

    def parse_comment_page(self, response, item):
        item['comments'] = []
        json_response = self.get_json_response(response)
        comments = json_response.get('tree')
        comments.pop('0')
        for key in comments.keys():
            comment_item_loader = ItemLoader(item=CommentItem(), selector=response)
            comment_author = comments[key].get('user', {}).get('displayName') or comments[key].get('isOfficial')
            comment_text = comments[key].get('content', [{}])[0].get('text')
            # published_date =
            comment_item_loader.add_value('commentAuthor', 'Official' if comment_author is True else comment_author)
            comment_item_loader.add_value('commentText', comment_text)
            comment_item_loader.add_value('publishedDate', 'published_date')
            item['comments'].append(comment_item_loader.load_item())
        return item

    @staticmethod
    def get_json_response(response):
        try:
            return json.loads(response.body_as_unicode())
        except ValueError:
            return {}
