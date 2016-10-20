"""
Created on 20 Mar 2016

@author: twsswt
"""
import unittest

from mock import Mock

from softdev_model.system import Bug, BugEncounteredException, Chunk, Feature, SoftwareSystem, Test


class TestTest(unittest.TestCase):

    def setUp(self):

        self.mock_feature = Mock(spec=Feature)

        self.fixture = Test(0, self.mock_feature)

        self.mock_chunk = Mock(spec=Chunk)
        self.mock_chunk.logical_name = 1

        self.mock_feature.chunks = [self.mock_chunk]
        self.mock_feature.size = 3
        self.mock_feature.software_system = Mock(spec=SoftwareSystem)
        self.mock_feature.software_system.test_efficiency = 1.0

        self.mock_bug = Mock(spec=Bug)
        self.mock_bug._logical_name = 1
        self.mock_feature.bugs = [self.mock_bug]
        self.mock_chunk.bugs = self.mock_feature.bugs

    def test_exercise_and_fail(self):
        self.mock_feature.software_system.test_effectiveness = 1.0

        with self.assertRaises(BugEncounteredException):
            self.fixture.exercise()
        pass

    def test_exercise_and_pass(self):
        self.mock_feature.software_system.test_effectiveness = 0.0

        self.fixture.exercise()


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
