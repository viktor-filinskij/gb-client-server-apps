#!/usr/bin/env python
__author__ = 'Viktor Filinskij'

# Преобразовать слова «разработка», «администрирование», «protocol», «standard»
# из строкового представления в байтовое и выполнить обратное преобразование
# (используя методы encode и decode).

words = ['разработка', 'администрирование', 'protocol', 'standard']
words_encoded = []
words_decoded = []


def main():

    for word in words:
        words_encoded.append(word.encode("utf-8", "strict"))

    print(f"{words_encoded}")

    for word in words_encoded:
        words_decoded.append(word.decode("utf-8", "strict"))

    print(f"{words_decoded}")


if __name__ == '__main__':
    main()
