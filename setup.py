#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'pinject'
]

setup(
    name='bigcli',
    version='0.2.0',
    description="A python framwork to write large CLIs using dependency injection",
    long_description=readme + '\n\n' + history,
    author="Duda Dornelles",
    author_email='duda@thoughtworks.com',
    url='https://github.com/dudadornelles/bigcli',
    packages=find_packages(include=['bigcli']),
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='bigcli',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
