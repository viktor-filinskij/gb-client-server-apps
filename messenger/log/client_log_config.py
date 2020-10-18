#!/usr/bin/env python3
__author__ = 'Viktor Filinskij'


"""
Простейшее логгирование
"""

import logging
import os


from logging.handlers import TimedRotatingFileHandler
# Создаём объект-логгер с именем app.main
LOG = logging.getLogger(__name__)

# Создаём объект форматирования:
FORMATTER = logging.Formatter(f"%(asctime)s - %(levelname)s - {LOG.name} - %(message)s ")

if os.name == 'posix':
    LOG_FILE = os.path.join(os.getcwd(), f"../logs/{LOG.name}.log")
elif os.name == 'nt':
    LOG_FILE = os.path.join(os.getcwd(), f"..\\logs\\{LOG.name}.log")


# Создаём файловый обработчик логгирования (можно задать кодировку):
FILE_HANDLER = TimedRotatingFileHandler(LOG_FILE, when='D', interval=1,
                                        backupCount='7', encoding='utf-8')
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

if __name__ == '__main__':
    main()
