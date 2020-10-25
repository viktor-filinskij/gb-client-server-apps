#!/usr/bin/env python3
__author__ = 'Viktor Filinskij'

import logging

# IP адрес по умолчанию
DEFAULT_IP_ADDRESS = '127.0.0.1'
# Порт сетевого ваимодействия
DEFAULT_PORT = 7777
# Максимальная очередь подключений
MAX_CONNECTIONS = 5
# Максимальная длинна сообщения в байтах
MAX_PACKAGE_LENGTH = 4096
# Кодировка проекта
ENCODING = 'utf-8'
# Текущий уровень логирования
LOGGING_LEVEL = logging.DEBUG

# Прококол JIM основные ключи:
ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'
ACCOUNT_AUTH_STRING = 'password'
TYPE = 'type'
SENDER = 'sender'

# Прочие ключи, используемые в протоколе
PRESENCE = 'presence'
RESPONSE = 'response'
ERROR = 'error'
MESSAGE = 'message'
MESSAGE_TEXT = 'mess_text'