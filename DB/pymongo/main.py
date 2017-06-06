import pymongo

MONGO_URL = 'localhost'
MONGO_DB = 'taobao'
MONGO_TABLE = 'product_xxxx'

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]


def save_to_mongo(result):
    try:
        if db[MONGO_TABLE].insert(result):
            print('Save to mongo successfully!', result)
    except Exception:
        print('Save failed!', result)
