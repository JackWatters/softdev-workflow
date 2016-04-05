import unittest


from models.systems.software.bug import Bug, BugEncounteredException
from models.systems.software.chunk import Chunk
from models.systems.software.developer import Developer
from models.systems.software.feature import Feature
from models.systems.software.softwaresystem import SoftwareSystem
from models.systems.software.test import Test

from models.workflows.testdrivendevelopment import TestDrivenDevelopment

from random import Random


class TestDrivenDevelopmentTest(unittest.TestCase):

    def setUp(self):
        Chunk._count = 0
        Feature._count = 0
        Test._count = 0
        Bug._count = 0

        self.random = Random(1)
        self.software_system = SoftwareSystem()
        self.developer = Developer(person_time=500)

        for feature_size in [3, 5, 7]:
            self.software_system.add_feature(feature_size)

        self.workflow = TestDrivenDevelopment(
            software_system=self.software_system,
            target_dependencies_per_feature=0
        )

    def test_implement_default_system_and_operate_regression(self):
        self.software_system.test_effectiveness=0.5
        self.workflow.work(self.random, self.developer)

        with self.assertRaises(BugEncounteredException):
            self.random.seed(1)
            self.software_system.operate(self.random, 10000)

        self.assertEquals(28, len(self.software_system.successful_operations))


if __name__ == '__main__':
    unittest.main()
