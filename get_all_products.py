import sys
import random
import datetime

import pymongo
import requests
from bs4 import BeautifulSoup


# create connection to database
client = pymongo.MongoClient()  # need to put mongoDB url
db = client.bigchallenges
products = db.products_without_date

# create variables
url = 'http://findfood.ru/product/index'

prices = []

# start parsing site
for category in range(4, 10):
    params = {'category': category}
    page = requests.get(url, params).content

    page_soup = BeautifulSoup(page, 'html.parser')
    pages_count = len(page_soup.find_all('li', class_='page'))

    for index in range(1, pages_count + 1):
        params['Product_page'] = index

        products_page = requests.get(url, params)
        products_soup = BeautifulSoup(
            products_page.content, 'html.parser'
        )

        product_divs = products_soup.find_all('div', class_='grid_4 view')

        for product_div in product_divs:
            link = product_div.find_all('a')[0]
            href = link['href']
            title = link['title']

            own_product_page = requests.get(f'http://findfood.ru{href}')
            own_product_soup = BeautifulSoup(
                own_product_page.content, 'html.parser'
            )

            own_product_divs = own_product_soup.find_all('div',
                                                         class_='grid_6')

            for own_product_div in own_product_divs:
                string = own_product_div.string

                if string is not None and string.endswith('р.'):
                    prices.append({
                        'title': title,
                        'selling_price': float(string.split()[0])
                    })

        print(products_page.url)


for index in range(len(prices)):
    extra_charge = random.randint(20, 35) / 100
    purchase_price = round(prices[index]['selling_price'] / (1 + extra_charge),
                           1)
    selling_price = prices[index]['selling_price']

    # get now date
    now_date = datetime.datetime.now()
    now_day = now_date.day
    now_month = now_date.month
    now_year = now_date.year

    # create purchase_date
    purchase_year = now_year
    purchase_month = random.randint(1, now_month)

    if purchase_month == 2:
        purchase_day = str(random.randint(1, 28))
    elif purchase_month in [1, 3, 5, 7, 8, 10, 12]:
        purchase_day = str(random.randint(1, 31))
    else:
        purchase_day = str(random.randint(1, 30))

    purchase_date = f'{purchase_day.rjust(2, "0")}.' \
                    f'{str(purchase_month).rjust(2, "0")}.' \
                    f'{purchase_year}'

    # create selling_date
    selling_year = now_year

    if selling_year == now_year:
        selling_month = random.randint(1, now_month + 3)
    else:
        selling_month = random.randint(purchase_month, purchase_month + 3)

    if selling_month > 12:
        print(selling_month)
        new_selling_month, add_year = selling_month % 12, selling_month // 12

        if add_year == 1:
            selling_year += 1
            selling_month = new_selling_month

    selling_date = (
        f'{str(31).rjust(2, "0")}.'
        f'{str(selling_month).rjust(2, "0")}.'
        f'{selling_year}'
    )

    margin = round(round((selling_price - purchase_price) / selling_price, 3)
                   * 100, 1)

    product = {
        'id': index + 1,
        'title': prices[index]['title'],
        'weight': round(random.random() + random.randint(20, 30), 1),
        'purchase_price': purchase_price,
        'extra_charge': round(extra_charge * 100, 1),
        'margin': margin,
        'selling_price': selling_price,
        # 'purchase_date': purchase_date,
        # 'sell_by_date': selling_date
    }

    products.insert_one(product)

    if index % 3 == 0:
        sys.stdout.write('\rinserting \\')
    if index % 4 == 0:
        sys.stdout.write('\rinserting |')
    if index % 5 == 0:
        sys.stdout.write('\rinserting /')
    if index % 6 == 0:
        sys.stdout.write('\rinserting -')

sys.stdout.write('\rAll done')
