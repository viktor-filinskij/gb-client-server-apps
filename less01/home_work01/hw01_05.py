#!/usr/bin/env python
__author__ = 'Viktor Filinskij'

# Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать
# результаты из байтовового в строковый тип на кириллице.

import subprocess

from sys import platform


COMMAND = 'ping'
destination = ['yandex.ru', 'youtube.com']

# by default on nix platforms ping runs infinite, so need to limit echoes
# but on win platforms ping use different args :
if platform == "win32":
    COMMAND_PARAMS = '-n 4'
else:
    COMMAND_PARAMS = '-c 4'


def main():
    for target in destination:
        completed_process = subprocess.run([COMMAND, COMMAND_PARAMS, target],
                                           check=True,
                                           encoding='utf-8',
                                           capture_output=True).stdout
        print(completed_process)


if __name__ == '__main__':
    main()
