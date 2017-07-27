#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `bigcli` package."""


import unittest
from click.testing import CliRunner

from bigcli import bigcli
from bigcli import cli

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
        pass


class TestBigcli(unittest.TestCase):

    def test_creates_parser_and_provides_complete_command_object(self):
        cli = bigcli.BigCli(commands=[ExampleCommand])

        parsed_args = cli.parser.parse_args(['example-command', 'a_value', '--password', 'notmypassword'])
        self.assertEqual('a_value', parsed_args.value)
        self.assertEqual('notmypassword', parsed_args.password)

        command_object = cli.provide(ExampleCommand, parsed_args)

        self.assertEqual('a_value', command_object.domain_object.value)
        self.assertEqual('notmypassword', command_object.domain_object.password)

