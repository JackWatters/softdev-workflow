import sys
import unittest

from softdev_model.system import Bug, BugEncounteredException, Test, Chunk, Developer, Feature, SoftwareSystem
from softdev_model.workflows import TestDrivenDevelopment

from random import Random


class TestDrivenDevelopmentTest(unittest.TestCase):

    def setUp(self):
        Chunk._count = 0
        Feature._count = 0
        Test._count = 0
        Bug._count = 0

        self.is_64bits = sys.maxsize > 2 ** 32

        self.random = Random(1)
        self.software_system = SoftwareSystem()
        self.developer = Developer("alice", person_time=500)

        self.workflow = TestDrivenDevelopment(
            target_dependencies_per_feature=0
        )

    def test_implement_default_system_and_operate_regression(self):

        self.workflow.work(
            random=self.random,
            software_system=self.software_system,
            developer=self.developer,
            schedule=[(0, 3), (1, 5), (2, 7)])

        self.random.seed(1)

        with self.assertRaises(BugEncounteredException):
            self.software_system.operate(self.random, 10000)

        if self.is_64bits:
            self.assertEquals(21, len(self.software_system.last_trace))
        else:
            self.assertEquals(14, len(self.software_system.last_trace))


if __name__ == '__main__':
    unittest.main()
