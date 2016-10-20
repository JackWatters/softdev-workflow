"""
@author: tws
"""
import unittest

from softdev_model.system import BugEncounteredException, SoftwareSystem

from random import Random

from mock import Mock


class SoftwareSystemTest(unittest.TestCase):

    def setUp(self):
        self.software_system = SoftwareSystem()
        self.chunk_count = 0

    def complete_feature(self, logical_name, size, random):
        feature = self.software_system.add_feature(logical_name, size)
        while not feature.is_implemented:
            feature.extend(self.chunk_count, random)
            self.chunk_count += 1

        for test_logical_name in range(0, 30):
            feature.add_test(test_logical_name)

    def test_operate_test_debug_operate_regression(self):
        """
        Regression tests using a seed random value for repeatability.
        """

        random = Random()
        random.seed(1)

        for logical_name in range(0, 1):
            self.complete_feature(logical_name, 3, random)

        with self.assertRaises(BugEncounteredException):
            self.software_system.operate(random, 10000)

        self.assertEquals(3, len(self.software_system.last_trace))

        for test in self.software_system.tests:

            while True:
                try:
                    test.exercise()
                    break
                except BugEncounteredException as e:
                    test.feature.debug(random, e.bug)

        self.software_system.operate(random, 10000)
        self.assertEquals(10000, len(self.software_system.last_trace))


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'ChunkTest.testName']
    unittest.main()
