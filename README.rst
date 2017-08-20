======
bigcli
======


.. image:: https://img.shields.io/pypi/v/bigcli.svg
        :target: https://pypi.python.org/pypi/bigcli

.. image:: https://img.shields.io/travis/dudadornelles/bigcli.svg
        :target: https://travis-ci.org/dudadornelles/bigcli

.. image:: https://readthedocs.org/projects/bigcli/badge/?version=latest
        :target: https://bigcli.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/dudadornelles/bigcli/shield.svg
     :target: https://pyup.io/repos/github/dudadornelles/bigcli/
     :alt: Updates


A python framework to write large CLIs. The concept is to automagically derive CLI commands and args based on the object graph of a callable class that implements a CLI command (command name is derived from the class name). It uses argparse_ to create the CLI parser and pinject_ as the Dependency_Injection_ engine. You implement a class - e.g.: ``DoSomething``- and that generates the name of a subcommand - e.g: ``do-something``. Then, based on the dependencies of class ``DoSomething``, we will derive the arguments, e.g.: if ``DoSomething`` depends on ``Dependency``, which in turn declares ``__args__ = [bigcli.arg('--option', required=False, help='help')]`` (add_argument_ method from argparse_), then command ``do-something`` will have a '--option' argument.

In theory, the auto-generation of arguments should enables and encourage the reuse of internal components for rapid development of consistent and testable rich CLIs, especially those that operate platforms.

* Free software: MIT license
* Documentation: https://bigcli.readthedocs.io.

Minimal example:
-------

.. code-block:: python

   #!/usr/bin/env python
   import bigcli
 
 
   class Dependency(object):
       __args__ = [bigcli.arg('--option')]
 
       def __init__(self, args):
           self.option = args.option
 
 
   class Command(object):
       __parent__ = 'sub-command'
       __depends_on__ = [Dependency]
 
       def __init__(self, dependency):
           self.dependency = dependency
 
       def __call__(self):
           print "dependency option: {}".format(self.dependency.option)
 
 
   if __name__ == "__main__":
       bigcli.BigCli(commands=[Command]).execute()
 
 
   # $ ./example.py sub-command command --option value
   # > dependency option: value
 
 
Features (see tests for example)
--------

* Auto generates parsers and commands using the ``__depends_on__`` and ``__args__`` attributes.
* Supports adding single subcommand using the ``__parent__ = 'subcommand'`` attribute.

Known Issues:
-------------

* Only supports python 2.7 because pinject_ only supports python 2.7.
* Class names should have more than a single letter (pinject know issue, not documented anywhere AFAIK).

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.
.. _Dependency_Injection: https://en.wikipedia.org/wiki/Dependency_injection
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _add_argument: https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.add_argument
.. _argparse: https://docs.python.org/2/howto/argparse.html
.. _pinject: https://github.com/google/pinject
