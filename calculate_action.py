import sys
import logging

import pymongo


logging.basicConfig(filename='customer.log', filemode='w', format='%(message)s', level=logging.INFO)
client = pymongo.MongoClient()  # need to put mongoDB url
db = client.bigchallenges

# create variables
count = 0
customers = {}
total_price = 0
coefficient = 0.46

for record in db.purchases.find():
    customer_card = record['customer_card']
    total_price_record = record['total_price']

    if customer_card not in customers:
        customers[customer_card] = {
            'total_price': total_price_record,
            'count': 1
        }
    else:
        try:
            customers[customer_card]['total_price'] += total_price_record
        except TypeError as error:
            print(error)
            print(customer_card[customer_card]['total_price'])
            print(total_price_record)
            raise Exception('Ты офигел или да?')
        finally:
            customers[customer_card]['count'] += 1

    total_price += total_price_record
    count += 1


middle_receipt = round(total_price / count, 1)
customer_middle_receipts = {}

for customer_card in customers:
    if customers[customer_card]['total_price'] != 0:
        customer_middle_receipt = round(
            customers[customer_card]['total_price'] /
            customers[customer_card]['count'], 1
        )
        customer_middle_receipts[customer_card] = customer_middle_receipt


index = 0
for customer in customer_middle_receipts:
    action = round(max(
        ((customer_middle_receipts[customer] -
          (middle_receipt + coefficient *
           customer_middle_receipts[customer])) /
         customer_middle_receipts[customer]) * 100, 0
    ), 1)

    action = min(30, action)

    db.actions.insert_one({
        'customer_card': customer,
        'action': action
    })

    logging.info(f'Customer: {customer}; action: {action}')
    sys.stdout.write(f'\rIndex: {index}')
    index += 1

sys.stdout.write('\rAll done!')
