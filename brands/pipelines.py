import pymongo
from scrapy.exceptions import DropItem


class MongoPipeline:
    collection_name = 'brands'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.client = None
        self.db = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri="localhost:27017",
            mongo_db="local",
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # print("Processing item:", item)  # Add this line.
        try:
            self.db[self.collection_name].insert_one(dict(item))
            return item
        except pymongo.errors.DuplicateKeyError:
            raise DropItem("Duplicate item found: %s" % item)
        except Exception as e:
            # print(f"Error inserting item: {e}")
            return item  # or raise DropItem, depending on how errors should be hand