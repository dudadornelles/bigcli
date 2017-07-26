# -*- coding: utf-8 -*-
import pinject
import argparse


def _get_all_args(dependencies):
    if not isinstance(dependencies, list):
        return dependencies.__dict__.get('__args__', [])
    if len(dependencies) == 0:
        return []
    else:
        return _get_all_args(dependencies[0]) + _get_all_args(dependencies[1:])


def init_parser(commands, *args, **kwargs):
    parser = argparse.ArgumentParser(**kwargs)
    sp = parser.add_subparsers(dest='command')
    for command in commands:
        p = sp.add_parser(command.__name__)
        [arg_fn(p) for arg_fn in _get_all_args(command.__depends_on__)]
    return parser


class BigCli(object):
    def __init__(self, commands, *args, **kwargs):
        self.__object_graph = None
        self.parser = init_parser(commands)

    @property
    def object_graph(self):
        if not self.__object_graph:
            self.__object_graph = pinject.new_object_graph()
        return self.__object_graph

    def provide(self, clazz):
        return self.object_graph.provide(clazz)


def arg(arg_action_name, *args, **kwargs):
    return lambda p: p.add_argument(arg_action_name, *args, **kwargs)
