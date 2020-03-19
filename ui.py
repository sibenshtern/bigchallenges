import sys

from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QLabel, QPushButton, QLineEdit
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.Qt import QFont

import pymongo


class Widget(QWidget):

    def __init__(self, *args, **kwargs):
        super(Widget, self).__init__(*args, **kwargs)
        self.client = pymongo.MongoClient(
            'mongodb+srv://application_user:application_user@'
            'bugchallenges-xyijm.mongodb.net/test?retryWrites=true&w=majority'
        )
        self.db = self.client.bigchallenges
        self.full_date = self.db.purchases.find(projection={'_id': 0, 'id': 0})
        total_price = 0
        count = 0

        for record in self.db.purchases.find():
            customer_card = record['customer_card']
            total_price_record = record['total_price']

            total_price += total_price_record
            count += 1

        self.middle_receipt = round(total_price / count, 1)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Программа лояльности клиентов')
        main_layout = QVBoxLayout()

        # create own font
        font = QFont(None)
        font.setPointSize(14)

        # create other layouts
        input_layout = QHBoxLayout()
        buttons_layout = QVBoxLayout()

        # create other widgets
        self.customer_card_input = QLineEdit()
        label = QLabel('Введите номер дисконтной карты: ')
        show_customers = QPushButton('Вывести записи о покупателе')
        show_discounts = QPushButton('Показать скидку для покупателей')

        # set font for widgets
        label.setFont(font)
        show_customers.setFont(font)
        show_discounts.setFont(font)
        self.customer_card_input.setFont(font)

        # connect buttons to functions
        show_customers.clicked.connect(self.show_customers)
        show_discounts.clicked.connect(self.show_discounts)

        # create a table and set it up
        self.table = QTableWidget()
        self.table.setFont(font)

        # set layouts up
        input_layout.addWidget(label)
        input_layout.addWidget(self.customer_card_input)

        buttons_layout.addLayout(input_layout)
        buttons_layout.addWidget(show_customers)
        buttons_layout.addWidget(show_discounts)

        main_layout.addLayout(buttons_layout)
        main_layout.addWidget(self.table)

        self.load_table()
        self.setLayout(main_layout)

    def load_table(self):
        data = self.full_date
        titles = [
            'Номер карты покупателя', 'Дата покупки',
            'Продукты', 'Итоговая цена'
        ]

        self.table.setColumnCount(len(titles))
        self.table.setHorizontalHeaderLabels(titles)
        self.table.setRowCount(0)

        for row_index, row in enumerate(data):
            self.table.setRowCount(self.table.rowCount() + 1)

            for column_index, element in enumerate(row):
                if element != 'products':
                    self.table.setItem(
                        row_index, column_index, QTableWidgetItem(
                            str(row[element])
                        )
                    )
                else:
                    self.table.setItem(
                        row_index, column_index,
                        QTableWidgetItem(self.pretty_element(row[element]))
                    )
            sys.stdout.write(f'\rIndex: {row_index}')
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

    def show_customers(self):
        customer_card = (
            int(self.customer_card_input.text())
            if self.customer_card_input.text().isdigit()
            else self.customer_card_input.text()
        )
        if isinstance(customer_card, int):
            data = self.db.purchases.find({'customer_card': customer_card},
                                          projection={'_id': 0, 'id': 0})
            titles = [
                'Номер карты покупателя', 'Дата покупки',
                'Продукты', 'Итоговая цена'
            ]

            self.table.setColumnCount(len(titles))
            self.table.setHorizontalHeaderLabels(titles)
            self.table.setRowCount(0)

            for row_index, row in enumerate(data):
                self.table.setRowCount(self.table.rowCount() + 1)

                for column_index, element in enumerate(row):
                    if element != 'products':
                        self.table.setItem(
                            row_index, column_index, QTableWidgetItem(
                                str(row[element])
                            )
                        )
                    else:
                        self.table.setItem(
                            row_index, column_index,
                            QTableWidgetItem(self.pretty_element(row[element]))
                        )
                sys.stdout.write(f'\rIndex: {row_index}')
            self.table.resizeColumnsToContents()
            self.table.resizeRowsToContents()
        else:
            self.load_table()

    def show_discounts(self):
        customer_card = (
            int(self.customer_card_input.text())
            if self.customer_card_input.text().isdigit()
            else self.customer_card_input.text()
        )
        data = self.db.purchases.find({'customer_card': customer_card},
                                      projection={'_id': 0, 'id': 0})
        titles = ['Номер карты покупателя', 'Скидка']
        total_count = 1
        count = 1

        for purchase in data:
            total_count += purchase['total_price']
            count += 1

        middle_receipt = round(total_count / count, 1)
        action = round(max(
            ((middle_receipt -
              (self.middle_receipt + 0.46 *
               middle_receipt)) /
             middle_receipt) * 100, 0
        ), 1)
        action = min(30, action)
        if isinstance(customer_card, int):
            self.table.setColumnCount(len(titles))
            self.table.setHorizontalHeaderLabels(titles)
            self.table.setRowCount(1)
            self.table.setItem(0, 0, QTableWidgetItem(str(customer_card)))
            self.table.setItem(0, 1, QTableWidgetItem(str(action)))

    def pretty_element(self, products):
        pretty_output = []

        for index in range(len(products)):
            pretty_product = []
            product_title = self.db.products.find_one(
                {'id': products[index]['id']}
            )
            pretty_product.append(f'{index + 1}. Название: {product_title["title"]};')
            pretty_product.append(f'Вес: {products[index]["weight"]};')
            pretty_product.append(f'Итоговая цена: '
                                  f'{products[index]["total_price"]}.')

            pretty_output.append(' '.join(pretty_product))
        return '\n'.join(pretty_output)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = Widget()
    widget.showMaximized()
    sys.exit(app.exec_())
