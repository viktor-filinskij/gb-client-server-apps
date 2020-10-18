#!/usr/bin/env python3
__author__ = 'Viktor Filinskij'


import socket
# import sys
# import getopt
import argparse
import json
import logging
import log.server_log_config


from lib.constants import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, ACCOUNT_AUTH_STRING, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT, DEFAULT_IP_ADDRESS

from lib.utils import get_message, send_message


SERVER_LOGGER = logging.getLogger('server.main')

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
    SERVER_LOGGER.info(f'{check_account.__name__} Проверка валидности клиента: {account_name}')
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
    SERVER_LOGGER.info(f'{check_msg_has_required_fields.__name__} Проверка корректного формата сообщения от клиента: {msg}')
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
        SERVER_LOGGER.warning(f'{process_client_message.__name__} Получено сообщение: {message}')
        if message[ACTION] in ['presence', 'authenticate']:
            pass
        else:
            SERVER_LOGGER.warning(f'{process_client_message.__name__} Не корректный формат сообщения: {message}')
            return {RESPONSE: 400, ERROR: 'Bad Request'}
    else:
        SERVER_LOGGER.warning(f'{process_client_message.__name__} Не корректный формат сообщения: {message}')
        return {RESPONSE: 400, ERROR: 'Bad Request'}

    if message[ACTION] == PRESENCE:
        SERVER_LOGGER.info(f'{process_client_message.__name__} Тип Сообщения - присутствие клиента: {message[USER][ACCOUNT_NAME]}')
        if message[USER][ACCOUNT_NAME] == 'Guest':
            SERVER_LOGGER.info(f'{process_client_message.__name__} Сообщение о присутствии клиента {message[USER][ACCOUNT_NAME]} подтверждено.')
            return {RESPONSE: 200,
                    ERROR: 'OK'}
        else:
            SERVER_LOGGER.warning(f'{process_client_message.__name__} Клиент {message[USER][ACCOUNT_NAME]} должен подтвердить личность.')
            return {RESPONSE: 401,
                    ERROR: 'Authentication Required'}

    if message[ACTION] == 'authenticate' and ACCOUNT_AUTH_STRING in message[USER].keys():
        SERVER_LOGGER.info(f'Тип Сообщения - аутентификация клиента: {message[USER][ACCOUNT_NAME]}')
        if check_account(message[USER][ACCOUNT_NAME], message[USER][ACCOUNT_AUTH_STRING]):
            SERVER_LOGGER.info(f'{process_client_message.__name__} Аутентификация клиента: {message[USER][ACCOUNT_NAME]}, прошла успешно')
            return {RESPONSE: 200,
                ERROR: 'Authenticated'}
        else:
            SERVER_LOGGER.warning(f'{process_client_message.__name__} Неудачная попытка аутентификации клиента: {message[USER][ACCOUNT_NAME]}')
            return {
                RESPONSE: 402,
                ERROR: 'Wrong credentials'
            }


def main():
    """
    Загрузка параметров командной строки, если нет параметров, то задаём значения по умоланию.
    Сначала обрабатываем порт:
    server.py -p 8079 -a 192.168.1.2
    :return:
    """

    parser = argparse.ArgumentParser(description='Bind to some socket.')
    parser.add_argument('-a', default=DEFAULT_IP_ADDRESS, type=str)
    parser.add_argument('-p', default=DEFAULT_PORT, type=int)

    listen_port = (parser.parse_args()).p
    listen_address = (parser.parse_args()).a

    # Готовим сокет
    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        transport.bind((listen_address, listen_port))
        SERVER_LOGGER.info(f'{__name__} Сервер запущен на: {listen_address}:{listen_port}')
    except OSError:
        SERVER_LOGGER.critical(f'Не удалось запустить сервер на: {listen_address}:{listen_port}')

    transport.listen(MAX_CONNECTIONS)

    while True:

        client, client_address = transport.accept()

        try:
            message_from_cient = get_message(client)
            # SERVER_LOGGER.info(f'Сообщение от клиента : {client_address}: {message_from_cient}')
            # {'action': 'presence', 'time': 1573760672.167031, 'user': {'account_name': 'Guest'}}
            response = process_client_message(message_from_cient)
            send_message(client, response)
            SERVER_LOGGER.info(f'{__name__} Обработка сообщения: SRC: {client_address} REQ: {message_from_cient} RESP: {response}')
            client.close()
        except (ValueError, json.JSONDecodeError):
            SERVER_LOGGER.error(f'{__name__} Получено некорректное сообщение SRC: {client_address} REQ: {message_from_cient}')
            client.close()


if __name__ == '__main__':
    main()
