#!/usr/bin/env python3
__author__ = 'Viktor Filinskij'


"""
Простейшее логгирование
"""

import logging
import os


# Создаём объект-логгер с именем app.main
LOG = logging.getLogger('client.main')

# Создаём объект форматирования:
FORMATTER = logging.Formatter(f"%(asctime)s - %(levelname)s - %(filename)s - %(message)s ")

# Path to LOG_FILE, based on os assuming that
# logs directory are in same directory lvl as scripts
LOG_FILE = os.path.dirname(os.path.abspath(__file__))

if os.name == 'posix':
    LOG_FILE = os.path.join(LOG_FILE, f"../logs/{LOG.name}.log")
elif os.name == 'nt':
    LOG_FILE = os.path.join(LOG_FILE, f"..\\logs\\{LOG.name}.log")

# Создаём файловый обработчик логгирования (можно задать кодировку):
FILE_HANDLER = logging.FileHandler(LOG_FILE, encoding='utf-8')

#fh.setLevel(logging.DEBUG)
FILE_HANDLER.setFormatter(FORMATTER)

# Добавляем в логгер новый обработчик событий и устанавливаем уровень логгирования
LOG.addHandler(FILE_HANDLER)
LOG.setLevel(logging.DEBUG)

if __name__ == '__main__':
    # Создаём потоковый обработчик логгирования (по умолчанию sys.stderr):
    STREAM_HANDLER = logging.StreamHandler()
    #console.setLevel(logging.DEBUG)
    STREAM_HANDLER.setFormatter(FORMATTER)
    LOG.addHandler(STREAM_HANDLER)
    # В логгирование передаем имя текущей функции и имя вызвавшей функции
    LOG.debug('Отладочное сообщение')
