import sys
import random
import datetime

import pymongo

client = pymongo.MongoClient()  # need to put mongoDB url
db = client.bigchallenges
customers = db.customers

genders = ['male', 'female']

# get now date
now_date = datetime.datetime.now()
now_year = now_date.year

card_numbers = []

for index in range(50000):
    card_number = random.randint(7700_4300_3400_1100, 7700_5300_3400_1100)

    if card_number not in card_numbers:
        card_numbers.append(card_number)

    sys.stdout.write(f'\rNow index: {index}; Card_number: {card_number}')

print(f'\rCreate all card numbers')

for index in range(len(card_numbers)):
    year = random.randint(now_year - 65, now_year - 19)
    month = random.randint(1, 12)

    if month == 2:
        day = str(random.randint(1, 28))
    elif month in [1, 3, 5, 7, 8, 10, 12]:
        day = str(random.randint(1, 31))
    else:
        day = str(random.randint(1, 30))

    birthday = f'{day.rjust(2, "0")}.' \
               f'{str(month).rjust(2, "0")}.' \
               f'{year}'

    customer = {
        'id': index + 1,
        'card_number': card_numbers[index],
        'gender': random.choice(genders),
        'birthday': birthday
    }

    sys.stdout.write(f'\rIndex: {index}')

    customers.insert_one(customer)

sys.stdout.write('\rAll done')
