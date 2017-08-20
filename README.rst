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


A python framework to write large CLIs. The concept is to automagically derive CLI commands and args based on classes that you implement and their dependencies. It uses argparse_ to create the CLI parser and pinject_ as the DI engine. You implement a class - e.g.: ``DoSomething``- and that generates the name of a subcommand - e.g: ``do-something``. Then, based on the dependencies for the class ``DoSomething``, we will derive the arguments, e.g.: ``DoSomething`` depends on ``Dependency``, which in turn declares ``__args__ = [bigcli.arg('--option', required=False, help='help')]`` (add_argument_ method from argparse_), that will add these arguments to the command ``do-something``, all based in the object graph.

The auto-generation of args enables and encourages the reuse of internal components for rapid and consistent development of rich CLIs, especially those that operate platforms.

.. _add_argument: https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.add_argument
.. _argparse: https://docs.python.org/2/howto/argparse.html
.. _pinject: https://github.com/google/pinject

* Free software: MIT license
* Documentation: https://bigcli.readthedocs.io.


Example
-------

.. code-block:: python

   #!/usr/bin/env python
   import bigcli
 
 
   class WhoMoves(object):
       __args__ = [bigcli.arg('--who-moves', default="she")]
 
       def __init__(self, args):
           self.who = args.who_moves
 
 
   class InTheWay(object):
       __depends_on__ = [WhoMoves]
 
       def __init__(self, who_moves):
           self.who = who_moves.who
 
       def __call__(self):
           print "{} moves".format(self.who)
 
 
   if __name__ == "__main__":
       bigcli.BigCli(commands=[InTheWay]).execute()
 
 
   # $ ./something.py in-the-way --who-moves
   # > she moves
 
 
Features
--------

* Auto generates parsers and commands
* Allows for reuse of components through dependency injection

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

