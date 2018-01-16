# -*- coding: utf-8 -*-
import re
import argparse
import pinject
import pydoc
from sys import exit


def commandize(class_name):
    """
    Turns a command class name into a cli style command.
    e.g: ExampleCommand -> example-comand
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', class_name)
    return re.sub('([a-z0-9])([A-Z])', r'\1-\2', s1).lower()


class ShortHelpAction(argparse.Action):
    def __init__(self, option_strings, dest, **kwargs):
        super(ShortHelpAction, self).__init__(option_strings, dest, nargs=0, help='print usage')

    def __call__(self, parser, namespace, values, option_string=None):
        parser.print_help()
        exit(0)


class ExtendedHelpAction(argparse.Action):
    def __init__(self, option_strings, dest, **kwargs):
        super(ExtendedHelpAction, self).__init__(option_strings, dest, nargs=0,
                                                 help='Print extended help')

    def __call__(self, parser, namespace, values, option_string=None):
        command_class = parser._defaults.get('__bigcli_meta_command_class')
        if command_class and command_class.__doc__:
            pydoc.pager(command_class.__doc__)
        else:
            parser.print_usage()
        exit(0)


class BigCli(object):
    """
    TODO: docs
    """
    def __init__(self, commands, *args, **kwargs):
        self._commands = {}
        self.parser = self._init_parser(commands, **kwargs)

    def execute(self, args=None):
        """
        TODO: docs
        """
        parsed_args = self.parser.parse_args(args) if args else self.parser.parse_args()
        command_class = self._commands[parsed_args.command]
        if parsed_args.__dict__.get('subcommand'):
            command_class = command_class[parsed_args.subcommand]
        self._provide(command_class, parsed_args)()

    def _register_command_class(self, command_name, command_class):
        self._commands[command_name] = command_class

    def _init_parser(self, commands, **kwargs):
        def get_all_args(dependencies):
            if len(dependencies) == 0:
                return []

            args = dependencies[0].__dict__.get('__args__', [])
            command_dependencies = dependencies[0].__dict__.get('__depends_on__', [])

            return args + get_all_args(command_dependencies + dependencies[1:])  # return any arg the command may have plus get_all_args for all dependencies

        help_parser = argparse.ArgumentParser(add_help=False)
        help_parser.add_argument('--help', action=ExtendedHelpAction)
        help_parser.add_argument('-h', action=ShortHelpAction)
        kwargs['add_help'] = False
        kwargs['parents'] = [help_parser]

        parser = argparse.ArgumentParser(**kwargs)
        sp = parser.add_subparsers(dest='command')
            
        def mkhelpparser(command_class):
            help_parser = argparse.ArgumentParser(add_help=False)
            help_parser.add_argument('--help', action=ExtendedHelpAction)
            help_parser.add_argument('-h', action=ShortHelpAction)
            help_parser._defaults.update({'__bigcli_meta_command_class': command_class})
            return help_parser

        for command_class in commands:
            actual_command_name = commandize(command_class.__name__)

            if command_class.__dict__.get('__parent__'):
                # register class as a subcommand of __parent__
                parent_command = command_class.__dict__.get('__parent__')
                if not self._commands.get(parent_command):
                    self._commands[parent_command] = {} 
                self._commands[parent_command][actual_command_name] = command_class

                ssp = sp.add_parser(name=parent_command)
                sssp = ssp.add_subparsers(dest='subcommand') 
                p = sssp.add_parser(actual_command_name, parents=[help_parser], add_help=False)
            else:
                # register class as command
                self._register_command_class(actual_command_name, command_class)

                # init parser for command name
                p = sp.add_parser(actual_command_name, parents=[mkhelpparser(command_class)], add_help=False)

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
