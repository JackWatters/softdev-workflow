import sys

import unittest

from Queue import Queue

from theatre_ag import Actor, SynchronizingClock, Cast

from softdev_model.system import BugEncounteredException, CentralisedVCSServer, SoftwareProject, SoftwareSystem, \
    SystemRandom, TestDrivenDevelopmentPlan, UserStory


class TDDDeveloperRegressionTestCase(unittest.TestCase):

    def setUp(self):

        self.is_64bits = sys.maxsize > 2 ** 32

        self.clock = SynchronizingClock(max_ticks=1000)

        self.development_team = Cast(self.clock)
        self.development_team.add_member('alice')

        self.product_backlog = Queue()

        self.product_backlog.put(UserStory(0, 3, 1))
        self.product_backlog.put(UserStory(1, 5, 2))
        self.product_backlog.put(UserStory(2, 7, 3))

        self.random = SystemRandom(1)

        self.plan = TestDrivenDevelopmentPlan(self.product_backlog, self.random)

        self.centralised_vcs_server = CentralisedVCSServer(SoftwareSystem())

        self.software_project = SoftwareProject(
            self.clock, self.development_team, self.plan, self.centralised_vcs_server, self.random)

    def assert_operate_trace_length(self, x64_bit_result, x32_bit_result):
        working_copy = self.centralised_vcs_server.checkout().working_copy

        with self.assertRaises(BugEncounteredException):
            working_copy.operate(self.random, 10000)

        if self.is_64bits:
            self.assertEquals(x64_bit_result, len(working_copy.last_trace))
        else:
            self.assertEquals(x32_bit_result, len(working_copy.last_trace))

    def test_tdd_development_team(self):

        self.software_project.build()


if __name__ == '__main__':
    unittest.main()
