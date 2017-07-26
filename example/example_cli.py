#!/usr/bin/env python
import unittest
from click.testing import CliRunner

from bigcli import bigcli
from bigcli import cli

class AClient(object):
    __args__ = [
        bigcli.arg('--foo', help='foo help', required=True),
        bigcli.arg('bar', help='bar help')
    ]

    def __init__(self, args):
       self.foo = args.foo
       self.bar = args.bar


class Command(object):
    __depends_on__ = [AClient]

    def __init__(self, a_client):
        self.a_client = a_client

    def __call__(self, *args, **kwargs):
        pass


bigcli.BigCli(commands=[Command]).parser.parse_args()
