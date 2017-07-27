#!/usr/bin/env python
from __future__ import print_function

import unittest
import bigcli
from mock import patch, call


class ComponentFour(object):
    __args__ = [bigcli.arg('four_value')]
    def __init__(self, args):
        self.four_value = args.four_value


class ComponentThree(object):
    __args__ = [bigcli.arg('three_value')]

    def __init__(self, args):
        self.three_value = args.three_value


class ComponentTwo(object):
    __depends_on__ = [ComponentFour]

    def __init__(self, component_four):
        self.component_four = component_four


class ComponentOne(object):
    __depends_on__ = [ComponentTwo, ComponentThree]

    def __init__(self, component_two, component_three):
        self.component_two = component_two
        self.component_three = component_three


class Command(object):
    __depends_on__ = [ComponentOne]

    def __init__(self, component_one):
        self.component_one = component_one

    def __call__(self):
        print('four_value: {}'.format(self.component_one.component_two.component_four.four_value))
        print('three_value: {}'.format(self.component_one.component_three.three_value))


if __name__ == "__main__":
    bigcli.BigCli(commands=[Command]).execute()


class TestWithDeepObjectGraph(unittest.TestCase):

    @patch('tests.test_with_deep_object_graph.print')
    def test_with_deep_object_graph(self, print_mock):
        # When the object graph is deep it is hard to know what actual positional parameter will come
        # first, but you could find out with '-h'
        cli = bigcli.BigCli(commands=[Command]).execute(['command', 'abc', '123'])  # baby you and me girl

        print_mock.assert_has_calls([call('four_value: abc'), call('three_value: 123')])
