#!/usr/bin/env python
__author__ = 'Viktor Filinskij'

# Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать
# результаты из байтовового в строковый тип на кириллице.

import subprocess

from sys import platform


COMMAND = 'ping'
destination = ['yandex.ru', 'youtube.com']


def main():

    # by default on nix platforms ping runs infinite, so need to limit echoes
    # but on win32 platforms ping use different args :
    for target in destination:
        if platform == "win32":
            completed_process = subprocess.run([COMMAND, '-n', '4', target],
                                               check=True,
                                               encoding='utf-8',
                                               capture_output=True).stdout
        else:
            completed_process = subprocess.run([COMMAND, '-c', '4', target],
                                               check=True,
                                               encoding='utf-8',
                                               capture_output=True).stdout
        print(completed_process)


if __name__ == '__main__':
    main()
