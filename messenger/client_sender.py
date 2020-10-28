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

import os
import sys
import json
import socket
import time
import logging
import argparse
import log.client_log_config


from lib.constants import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME,\
    ACCOUNT_AUTH_STRING, TYPE, SENDER, MESSAGE, MESSAGE_TEXT, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT
from lib.utils import get_message, send_message
from log.decorator_log import log
from errors import ReqFieldMissingError, ServerError


sys.path.append(os.path.join(os.getcwd(), '..'))

CLIENT_LOGGER = logging.getLogger('client.main')


# def log(func):
#     def wrapper(*args,**kwargs):
#         CLIENT_LOGGER.info(f'Starting {func.__name__}({args},{kwargs})')
#         res = func(*args, **kwargs)
#         CLIENT_LOGGER.info(f'End {func.__name__}({args},{kwargs})')
#         return res
#     return wrapper


@log
def create_presence(account_name='Guest'):
    """
    Функция генерирует запрос о присутствии клиента
    :param account_name:
    :return:
    """
    # {'action': 'presence', 'time': 1573760672.167031, 'user': {'account_name': 'Guest'}}
    # CLIENT_LOGGER.info(f'Запрос о присутствии клиента: {account_name}')
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


@log
def authenticate(account_name, account_auth_string):
    """
    Function that performs authentication against server
    :param account_name:
    :param account_auth_string:
    :return:
    """
    CLIENT_LOGGER.info(f'Аутентификация клиента {account_name} на сервере.')
    out = {
        ACTION: 'authenticate',
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name,
            ACCOUNT_AUTH_STRING: account_auth_string
        }
    }
    return out


@log
def process_ans(message):
    """
    Функция разбирает ответ сервера
    :param message:
    :return:
    """
    CLIENT_LOGGER.info(f'Разбор сообщения от сервера: {message}')
    if RESPONSE in message:
        # if message[RESPONSE] == 200:
        #     if message[ERROR]:
        #         return f'200 : {message[ERROR]}'
        #     else:
        #         return '200: OK'
        return f'{message[RESPONSE]} : {message[ERROR]}'
    raise ValueError


@log
def process_response_ans(message):
    """
    Функция разбирает ответ сервера на сообщение о присутствии,
    возращает 200 если все ОК или генерирует исключение при ошибке
    """
    CLIENT_LOGGER.debug(f'Разбор приветственного сообщения от сервера: {message}')
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        elif message[RESPONSE] == 400:
            raise ServerError(f'400 : {message[ERROR]}')
    raise ReqFieldMissingError(RESPONSE)


@log
def arg_parser():
    """Создаём парсер аргументов коммандной строки
    и читаем параметры, возвращаем 3 параметра
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-m', '--mode', default='send', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    client_mode = namespace.mode

    # проверим подходящий номер порта
    if not 1023 < server_port < 65536:
        CLIENT_LOGGER.critical(
            f'Попытка запуска клиента с неподходящим номером порта: {server_port}. '
            f'Допустимы адреса с 1024 до 65535. Клиент завершается.')
        sys.exit(1)

    # Проверим допустим ли выбранный режим работы клиента
    if client_mode not in ('listen', 'send'):
        CLIENT_LOGGER.critical(f'Указан недопустимый режим работы {client_mode}, '
                        f'допустимые режимы: listen , send')
        sys.exit(1)

    return server_address, server_port, client_mode

@log
def message_from_server(message):
    """Функция - обработчик сообщений других пользователей, поступающих с сервера"""
    # print(f"processing message_from_server, {message}")
    if ACTION in message and message[ACTION] == MESSAGE and \
            SENDER in message and MESSAGE_TEXT in message:
        print(f'Получено сообщение от пользователя '
              f'{message[SENDER]}:\n{message[MESSAGE_TEXT]}')
        CLIENT_LOGGER.info(f'Получено сообщение от пользователя '
                    f'{message[SENDER]}:\n{message[MESSAGE_TEXT]}')
    else:
        CLIENT_LOGGER.error(f'Получено некорректное сообщение с сервера: {message}')


@log
def create_message(sock, account_name='Guest'):
    """Функция запрашивает текст сообщения и возвращает его.
    Так же завершает работу при вводе подобной комманды
    """
    message = input('Введите сообщение для отправки или \'!!!\' для завершения работы: ')
    if message == '!!!':
        sock.close()
        CLIENT_LOGGER.info('Завершение работы по команде пользователя.')
        print('Спасибо за использование нашего сервиса!')
        sys.exit(0)
    message_dict = {
        ACTION: MESSAGE,
        TIME: time.time(),
        ACCOUNT_NAME: account_name,
        MESSAGE_TEXT: message
    }
    CLIENT_LOGGER.debug(f'Сформирован словарь сообщения: {message_dict}')
    return message_dict


def main():
    """
    Загружаем параметы коммандной строки
    client.py 192.168.1.2 8079 -m listen|send
    """
    # client.py -a 192.168.1.2 -p 8079 -m listen|send
    # parser = argparse.ArgumentParser(description='Bind to some socket.')
    # parser.add_argument('-a', default=DEFAULT_IP_ADDRESS, type=str)
    # parser.add_argument('-p', default=DEFAULT_PORT, type=int)
    # parser.add_argument('-m', default='listen', type=str)

    # server_port = (parser.parse_args()).p
    # server_address = (parser.parse_args()).a
    # client_mode = (parser.parse_args()).m

    server_address, server_port, client_mode = arg_parser()

    print(f'server address: {server_address}, server port:{server_port}, mode: {client_mode}')
    CLIENT_LOGGER.info(f'Запущен клиент с парамертами: адрес сервера: {server_address},'
                       f'порт: {server_port}, режим работы: {client_mode}')
    # Инициализация сокета и сообщение серверу о нашем появлении
    try:
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((server_address, server_port))
        send_message(transport, create_presence())
        answer = process_response_ans(get_message(transport))
        CLIENT_LOGGER.info(f'Установлено соединение с сервером. Ответ сервера: {answer}')
        print(f'Установлено соединение с сервером.')
    except json.JSONDecodeError:
        CLIENT_LOGGER.error('Не удалось декодировать полученную Json строку.')
        sys.exit(1)
    except ServerError as error:
        CLIENT_LOGGER.error(f'При установке соединения сервер вернул ошибку: {error.text}')
        sys.exit(1)
    except ReqFieldMissingError as missing_error:
        CLIENT_LOGGER.error(f'В ответе сервера отсутствует необходимое поле {missing_error.missing_field}')
        sys.exit(1)
    except ConnectionRefusedError:
        CLIENT_LOGGER.critical(
            f'Не удалось подключиться к серверу {server_address}:{server_port}, '
            f'конечный компьютер отверг запрос на подключение.')
        sys.exit(1)
    else:
        # Если соединение с сервером установлено корректно,
        # начинаем обмен с ним, согласно требуемому режиму.
        # основной цикл прогрммы:
        if client_mode == 'send':
            print('Режим работы - отправка сообщений.')
        else:
            print('Режим работы - приём сообщений.')
        while True:
            # режим работы - отправка сообщений
            if client_mode == 'send':
                try:
                    send_message(transport, create_message(transport))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    CLIENT_LOGGER.error(f'Соединение с сервером {server_address} было потеряно.')
                    sys.exit(1)

            # Режим работы приём:
            if client_mode == 'listen':
                try:
                    message_from_server(get_message(transport))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    CLIENT_LOGGER.error(f'Соединение с сервером {server_address} было потеряно.')
                    sys.exit(1)
    # try:
    #     server_address = sys.argv[1]
    #     server_port = int(sys.argv[2])
    #     if server_port < 1024 or server_port > 65535:
    #         raise ValueError
    # except IndexError:
    #     server_address = DEFAULT_IP_ADDRESS
    #     server_port = DEFAULT_PORT
    # except ValueError:
    #     CLIENT_LOGGER.critical(f'В качестве порта может быть указано только число в диапазоне от 1024 до 65535')
    #     # print('В качестве порта может быть указано только число в диапазоне от 1024 до 65535.')
    #     sys.exit(1)



    # parser = argparse.ArgumentParser(description='Bind to some socket.')
    # parser.add_argument('-p', default=DEFAULT_PORT, type=int)
    # parser.add_argument('-a', default=DEFAULT_IP_ADDRESS, type=str)
    # server_port = (parser.parse_args()).p
    # server_address = (parser.parse_args()).a

    # Инициализация сокета и обмен
    # transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # transport.connect((server_address, server_port))
    #
    # """
    # To receive data from server we will accept messages in while loop
    # """
    #
    # # while True:
    #
    # """
    # As guest we can announce our presence, because no auth as guest required
    # As registered user we, will get 401 error and will have to authenticate.
    # """
    # # CLIENT_LOGGER.info(f'Вызваeм ф-цию: create_presence() из ф-ции main()')
    # message_to_server = create_presence()
    # send_message(transport, message_to_server)
    # try:
    #     # CLIENT_LOGGER.info(f'Вызваeм ф-цию: process_ans() из ф-ции main()')
    #     answer = process_ans(get_message(transport))
    #     # CLIENT_LOGGER.info(f'Ответ от сервера: {answer}')
    #     # print(answer)
    #     # print(type(answer))
    # except (ValueError, json.JSONDecodeError):
    #     # print('Не удалось декодировать сообщение сервера.')
    #     CLIENT_LOGGER.error(f'Не удалось декодировать сообщение сервера')

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

