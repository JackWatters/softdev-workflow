'''
Created on 20 Mar 2016

@author: Tim
'''
import unittest

from mock import Mock

from models.systems.software.bug import Bug, BugEncounteredException
from models.systems.software.feature import Feature
from models.systems.software.test import Test

class TestTest(unittest.TestCase):


    def setUp(self):
        self.mock_feature = Mock(spec=Feature)
        self.fixture = Test(self.mock_feature)


    def tearDown(self):
        pass


    def testExerciseAndFail(self):
        self.mock_bug = Mock(spec=Bug)
        self.mock_bug.id = 1
        self.mock_bug.pfd = 1.0
        self.mock_feature.bugs = [self.mock_bug]
        with self.assertRaises(BugEncounteredException):
            self.fixture.exercise()
        pass


    def testExerciseAndPass(self):
        self.mock_bug = Mock(spec=Bug)
        self.mock_bug.id = 1
        self.mock_bug.pfd = 0.0
        self.mock_feature.bugs = [self.mock_bug]

        self.fixture.exercise()
        pass
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()