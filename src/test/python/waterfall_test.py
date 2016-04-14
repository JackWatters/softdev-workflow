"""
@author: twsswt
"""
import unittest

from models.systems.software import Bug, BugEncounteredException, Chunk, Developer, Feature, SoftwareSystem, Test

from models.workflows import Waterfall

from random import Random


class WaterfallTest(unittest.TestCase):

    def setUp(self):
        Chunk._count = 0
        Feature._count = 0
        Test._count = 0
        Bug._count = 0

        self.random = Random(1)
        self.software_system = SoftwareSystem()
        self.developer = Developer(person_time=500)

        self.workflow = Waterfall(
            software_system=self.software_system,
        )

    def test_implement_default_system_and_operate_regression(self):
        self.workflow.work(self.random, self.developer, [3, 5, 7])

        with self.assertRaises(BugEncounteredException):
            self.random.seed(1)
            self.software_system.operate(self.random, 10000)
        self.assertEquals(73, len(self.software_system.last_trace))

    def test_implement_system_with_low_effectiveness_tests_and_operate_regression(self):
        self.software_system.test_effectiveness = 0.1

        self.workflow.work(self.random, self.developer, [3, 5, 7])

        with self.assertRaises(BugEncounteredException):
            self.software_system.operate(self.random, 10000)
        self.assertEquals(11, len(self.software_system.last_trace))

    def test_implement_system_with_high_effectiveness_tests_and_operate_regression(self):
        self.software_system.test_effectiveness = 1.0

        self.workflow.work(self.random, self.developer, [3, 5, 7])

        self.software_system.operate(self.random, 10000)
        self.assertEquals(10000, len(self.software_system.last_trace))


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
