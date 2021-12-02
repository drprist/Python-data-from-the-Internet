from pymongo import MongoClient
from pprint import pprint

client = MongoClient('127.0.0.1', 27017)
db = client.hh
collection = db.hh_list


def coast(co):
    coast_list = list(collection.find({'$or': [{'max_coast': {'$gt': co}}, {'min_coast': {'$gt': co}}]}))
    for cl in coast_list:
        pprint(cl)


coast(800000)
