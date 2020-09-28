#!/usr/bin/env python3
__author__ = 'Viktor Filinskij'

# Каждое из слов «разработка», «сокет», «декоратор» представить в строковом
# формате и проверить тип и содержание соответствующих переменных.
# Затем с помощью онлайн-конвертера преобразовать строковые представление
# в формат Unicode и также проверить тип и содержимое переменных.

word1_str = 'разработка'
word2_str = 'сокет'
word3_str = 'декоратор'
word1_utf8 = b'\xd1\x80\xd0\xb0\xd0\xb7\xd1\x80\xd0\xb0\xd0\xb1\xd0\xbe\xd1\x82\xd0\xba\xd0\xb0'
word2_utf8 = b'\xd1\x81\xd0\xbe\xd0\xba\xd0\xb5\xd1\x82'
word3_utf8 = b'\xd0\xb4\xd0\xb5\xd0\xba\xd0\xbe\xd1\x80\xd0\xb0\xd1\x82\xd0\xbe\xd1\x80'


def main():
    print(f"String \"{word1_str}\", type: {type(word1_str)}")
    print(f"String \"{word2_str}\", type: {type(word2_str)}")
    print(f"String \"{word3_str}\", type: {type(word3_str)}")
    print(f"Byte sequence \"{word1_utf8.decode('utf-8', 'strict')}\", type: {type(word1_utf8)}")
    print(f"Byte sequence \"{word2_utf8.decode('utf-8', 'strict')}\", type: {type(word2_utf8)}")
    print(f"Byte sequence \"{word3_utf8.decode('utf-8', 'strict')}\", type: {type(word3_utf8)}")


if __name__ == '__main__':
    main()
