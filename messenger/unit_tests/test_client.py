#!/usr/bin/env python3
__author__ = 'Viktor Filinskij'


import os
import sys
import unittest


sys.path.append(os.path.join(os.getcwd(), '..'))

from lib.constants import RESPONSE, ERROR, USER, ACCOUNT_NAME, TIME, ACTION, \
                          PRESENCE, TYPE, ERROR
from client import create_presence, process_ans


class TestClass(unittest.TestCase):
    '''
    Класс с тестами
    '''

    def test_def_presense(self):
        """Тест коректного запроса"""
        # {'action': 'presence', 'time': 1573760672.167031, 'user': {'account_name': 'Guest'}}
        test = create_presence()
        test[TIME] = 1.1  # время необходимо приравнять принудительно
                          # иначе тест никогда не будет пройден
        self.assertEqual(test, {ACTION: PRESENCE, TYPE: 'status', TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest', TYPE: 'Yep, I am here!'}})

    def test_200_ans(self):
        """Тест корректтного разбора ответа 200"""
        self.assertEqual(process_ans({RESPONSE: 200, ERROR: 'OK'}), '200 : OK')

    def test_400_ans(self):
        """Тест корректного разбора 400"""
        self.assertEqual(process_ans({RESPONSE: 400, ERROR: 'Bad Request'}), '400 : Bad Request')

    def test_no_response(self):
        """Тест исключения без поля RESPONSE"""
        self.assertRaises(ValueError, process_ans, {ERROR: 'Bad Request'})


def main():
    pass


if __name__ == '__main__':
    unittest.main()
