import sys
import pymongo
import datetime

client = pymongo.MongoClient()  # need to put mongoDB url
db = client.bigchallenges
customers = db.customers


# for index in range(1, 50001):

for index in range(5, 50001):
    cursor = customers.find({'id': index})
    day, month, year = map(int, cursor[0]['birthday'].split('.'))
    customers.update_one(
        {'id': index},
        {'$set': {'birthday': datetime.datetime(year, month, day)}}
    )

    sys.stdout.write(f'\rIndex: {index}')
