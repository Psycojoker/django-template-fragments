#!/usr/bin/env/python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='django-template-fragments',
    version='0.1',
    author='Laurent Peuch',
    author_email='cortex@worlddomination.be',
    url='https://github.com/Psycojoker/django-template-fragments',
    packages=('fragments',),
    description="helper for templates used in javascript client framework: allow to store small django templates in a dir and generate a javascript object that contains them all as strings",
    long_description=open("README", "r").read(),
    license='MIT',
)
