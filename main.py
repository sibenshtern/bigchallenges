import sys

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QPushButton, QLabel, QLineEdit
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QFont

import pymongo


class Widget(QWidget):

    def __init__(self, *args, **kwargs):
        super(Widget, self).__init__(*args, **kwargs)

        self.client = pymongo.MongoClient()  # need to put mongoDB url
        self.db = self.client.bigchallenges

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Система лояльности клиентов')
        main_layout = QVBoxLayout()

        font = QFont(None)
        font.setPointSize(14)

        h_input_layout = QHBoxLayout()
        v_input_layout = QVBoxLayout()

        label = QLabel('Введите номер дисконтной карты: ')
        self.line_edit = QLineEdit()
        button = QPushButton('Вывести записи о покупателе')
        button1 = QPushButton('Показать скидку для покупателей')

        button.setFont(font)
        button1.setFont(font)
        label.setFont(font)
        self.line_edit.setFont(font)

        button.clicked.connect(self.show_customers)
        button1.clicked.connect(self.show_discounts)

        self.table = QTableWidget()
        self.table.setFont(font)

        h_input_layout.addWidget(label)
        h_input_layout.addWidget(self.line_edit)
        v_input_layout.addLayout(h_input_layout)
        v_input_layout.addWidget(button)
        v_input_layout.addWidget(button1)

        main_layout.addLayout(v_input_layout)
        main_layout.addWidget(self.table)

        self.load_table()

        self.setLayout(main_layout)

    def load_table(self):
        data = self.db.purchases.find(projection={'_id': 0, 'id': 0})


        titles = [
            'Номер карты покупателя', 'Дата покупки', 'Продукты',
            'Итоговая цена'
        ]

        self.table.setColumnCount(len(titles))
        self.table.setHorizontalHeaderLabels(titles)
        self.table.setRowCount(0)

        for row_index, row in enumerate(data):
            self.table.setRowCount(self.table.rowCount() + 1)
            for column_index, element in enumerate(row):
                self.table.setItem(row_index, column_index,
                                   QTableWidgetItem(str(row[element])))

        self.table.resizeColumnsToContents()

    def show_customers(self):
        cursor = self.connection.cursor()

        if self.line_edit.text() != '':
            card_number = int(self.line_edit.text())
        else:
            card_number = None

        if card_number is not None:
            self.table.clear()

            data = cursor.execute(
                "SELECT customer_card_number, date_of_purchase, item_name,"
                " action, items_count, price FROM purchases "
                "WHERE customer_card_number = ?", (card_number,)
            ).fetchall()

            titles = [
                'Номер карты покупателя', 'Дата покупки', 'Название продукта',
                'Акция', 'Количества продуктов', 'Цена'
            ]

            self.table.setColumnCount(len(titles))
            self.table.setHorizontalHeaderLabels(titles)
            self.table.setRowCount(0)

            for row_index, row in enumerate(data):
                self.table.setRowCount(self.table.rowCount() + 1)
                for column_index, element in enumerate(row):
                    self.table.setItem(row_index, column_index,
                                       QTableWidgetItem(str(element)))

            self.table.resizeColumnsToContents()
        else:
            self.load_table()

    def show_discounts(self):
        cursor = self.connection.cursor()
        data = cursor.execute(
            "SELECT card_number, discount FROM customers_discount"
        ).fetchall()

        titles = [
            'Номер карты покупателя', 'Скидка'
        ]

        self.table.setColumnCount(len(titles))
        self.table.setHorizontalHeaderLabels(titles)
        self.table.setRowCount(0)

        for row_index, row in enumerate(data):
            self.table.setRowCount(self.table.rowCount() + 1)
            for column_index, element in enumerate(row):
                self.table.setItem(row_index, column_index,
                                   QTableWidgetItem(str(element)))

        self.table.resizeColumnsToContents()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = Widget()
    widget.showMaximized()
    sys.exit(app.exec_())

