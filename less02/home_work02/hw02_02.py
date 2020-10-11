#!/usr/bin/env python3
__author__ = 'Viktor Filinskij'

"""
2. Задание на закрепление знаний по модулю json. Есть файл orders
в формате JSON с информацией о заказах. Написать скрипт, автоматизирующий
его заполнение данными.

Для этого:
Создать функцию write_order_to_json(), в которую передается
5 параметров — товар (item), количество (quantity), цена (price),
покупатель (buyer), дата (date). Функция должна предусматривать запись
данных в виде словаря в файл orders.json. При записи данных указать
величину отступа в 4 пробельных символа;
Проверить работу программы через вызов функции write_order_to_json()
с передачей в нее значений каждого параметра.

ПРОШУ ВАС НЕ УДАЛЯТЬ ИСХОДНЫЙ JSON-ФАЙЛ
ПРИМЕР ТОГО, ЧТО ДОЛЖНО ПОЛУЧИТЬСЯ

{
    "orders": [
        {
            "item": "printer",
            "quantity": "10",
            "price": "6700",
            "buyer": "Ivanov I.I.",
            "date": "24.09.2017"
        },
        {
            "item": "scaner",
            "quantity": "20",
            "price": "10000",
            "buyer": "Petrov P.P.",
            "date": "11.01.2018"
        }
    ]
}

вам нужно подгрузить JSON-объект
и достучаться до списка, который и нужно пополнять
а потом сохранять все в файл
"""

import json
import os


DATA_STORE = 'orders.json'


def read_data(file):
    with open(os.path.join(os.getcwd(), file), 'r', encoding='utf-8') as orders_file:
        current_data = json.load(orders_file)

    return current_data


def write_order_to_json(item, quantity, price, buyer, date):
    order = dict(item=item, quantity=quantity, price=price, buyer=buyer, date=date)

    data = read_data(DATA_STORE)  # get current orders dict form existing orders file
    orders = data.get("orders")   # get current order list from orders dictionary

    orders.append(order)          # append order list, with new order
    data.update(orders=orders)    # update dictionary with new order list

    with open(os.path.join(os.getcwd(), DATA_STORE), 'r+', encoding='utf-8') as orders_file:
        json.dump(data, orders_file, indent=4, sort_keys=True)


def main():
    write_order_to_json('репка', 1.200, 8.50, 'Ольга', '2020-10-07')
    write_order_to_json('лук', 1.46, 7.20, 'Maksim', '2020-10-07')
    write_order_to_json('keyboard', 1, 299.99, 'Viktor', '2020-10-07')


if __name__ == '__main__':
    main()
