#!/usr/bin/python

'''!
Unit test for the Card class.

To execute the unit test from base dir location, enter:
@code
python tests/unittest_card.py [-v]
python tests/unittest_card.py TestCard.test_constructor
@endcode
@author <A email="fulkgl@gmail.com">George L Fulk</A>
'''

import unittest
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))[:-6]) #=dev first
from pybaccarat.playingcards import Card


class TestCard(unittest.TestCase):
    def test_constructor(self):
        # simple good value test
        c5s = Card(5, 's')
        self.assertIsNotNone(c5s, "normal 5s")

