from __future__ import print_function
from mock import patch, call
import unittest

import bigcli

class DomainObject(object):
    __args__ = [
        bigcli.arg('--password', help='the password', required=True),
        bigcli.arg('value', help='a value')
    ]

    def __init__(self, args):
       self.password = args.password
       self.value = args.value


class ExampleCommand(object):
    __depends_on__ = [DomainObject]

    def __init__(self, domain_object):
        self.domain_object = domain_object

    def __call__(self, *args, **kwargs):
        print(self.domain_object.password)
        print(self.domain_object.value)


class TestBigcli(unittest.TestCase):

    def test_creates_parser_and_provides_complete_command_object(self):
        cli = bigcli.BigCli(commands=[ExampleCommand])

        parsed_args = cli.parser.parse_args(['example-command', 'a_value', '--password', 'notmypassword'])
        self.assertEqual('a_value', parsed_args.value)
        self.assertEqual('notmypassword', parsed_args.password)

        command_object = cli._provide(ExampleCommand, parsed_args)

        self.assertEqual('a_value', command_object.domain_object.value)
        self.assertEqual('notmypassword', command_object.domain_object.password)

    @patch('tests.test_bigcli.print')
    def test_execute(self, print_mock):
        bigcli.BigCli(commands=[ExampleCommand]).execute(['example-command', 'a_value', '--password', 'notmypassword'])

        print_mock.assert_has_calls([call('notmypassword'), call('a_value')])
       
