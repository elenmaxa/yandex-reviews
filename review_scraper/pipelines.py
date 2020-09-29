# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymongo


class MongoPipeline:

    collection_name = 'reviews'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):

        old_review = self.db[self.collection_name].find_one({
            'companyName': item['companyName'],
            'reviewText': item['reviewText']
        })
        if old_review:
            self.db[self.collection_name].update_one(
                {'_id': old_review['_id']},
                {'$set': item}
            )
            return item

        self.db[self.collection_name].insert_one(item)
        return item
