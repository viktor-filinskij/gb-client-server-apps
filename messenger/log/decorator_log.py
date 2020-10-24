#!/usr/bin/env python3
__author__ = 'Viktor Filinskij'

"""Декораторы"""

import sys
import os
import logging
import inspect
import traceback

sys.path.append(os.path.join(os.getcwd(), '..'))

import log.client_log_config
import log.server_log_config


# метод определения модуля, источника запуска.
# Метод find () возвращает индекс первого вхождения искомой подстроки,
# если он найден в данной строке.
# Если его не найдено, - возвращает -1.
if sys.argv[0].find('client_log_config') == -1:
    # если не клиент то сервер!
    LOGGER = logging.getLogger('server')
else:
    # ну, раз не сервер, то клиент
    LOGGER = logging.getLogger('client')


def log(func_to_log):
    """Функция-декоратор"""
    def log_saver(*args, **kwargs):
        ret = func_to_log(*args, **kwargs)
        LOGGER.debug(f'Была вызвана функция {func_to_log.__name__} c параметрами {args}, {kwargs}. '
                     f'Вызов из модуля {func_to_log.__module__}. Вызов из'
                     f'ф-ии {traceback.format_stack()[0].strip().split()[-1]}.'
                     f'Вызов из ф-ии {inspect.stack()[1][3]}')
        return ret
    return log_saver


def main():
    pass


if __name__ == '__main__':
    main()
