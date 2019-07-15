#!/usr/bin/env python3
# coding: UTF-8


'''!
python -m pytest tests/test_file1.py
@author <A href="email:fulkgl@gmail.com">George L Fulk</A>
'''

#import unittest
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))[:-6]) #=dev first
import flask_edu_1.file1

def test_version(mocker, capsys):
    with capsys.disabled():
        print("Hi")
    assert 0.01 == flask_edu_1.file1.__version__

