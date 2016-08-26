"""
@author: twsswt
"""
import unittest

import sys

from softdev_model.system import Bug, BugEncounteredException, Chunk, Developer, Feature, SoftwareSystem, Test
from softdev_model.workflows import Waterfall

from random import Random


class WaterfallTest(unittest.TestCase):

    def setUp(self):
        Chunk._count = 0
        Feature._count = 0
        Test._count = 0
        Bug._count = 0

        self.is_64bits = sys.maxsize > 2**32

        self.random = Random(1)
        self.software_system = SoftwareSystem()
        self.developer = Developer(person_time=500)

        self.workflow = Waterfall()

    def test_implement_default_system_and_operate_regression(self):
        self.workflow.work(self.random, self.software_system, self.developer, [(0, 3), (1, 5), (2, 7)])

        with self.assertRaises(BugEncounteredException):
            self.random.seed(1)
            self.software_system.operate(self.random, 10000)
        if self.is_64bits:
            self.assertEquals(15, len(self.software_system.last_trace))
        else:
            self.assertEquals(1, len(self.software_system.last_trace))

    def test_implement_system_with_low_effectiveness_tests_and_operate_regression(self):
        self.software_system.test_effectiveness = 0.1

        self.workflow.work(self.random, self.software_system, self.developer, [(0, 3), (1, 5), (2, 7)])
        with self.assertRaises(BugEncounteredException):
            self.random.seed(1)
            self.software_system.operate(self.random, 10000)
        self.assertEquals(1, len(self.software_system.last_trace))

    def test_implement_system_with_high_effectiveness_tests_and_operate_regression(self):
        self.software_system.test_effectiveness = 1.0

        self.workflow.work(self.random, self.software_system, self.developer, [(0, 3), (1, 5), (2, 7)])

        self.random.seed(1)
        self.software_system.operate(self.random, 10000)
        self.assertEquals(10000, len(self.software_system.last_trace))


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
