#!/usr/bin/env python3
__author__ = 'Viktor Filinskij'

# Определить, какие из слов «attribute», «класс», «функция», «type»
# невозможно записать в байтовом типе.

# это работает
WORD1 = b'\x61\x74\x74\x72\x69\x62\x75\x74\x65'  # attribute
WORD2 = b'\xd0\xba\xd0\xbb\xd0\xb0\xd1\x81\xd1\x81'  # класс
WORD3 = b'\xd1\x84\xd1\x83\xd0\xbd\xd0\xba\xd1\x86\xd0\xb8\xd1\x8f'  # функция
WORD4 = b'\x74\x79\x70\x65'  # type

# WORD1 = b'attribute'
# WORD2 = b'класс'  # это не работает SyntaxError: bytes can only contain ASCII literal characters.
# WORD3 = b'функция'  # - // -
# WORD4 = b'type'


def main():

    # преобразуем заданные слова в байт-последовательность
    # выводим на экран слова «attribute», «класс», «функция», «type»
    for word in ['attribute', 'класс', 'функция', 'type']:
        print(f"Word {word} as byte sequence: {word.encode('utf-8', 'strict')}")

    # выводим на экран слова «attribute», «класс», «функция», «type»
    # определённые ранее как тип byte
    for var in [WORD1, WORD2, WORD3, WORD4]:
        print(f"Byte sequence: \"{var.decode('utf-8', 'strict')}\", "
              f"type: {type(var)}, "
              f"length: {len(var)}")


if __name__ == '__main__':
    main()
