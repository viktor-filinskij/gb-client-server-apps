#!/usr/bin/env python3
__author__ = 'Viktor Filinskij'


import socket
# import sys
# import getopt
import argparse
import json


from lib.constants import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, ACCOUNT_AUTH_STRING, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT, DEFAULT_IP_ADDRESS

from lib.utils import get_message, send_message


"""
1. Реализовать простое клиент-серверное взаимодействие по протоколу JIM (JSON instant messaging):
клиент отправляет запрос серверу;
сервер отвечает соответствующим кодом результата. Клиент и сервер должны быть реализованы в виде отдельных скриптов, 
содержащих соответствующие функции. Функции клиента: сформировать presence-сообщение; 
отправить сообщение серверу; получить ответ сервера; разобрать сообщение сервера; 
параметры командной строки скрипта client.py <addr> [<port>]: addr — ip-адрес сервера; 
port — tcp-порт на сервере, по умолчанию 7777. 
Функции сервера: принимает сообщение клиента; формирует ответ клиенту; отправляет ответ клиенту; 
имеет параметры командной строки: -p <port> — TCP-порт для работы (по умолчанию использует 7777);
-a <addr> — IP-адрес для прослушивания (по умолчанию слушает все доступные адреса).
"""

"""Программа-сервер"""


def check_account(account_name, account_pass):

    valid_accounts = [{'user_name': 'Guest', 'user_password': None},
                      {'user_name': 'C0deMaver1ck','user_password': 'CorrectHorseBatteryStaple'}]

    for record in valid_accounts:
        # print(record)
        # for user_name, user_password in record.values():
            # print(user_name, user_password)
            # if account_name == user_name and account_pass == user_password:
        if account_name == record.get('user_name') and account_pass == record.get('user_password'):
            return True

    return 'Invalid Account'


def check_msg_has_required_fields(msg):

    required_keys = [ACTION, TIME, USER]

    msg_format_valid = True

    for key in required_keys:
        if key in msg.keys():
            pass
        else:
            msg_format_valid = False

    return msg_format_valid

def process_client_message(message):
    """
    Обработчик сообщений от клиентов, принимает словарь -
    сообщение от клинта, проверяет корректность,
    возвращает словарь-ответ для клиента

    :param message:
    :return:
    """

    # probably need to create a separate function to check message
    # for presence of required fields
    if check_msg_has_required_fields(message):
        if message[ACTION] in ['presence', 'authenticate']:
            pass
    else:
        return {RESPONSE: 400, ERROR: 'Bad Request'}

    if message[ACTION] == PRESENCE:
        if message[USER][ACCOUNT_NAME] == 'Guest':
            return {RESPONSE: 200,
                    ERROR: 'OK'}
        else:
            return {RESPONSE: 401,
                    ERROR: 'Authentication Required'}

    if message[ACTION] == 'authenticate' and ACCOUNT_AUTH_STRING in message[USER].keys():
        if check_account(message[USER][ACCOUNT_NAME], message[USER][ACCOUNT_AUTH_STRING]):
            return {RESPONSE: 200,
                ERROR: 'Authenticated'}
        else:
            return {
                RESPONSE: 402,
                ERROR: 'Wrong credentials'
            }


def main(*argv):
    """
    Загрузка параметров командной строки, если нет параметров, то задаём значения по умоланию.
    Сначала обрабатываем порт:
    server.py -p 8079 -a 192.168.1.2
    :return:
    """
    # try:
    #     opts, args = getopt.getopt(argv, "p:a:")
    # except getopt.GetoptError:
    #     print(f'Starting with defaults -p {DEFAULT_PORT} -a {DEFAULT_IP_ADDRESS}')
    # else:
    #     for opt, arg in opts:
    #         if opt == "-p":
    #             listen_port = arg
    #         elif opt == "-a":
    #             listen_address = arg
    # listen_address = DEFAULT_IP_ADDRESS
    # listen_port = DEFAULT_PORT

    parser = argparse.ArgumentParser(description='Bind to some socket.')
    parser.add_argument('-p', default=DEFAULT_PORT, type=int)
    parser.add_argument('-a', default=DEFAULT_IP_ADDRESS, type=str)

    listen_port = (parser.parse_args()).p
    print(listen_port)
    listen_address = (parser.parse_args()).a
    print(listen_address)

    # listen_address = parser.parse_args(['-a'])
    # print(listen_address)
    # try:
    #     if '-p' in sys.argv:
    #         listen_port = int(sys.argv[sys.argv.index('-p') + 1])
    #     else:
    #         listen_port = DEFAULT_PORT
    #     if listen_port < 1024 or listen_port > 65535:
    #         raise ValueError
    # except IndexError:
    #     print('После параметра -\'p\' необходимо указать номер порта.')
    #     sys.exit(1)
    # except ValueError:
    #     print(
    #         'В качастве порта может быть указано только число в диапазоне от 1024 до 65535.')
    #     sys.exit(1)
    #
    # # Затем загружаем какой адрес слушать
    #
    # try:
    #     if '-a' in sys.argv:
    #         listen_address = sys.argv[sys.argv.index('-a') + 1]
    #     else:
    #         listen_address = DEFAULT_IP_ADDRESS
    #
    # except IndexError:
    #     print(
    #         'После параметра \'a\'- необходимо указать адрес, который будет слушать сервер.')
    #     sys.exit(1)

    # Готовим сокет

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # transport.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    transport.bind((listen_address, listen_port))

    # Слушаем порт

    transport.listen(MAX_CONNECTIONS)

    while True:

        client, client_address = transport.accept()

        try:
            message_from_cient = get_message(client)
            print(message_from_cient)
            # {'action': 'presence', 'time': 1573760672.167031, 'user': {'account_name': 'Guest'}}
            response = process_client_message(message_from_cient)
            send_message(client, response)

            """
            If we want to continue to deal with clients we have to keep socket (communication endpoint) open
            """
            client.close()
        except (ValueError, json.JSONDecodeError):
            print('Принято некорретное сообщение от клиента.')
            client.close()


if __name__ == '__main__':
    main()
