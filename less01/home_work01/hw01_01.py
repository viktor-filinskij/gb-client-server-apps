#!/usr/bin/env python3
__author__ = 'Viktor Filinskij'

# Каждое из слов «разработка», «сокет», «декоратор» представить в строковом
# формате и проверить тип и содержание соответствующих переменных.
# Затем с помощью онлайн-конвертера преобразовать строковые представление
# в формат Unicode и также проверить тип и содержимое переменных.

WORD1_STR = 'разработка'
WORD2_STR = 'сокет'
WORD3_STR = 'декоратор'
WORD1_UTF8 = b'\xd1\x80\xd0\xb0\xd0\xb7\xd1\x80\xd0\xb0\xd0\xb1\xd0\xbe\xd1\x82\xd0\xba\xd0\xb0'
WORD2_UTF8 = b'\xd1\x81\xd0\xbe\xd0\xba\xd0\xb5\xd1\x82'
WORD3_UTF8 = b'\xd0\xb4\xd0\xb5\xd0\xba\xd0\xbe\xd1\x80\xd0\xb0\xd1\x82\xd0\xbe\xd1\x80'


def main():

    for var in [WORD1_STR, WORD2_STR, WORD3_STR, WORD1_UTF8, WORD2_UTF8, WORD3_UTF8]:
        if isinstance(var, str):
            print(f"String \"{var}\", type: {type(var)}")
        elif isinstance(var, bytes):
            print(f"Byte sequence \"{var.decode('utf-8', 'strict')}\", type: {type(var)}")


if __name__ == '__main__':
    main()
