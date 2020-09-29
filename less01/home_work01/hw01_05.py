#!/usr/bin/env python
__author__ = 'Viktor Filinskij'

# Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать
# результаты из байтовового в строковый тип на кириллице.

import subprocess


COMMAND = 'ping'
COMMAND_PARAMS = '-c 4'
destination = ['yandex.ru', 'youtube.com']


def main():
    for target in destination:
        completed_process = subprocess.run([COMMAND, COMMAND_PARAMS, target],
                                           check=True,
                                           encoding='utf-8',
                                           capture_output=True).stdout
        print(completed_process)


if __name__ == '__main__':
    main()
