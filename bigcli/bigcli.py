# -*- coding: utf-8 -*-
import re
import argparse
import pinject


def commandize(class_name):
    """
    Turns a command class name into a cli style command.
    e.g: ExampleCommand -> example-comand
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', class_name)
    return re.sub('([a-z0-9])([A-Z])', r'\1-\2', s1).lower()


def init_parser(commands, *args, **kwargs):
    """
    TODO: docs
    """
    def get_all_args(dependencies):
        if not isinstance(dependencies, list):
            return dependencies.__dict__.get('__args__', [])
        if len(dependencies) == 0:
            return []
        else:
            return get_all_args(dependencies[0]) + \
                    get_all_args(dependencies[1:])

    parser = argparse.ArgumentParser(**kwargs)
    sp = parser.add_subparsers(dest='command')
    for command in commands:
        p = sp.add_parser(commandize(command.__name__))
        [arg_fn(p) for arg_fn in get_all_args(command.__depends_on__)]
    return parser


class BigCli(object):
    """
    TODO: docs
    """
    def __init__(self, commands, *args, **kwargs):
        self.__object_graph = None
        self.parser = init_parser(commands)

    def provide(self, clazz, parsed_args):
        """
        TODO: docs
        """
        class DipBindingSpec(pinject.BindingSpec):
            @pinject.provides(in_scope=pinject.PROTOTYPE)
            def provide_args(self):
                return parsed_args

        return pinject.new_object_graph(
            binding_specs=[DipBindingSpec()]).provide(clazz)


def arg(arg_action_name, *args, **kwargs):
    """
    TODO: docs
    """
    return lambda p: p.add_argument(arg_action_name, *args, **kwargs)
