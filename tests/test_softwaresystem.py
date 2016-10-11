"""
@author: tws
"""
import unittest

from softdev_model.system import BugEncounteredException, Developer, SoftwareSystem

from random import Random

from mock import Mock


class SoftwareSystemTest(unittest.TestCase):
    def setUp(self):
        self.software_system = SoftwareSystem()
        self.chunk_count = 0

        self.developer_mock = Mock(spec=Developer)
        self.developer_mock.logical_name = "bob"

    def complete_feature(self, random, size, logical_name):
        feature = self.software_system.add_feature(logical_name, size)
        while not feature.is_implemented:
            feature.extend(self.chunk_count, self.developer_mock, random)
            self.chunk_count += 1

        for _ in range(0, 30):
            self.software_system.add_test(feature)

    def test_operate_test_debug_operate_regression(self):
        """
        Regression tests using a seed random value for repeatability.
        """

        rand = Random()
        rand.seed(1)

        for logical_name in range(0, 1):
            self.complete_feature(rand, 3, logical_name)

        with self.assertRaises(BugEncounteredException):
            self.software_system.operate(rand, 10000)

        self.assertEquals(334, len(self.software_system.last_trace))

        for test in self.software_system.tests:

            while True:
                try:
                    test.exercise()
                    break
                except BugEncounteredException as e:
                    test.feature.debug(rand, e.bug)

        self.software_system.operate(rand, 10000)
        self.assertEquals(10000, len(self.software_system.last_trace))


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'ChunkTest.testName']
    unittest.main()
