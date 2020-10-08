#!/usr/bin/env python3
__author__ = 'Viktor Filinskij'

"""
3. Задание на закрепление знаний по модулю yaml.
 Написать скрипт, автоматизирующий сохранение данных
 в файле YAML-формата.
Для этого:

Подготовить данные для записи в виде словаря, в котором
первому ключу соответствует список, второму — целое число,
третьему — вложенный словарь, где значение каждого ключа —
это целое число с юникод-символом, отсутствующим в кодировке
ASCII(например, €);

Реализовать сохранение данных в файл формата YAML — например,
в файл file.yaml. При этом обеспечить стилизацию файла с помощью
параметра default_flow_style, а также установить возможность работы
с юникодом: allow_unicode = True;

Реализовать считывание данных из созданного файла и проверить,
совпадают ли они с исходными.
"""

import os
import yaml  # from module pyyaml


# Store data in current workdir
data_store = os.path.join(os.getcwd(), 'file.yaml')


# stolen from: https://stackoverflow.com/questions/25108581/python-yaml-dump-bad-indentation
# format yml with indents
class MyDumper(yaml.Dumper):

    def increase_indent(self, flow=False, indentless=False):
        return super(MyDumper, self).increase_indent(flow, False)


def prepare_data(*args, **kwargs):

    data = dict(my_list=args[0],
                my_int=int(args[1]),
                my_dict={el: ord(val) for el,val in kwargs.items()})

    return data


def save_data_to_file(file, data):

    with open(file, 'w+', encoding='utf-8') as data_file:
       yaml.dump(data, Dumper=MyDumper, stream=data_file, allow_unicode=True)


def main():
    # store test data in file.yaml under current work directory
    data = prepare_data(['one', '1', ['1.1'], [['1.1.1'], ['i am string']],
                         'two', '2', ['2.1', '2.2'], 'three', {"Checking-UTF8":'Кириллица'}],
                        1,
                        key1='€', key2='Ð', key3='A')
    save_data_to_file(data_store, data)

    # Chek stored data:
    with open(data_store, 'r', encoding='utf-8') as f_n:
        doc = yaml.load(f_n, Loader=yaml.FullLoader)

        result = yaml.dump(doc, Dumper=MyDumper, sort_keys=True, allow_unicode=True)
        print(result)


if __name__ == '__main__':
    main()
