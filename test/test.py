__author__ = 'joseph'

import sys
import os

p = lambda rel: os.path.join(os.path.dirname(__file__), rel)

sys.path.insert(0,p('../src'))
sys.path.insert(0,p('../src/DebugChannel.py'))
sys.path.insert(0,p('./DebugChannelTest.py'))

#print "\n".join(sys.path)
from DebugChannelTest import DebugChannelTest
import unittest


if __name__ == '__main__':
    unittest.main()
