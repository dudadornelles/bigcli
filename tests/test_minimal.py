from __future__ import print_function
from mock import mock, patch
import unittest

import bigcli


class HiStranger(object):
    def __call__(self):
        print('Hi Stranger')


class ByeStranger(object):
    def __call__(self):
        print('Bye Stranger')


class TestMinimal(unittest.TestCase):

    @patch('tests.test_minimal.print')
    def test_minimal_cli(self, print_mock):
        cli = bigcli.BigCli(commands=[HiStranger, ByeStranger])

        cli.execute(['hi-stranger'])
        print_mock.assert_called_with('Hi Stranger')

        cli.execute(['bye-stranger'])
        print_mock.assert_called_with('Bye Stranger')
