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


class BigCli(object):
    """
    TODO: docs
    """
    def __init__(self, commands, *args, **kwargs):
        self.__commands = {}
        self.parser = self._init_parser(commands, **kwargs)

    def execute(self, args=None):
        """
        TODO: docs
        """
        parsed_args = self.parser.parse_args(args) if args else self.parser.parse_args()
        command_class = self.__commands[parsed_args.command]
        self._provide(command_class, parsed_args)()

    def _register_command_class(self, command_name, command_class):
        self.__commands[command_name] = command_class

    def _init_parser(self, commands, **kwargs):
        def get_all_args(dependencies):
            if len(dependencies) == 0:
                return []

            args = dependencies[0].__dict__.get('__args__', [])
            command_dependencies = dependencies[0].__dict__.get('__depends_on__', [])

            return args + get_all_args(command_dependencies + dependencies[1:])  # return any arg the command may have plus get_all_args for all dependencies

        parser = argparse.ArgumentParser(**kwargs)
        sp = parser.add_subparsers(dest='command')

        for command_class in commands:
            # register class as command
            actual_command_name = commandize(command_class.__name__)
            self._register_command_class(actual_command_name, command_class)

            # init parser for command name
            p = sp.add_parser(actual_command_name)

            # get all lambda args recursively and apply them to the new parser
            all_lambda_args = get_all_args([command_class])
            [arg_fn(p) for arg_fn in all_lambda_args]
        return parser

    def _provide(self, clazz, parsed_args, extra_binding_specs=None):
        class DipBindingSpec(pinject.BindingSpec):
            @pinject.provides(in_scope=pinject.PROTOTYPE)
            def provide_args(self):
                return parsed_args

        binding_specs = [DipBindingSpec()] + (extra_binding_specs or [])
        return pinject.new_object_graph(binding_specs=binding_specs).provide(clazz)


def arg(arg_action_name, *args, **kwargs):
    """
    TODO: docs
    """
    return lambda p: p.add_argument(arg_action_name, *args, **kwargs)
