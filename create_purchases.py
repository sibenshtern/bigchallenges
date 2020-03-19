import sys
import random
import datetime

import pymongo


client = pymongo.MongoClient(
    "mongodb+srv://sibenshtern:sibenshtern@bugchallenges-xyijm.mongodb.net/"
    "test?retryWrites=true&w=majority"
)
db = client.bigchallenges
products = db.products
customers = db.customers
purchases = db.purchases


for index in range(64092, 100000):  # todo: set 100000
    customer_card = customers.find(
        {'id': random.randint(1, 50000)}
    )[0]['card_number']

    # get now date
    now_date = datetime.datetime.now()
    now_day = now_date.day
    now_month = now_date.month
    now_year = now_date.year

    # create selling_date
    purchase_year = random.randint(2019, now_year)

    if purchase_year == now_year:
        purchase_month = random.randint(1, now_month)
    else:
        purchase_month = random.randint(1, 12)

    if purchase_month == now_month:
        purchase_day = random.randint(1, now_day)
    else:
        if purchase_month == 2:
            purchase_day = random.randint(1, 28)
        elif purchase_month in [1, 3, 5, 7, 8, 10, 12]:
            purchase_day = random.randint(1, 31)
        else:
            purchase_day = random.randint(1, 30)

    purchase_date = datetime.datetime(purchase_year, purchase_month,
                                      purchase_day)

    basket = []
    used_id = []
    for product_index in range(random.randint(1, 10)):

        product_id = random.randint(1, 1248)
        while product_id in used_id:
            product_id = random.randint(1, 1248)

        used_id.append(product_id)

        product = products.find({'id': product_id})[0]

        if product['selling_price'] <= 100:
            weight = round(random.random() + random.randint(1, 3), 2)
        elif 100 < product['selling_price'] <= 500:
            weight = round(random.random() + random.randint(1, 2), 2)
        else:
            weight = round(random.random() + 1, 2)

        total_price = round(product['selling_price'] * weight, 2)

        basket.append(
            {
                'id': product_id,
                'weight': weight,
                'total_price': total_price
            }
        )

    purchase = {
        'id': index + 1,
        'customer_card': customer_card,
        'date_of_purchases': purchase_date,
        'products': basket,
        'total_price':
            round(sum([product['total_price'] for product in basket]), 2)
    }

    purchases.insert_one(purchase)

    sys.stdout.write(f'\rIndex: {index + 1}')

sys.stdout.write(f'\rAll done')
