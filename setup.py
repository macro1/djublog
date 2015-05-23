#!/usr/bin/env python
from setuptools import setup

setup(
    install_requires=[
        'defusedxml',
        'Django>=1.7',
        'lxml>=3.0',
        'requests>=1.0',
    ],
    name='djublog',
    packages=['djublog'],
    test_suite='runtests.main',
    tests_require=[
        'responses',
    ],
    version='0.1',
)
