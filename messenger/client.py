#!/usr/bin/env python3
__author__ = 'Viktor Filinskij'

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


"""Программа-клиент"""

import sys
import json
import socket
import time
import argparse


from lib.constants import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME,\
    ACCOUNT_AUTH_STRING, TYPE, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT
from lib.utils import get_message, send_message


def create_presence(account_name='Guest'):
    """
    Функция генерирует запрос о присутствии клиента
    :param account_name:
    :return:
    """
    # {'action': 'presence', 'time': 1573760672.167031, 'user': {'account_name': 'Guest'}}
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        TYPE: "status",
        USER: {
            ACCOUNT_NAME: account_name,
            TYPE: 'Yep, I am here!'
        }
    }
    return out


def authenticate(account_name, account_auth_string):
    """
    Function that performs authentication against server
    :param account_name:
    :param account_auth_string:
    :return:
    """
    out = {
        ACTION: 'authenticate',
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name,
            ACCOUNT_AUTH_STRING: account_auth_string
        }
    }
    return out


def process_ans(message):
    """
    Функция разбирает ответ сервера
    :param message:
    :return:
    """
    if RESPONSE in message:
        # if message[RESPONSE] == 200:
        #     if message[ERROR]:
        #         return f'200 : {message[ERROR]}'
        #     else:
        #         return '200: OK'
        return f'{message[RESPONSE]} : {message[ERROR]}'
    raise ValueError


def main():
    """
    Загружаем параметы коммандной строки
    client.py 192.168.1.2 8079
    """
    try:
        server_address = sys.argv[1]
        server_port = int(sys.argv[2])
        if server_port < 1024 or server_port > 65535:
            raise ValueError
    except IndexError:
        server_address = DEFAULT_IP_ADDRESS
        server_port = DEFAULT_PORT
    except ValueError:
        print('В качестве порта может быть указано только число в диапазоне от 1024 до 65535.')
        sys.exit(1)

    # parser = argparse.ArgumentParser(description='Bind to some socket.')
    # parser.add_argument('-p', default=DEFAULT_PORT, type=int)
    # parser.add_argument('-a', default=DEFAULT_IP_ADDRESS, type=str)
    # server_port = (parser.parse_args()).p
    # server_address = (parser.parse_args()).a

    # Инициализация сокета и обмен
    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.connect((server_address, server_port))

    """
    To receive data from server we will accept messages in while loop
    """

    # while True:

    """
    As guest we can announce our presence, because no auth as guest required
    As registered user we, will get 401 error and will have to authenticate.  
    """

    message_to_server = create_presence()
    send_message(transport, message_to_server)
    try:
        answer = process_ans(get_message(transport))
        print(answer)
        print(type(answer))
    except (ValueError, json.JSONDecodeError):
        print('Не удалось декодировать сообщение сервера.')

    # message_to_server = create_presence('C0deMaver1ck')
    # send_message(transport, message_to_server)
    # message_to_server = authenticate('C0deMaver1ck', 'CorrectHorseBatterStaple')
    # send_message(transport, message_to_server)

    # try:
    #     answer = process_ans(get_message(transport))
    #     print(answer)
    #     print(type(answer))
    # except (ValueError, json.JSONDecodeError):
    #     print('Не удалось декодировать сообщение сервера.')

    # if '401' in answer:
    #     message_to_server = authenticate('C0deMaver1ck', 'CorrectHorseBatterStaple')
    #     # message_to_server = authenticate(input("Provide Username: "), input("Provide password: "))
    #     send_message(transport, message_to_server)
    #     try:
    #         answer = process_ans(get_message(transport))
    #         print(answer)
    #         print(type(answer))
    #     except (ValueError, json.JSONDecodeError):
    #         print('Не удалось декодировать сообщение сервера.')



if __name__ == '__main__':
    main()

