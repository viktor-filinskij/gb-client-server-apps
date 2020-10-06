#!/usr/bin/env python3
__author__ = 'Viktor Filinskij'

# 1. Задание на закрепление знаний по модулю CSV. Написать скрипт,
# осуществляющий выборку определенных данных из файлов info_1.txt, info_2.txt,
# info_3.txt и формирующий новый «отчетный» файл в формате CSV.
# Для этого:
#
# Создать функцию get_data(), в которой в цикле осуществляется перебор
# файлов с данными, их открытие и считывание данных. В этой функции из
# считанных данных необходимо с помощью регулярных выражений извлечь значения
# параметров «Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».
# Значения каждого параметра поместить в соответствующий список.
# Должно получиться четыре списка — например, os_prod_list, os_name_list,
# os_code_list, os_type_list.
# В этой же функции создать главный список для хранения данных отчета — например,
# main_data — и поместить в него названия столбцов отчета в виде списка:
# «Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».
# Значения для этих столбцов также оформить в виде списка и поместить
# в файл main_data (также для каждого файла);
# Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл.
# В этой функции реализовать получение данных через вызов функции get_data(),
# а также сохранение подготовленных данных в соответствующий CSV-файл;
# Проверить работу программы через вызов функции write_to_csv().

import os
import re

from chardet.universaldetector import UniversalDetector


patterns = ['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']
file_list = ['info_1.txt', 'info_2.txt', 'info_3.txt']
# ENC = "utf-8"


def get_data(*args):
    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []
    main_data = [args[0]]

    def check_enc(filename):
        detector = UniversalDetector()
        detector.reset()

        with open(os.path.join(os.getcwd(), filename), 'rb') as f_n:
            for line in f_n:
                detector.feed(line)
                if detector.done:
                    break
            detector.close()

        return detector.result.get('encoding')

    def get_pattern(pat, filename):
        pass

    for keyword in args[0]:
        result = []
        # we extend basic pattern with ":" and following whitespaces
        pattern = keyword + r':\s*(.*)'
        # configure patterns to search for
        patt = re.compile(pattern)

        for file in args[1]:
            with open(os.path.join(os.getcwd(), file), 'r',
                      encoding=check_enc(file)) as f_n:
                for line in f_n:
                    # in each file line
                    match = patt.match(line)
                    if match:
                        # print(f"Match found: {line[match.end():]}")
                        result.append(match.group(1))

        if keyword == 'Изготовитель системы':
            os_prod_list.append(result)
            main_data.extend(os_prod_list)
        elif keyword == 'Название ОС':
            os_name_list.append(result)
            main_data.extend(os_name_list)
        elif keyword == 'Код продукта':
            os_code_list.append(result)
            main_data.extend(os_code_list)
        elif keyword == 'Тип системы':
            os_type_list.append(result)
            main_data.extend(os_type_list)

    return main_data


def write_to_csv():
    pass


def main():
    main_data = get_data(patterns, file_list)
    print(main_data)


if __name__ == '__main__':
    main()
