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


A python framework to write large CLIs


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

