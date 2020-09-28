#!/usr/bin/env python3
__author__ = 'Viktor Filinskij'

# Каждое из слов «class», «function», «method» записать в байтовом типе
# без преобразования в последовательность кодов
# (не используя методы encode и decode) и определить тип, содержимое и длину
# соответствующих переменных.

WORD1_UTF8 = b'\x63\x6c\x61\x73\x73'
WORD2_UTF8 = b'\x66\x75\x6e\x63\x74\x69\x6f\x6e'
WORD3_UTF8 = b'\x6d\x65\x74\x68\x6f\x64'


def main():

    for var in [WORD1_UTF8, WORD2_UTF8, WORD3_UTF8]:
        print(f"Byte sequence \"{var.decode('utf-8', 'strict')}\", "
              f"type: {type(var)}, "
              f"length: {len(var)}"
              )


if __name__ == '__main__':
    main()
