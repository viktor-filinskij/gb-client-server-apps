#!/usr/bin/env python3
__author__ = 'Viktor Filinskij'

# Создать текстовый файл test_file.txt, заполнить его тремя строками:
# «сетевое программирование», «сокет», «декоратор».
# Проверить кодировку файла по умолчанию.
# Принудительно открыть файл в формате Unicode и вывести его содержимое.

import os


lines = ['сетевое программирование', 'сокет', 'декоратор']
FILE_NAME = 'test_file.txt'


def main():

    with open(os.path.join(os.getcwd(), FILE_NAME), 'w+', encoding="utf-8") as test_file:
        for line in lines:
            test_file.write(line)
            test_file.write('\n')

        test_file.seek(0, 0)

        for line in test_file:
            print(line, end='')


if __name__ == '__main__':
    main()
