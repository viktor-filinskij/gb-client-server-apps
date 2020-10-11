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

import getopt, sys
import socket
import time


bind_host = socket.gethostname()
bind_port = 7777


def main(argv):

    # check if script started with parameters
    if argv:
        try:
            opts, args = getopt.getopt(argv, "ha:p:",["address=", "port="])
        except getopt.GetoptError:
            print(f'Starting server with default values')
            # sys.exit(2)
        for opt, arg in opts:
            if opt == '-h':
                print('test.py -a <listen_address> -p <listen_port>')
            elif opt in ("-a", "--address"):
                bind_host == arg
            elif opt in ("-p", "--port"):
                bind_port == arg

    # create an INET, STREAMing socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # by default bind the socket to a public host, and a default port
    server_socket.bind((bind_host, bind_port))

    # become a server socket
    server_socket.listen(5)

    while True:
        # accept connections from outside
        (client_socket, address) = server_socket.accept()
        # kind of a logging
        print(f'Got request from: {address}')

        # process client request:
        with client_socket as c_sock:
            pass


if __name__ == '__main__':
    main()
