import sys
import unittest

from softdev_model.system import BugEncounteredException, CentralisedVCSServer, SoftwareSystem, SystemRandom

from softdev_model.workflows import TestDrivenDevelopment


class TestDrivenDevelopmentTest(unittest.TestCase):

    def setUp(self):

        self.is_64bits = sys.maxsize > 2 ** 32

        self.centralised_vcs_server = CentralisedVCSServer(SoftwareSystem())
        self.schedule = [(0, 3), (1, 5), (2, 7)]
        self.random = SystemRandom(1)

        self.test_driven_development = TestDrivenDevelopment(self.centralised_vcs_server)

    def test_implement_default_system_and_operate_regression(self):

        self.test_driven_development.allocate_tasks(self.schedule, self.random)

        self.random.seed(1)

        working_copy = self.centralised_vcs_server.checkout().working_copy

        with self.assertRaises(BugEncounteredException):
            working_copy.operate(self.random, 10000)

        if self.is_64bits:
            self.assertEquals(12, len(working_copy.last_trace))
        else:
            self.assertEquals(32, len(working_copy.last_trace))


if __name__ == '__main__':
    unittest.main()
