__author__ = 'joseph'

import sys
import os

sys.path.insert(0,os.path.abspath('../src'))
sys.path.insert(0,os.path.abspath('../src/ChannelDebug.py'))
sys.path.insert(0,os.path.abspath('./ChannelDebugTest.py'))

#print "\n".join(sys.path)
from ChannelDebugTest import ChannelDebugTest
import unittest


if __name__ == '__main__':
    unittest.main()
