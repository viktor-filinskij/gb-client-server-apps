#!/usr/bin/env python3
__author__ = 'Viktor Filinskij'


import sys
import os
import collections
import unittest


sys.path.append(os.path.join(os.getcwd(), '..'))


from lib.constants import RESPONSE, ERROR, USER, ACCOUNT_NAME, TIME, ACTION, \
                          PRESENCE, TYPE, ACCOUNT_AUTH_STRING
from server import process_client_message, check_msg_has_required_fields, check_account


class TestServer(unittest.TestCase):
    '''
    В сервере только 1 функция для тестирования
    '''
    err_dict = {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }
    ok_dict = {
        RESPONSE: 200,
        ERROR: 'OK'
    }
    auth_required_dict = {
        RESPONSE: 401,
        ERROR: 'Authentication Required'
    }


    def test_no_action(self):
        """Ошибка если нет действия"""
        self.assertEqual(process_client_message(
            {TIME: '1.1', USER: {ACCOUNT_NAME: 'Guest'}}), self.err_dict)

    # """
    #
    # I can't understand why test expects 'None', if it must check result with err_dict
    # By some reason next test fails with folowing error:
    #
    # Ran 1 test in 0.005s
    #
    # FAILED (failures=1)
    #
    #
    # {'error': 'Bad Request', 'response': 400} != None
    #
    # Expected :None
    # Actual   :{'error': 'Bad Request', 'response': 400}
    # <Click to see difference>
    #
    # Traceback (most recent call last):
    #   File "C:\Program Files\JetBrains\PyCharm Community Edition 2020.2.2\plugins\python-ce\helpers\pycharm\teamcity\diff_tools.py", line 32, in _patched_equals
    #     old(self, first, second, msg)
    #   File "H:\Python\3.8.5\lib\unittest\case.py", line 912, in assertEqual
    #     assertion_func(first, second, msg=msg)
    #   File "H:\Python\3.8.5\lib\unittest\case.py", line 905, in _baseAssertEqual
    #     raise self.failureException(msg)
    # AssertionError: None != {'response': 400, 'error': 'Bad Request'}
    #
    # During handling of the above exception, another exception occurred:
    #
    # Traceback (most recent call last):
    #   File "H:\Python\3.8.5\lib\unittest\case.py", line 60, in testPartExecutor
    #     yield
    #   File "H:\Python\3.8.5\lib\unittest\case.py", line 676, in run
    #     self._callTestMethod(testMethod)
    #   File "H:\Python\3.8.5\lib\unittest\case.py", line 633, in _callTestMethod
    #     method()
    #   File "H:\PyCharmProjects\gb-client-server-apps\messenger\unit_tests\test_server.py", line 44, in test_wrong_action
    #     self.assertEqual(process_client_message(
    # """
    def test_wrong_action(self):
        """Ошибка если неизвестное действие"""
        self.assertEqual(process_client_message({ACTION: 'Wrong', TIME: '1.1', USER: {ACCOUNT_NAME: 'Guest'}}), self.err_dict)

    def test_no_time(self):
        """Ошибка, если  запрос не содержит штампа времени"""
        self.assertEqual(process_client_message(
            {ACTION: PRESENCE, USER: {ACCOUNT_NAME: 'Guest'}}), self.err_dict)

    def test_no_user(self):
        """Ошибка - нет пользователя"""
        self.assertEqual(process_client_message(
            {ACTION: PRESENCE, TIME: '1.1'}), self.err_dict)

    def test_unknown_user(self):
        """Ошибка - не Guest"""
        self.assertEqual(process_client_message(
            {ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest1', TYPE: 'Yep, I am here!'}}), self.auth_required_dict)

    def test_ok_check(self):
        """Корректный запрос"""
        self.assertEqual(process_client_message(
            {ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest'}}), self.ok_dict)

    def test_auth_ok(self):
        """Valid account"""
        self.assertEqual(check_account('C0deMaver1ck', 'CorrectHorseBatteryStaple'), True)

    def test_auth_wrong(self):
        """Valid account"""
        self.assertEqual(check_account('C0deMaver1ck', ''), 'Invalid Account')


if __name__ == '__main__':
    unittest.main()
