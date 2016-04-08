'''
Created on 8 Apr 2016

@author: Janion
'''
import sys
sys.path.insert(0, 'C:\\Users\\Janion\\git\\TimeMan\\src')

import unittest
import os
from processing.Logic import Logic

class Test(unittest.TestCase):

    testDataFolder = "tmp"

    def setUp(self):
        os.mkdir(self.testDataFolder)
        self.logic = Logic()


    def tearDown(self):
        os.rmdir(self.testDataFolder)


    def testShouldFindFiles(self):
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()