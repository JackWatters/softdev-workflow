"""
@author: tws
"""
import unittest
from models.systems.software.softwaresystem import SoftwareSystem
from random import Random
from models.systems.software.bug import BugEncounteredException


class SoftwareSystemTest(unittest.TestCase):
    def setUp(self):
        self.software_system = SoftwareSystem()

    def complete_feature(self, random, size):
        feature = self.software_system.add_feature(size)
        while not feature.is_implemented:
            feature.extend(random)
        for _ in range(0, 30):
            self.software_system.add_test(feature)

    def test_operate_test_debug_operate_regression(self):
        '''
        Regression test using a seed random value for repeatability.
        '''

        rand = Random()
        rand.seed(1)

        for _ in range(0, 1):
            self.complete_feature(rand, 3)

        with self.assertRaises(BugEncounteredException) as e:
            self.software_system.operate(rand, 10000)

        self.assertEquals(10, len(self.software_system.successful_operations))

        for test in self.software_system.tests:
            test_failing = True

            while test_failing:
                try:
                    test.exercise()
                    test_failing = False
                except BugEncounteredException as e:
                    test.feature.debug(rand, e.bug)

        self.software_system.operate(rand, 10000)
        self.assertEquals(10000, len(self.software_system.successful_operations))


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'ChunkTest.testName']
    unittest.main()
