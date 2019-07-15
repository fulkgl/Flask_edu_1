#!/usr/bin/env python3
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
#--
import os,sys,unittest
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))) #=dev first
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+"/flask_edu_1")
from flask_edu_1.file1 import __version__
#--

def readme(filespec):
    '''Utility to return readme contents for long description'''
    with open(filespec) as f:
        return f.read()

setup(
    name='flask_edu_1',
    version=__version__,
    url='https://github.com/fulkgl/Flask_edu_1',
    download_url='https://pypi.python.org/packages/source/F/flask_edu_1/'+\
        'flask_edu_1-%s.tar.gz' % __version__,
    description='Flask education 1',
    long_description=readme('README.md'),
    author='George L Fulk',
    author_email='fulkgl@gmail.com',
    maintainer='George L Fulk',
    maintainer_email='fulkgl@gmail.com',
    license='MIT',
    packages=['flask_edu_1'],
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
)
