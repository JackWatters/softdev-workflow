import sys

import unittest

from Queue import Queue

from theatre_ag import Actor, SynchronizingClock

from softdev_model.system import BugEncounteredException, CentralisedVCSServer, SoftwareSystem, SystemRandom, \
    TDDDevelopmentTeam,  UserStory
from softdev_model.workflows import TestDrivenDevelopment


class TDDDeveloperRegressionTestCase(unittest.TestCase):

    def setUp(self):

        self.is_64bits = sys.maxsize > 2 ** 32

        self.clock = SynchronizingClock(max_ticks=1000)

        self.centralised_vcs_server = CentralisedVCSServer(SoftwareSystem())

        self.product_backlog = Queue()

        self.product_backlog.put(UserStory(0, 3, 1))
        self.product_backlog.put(UserStory(1, 5, 2))
        self.product_backlog.put(UserStory(2, 7, 3))

        self.random = SystemRandom(1)

    def assert_operate_trace_length(self, x64_bit_result, x32_bit_result):
        working_copy = self.centralised_vcs_server.checkout().working_copy

        with self.assertRaises(BugEncounteredException):
            working_copy.operate(self.random, 10000)

        if self.is_64bits:
            self.assertEquals(x64_bit_result, len(working_copy.last_trace))
        else:
            self.assertEquals(x32_bit_result, len(working_copy.last_trace))

    def test_tdd_developer(self):

        tdd_developer = Actor("alice", self.clock)

        test_driven_development = TestDrivenDevelopment(tdd_developer, self.centralised_vcs_server)

        tdd_developer.allocate_task(
            test_driven_development,
            test_driven_development.work_from_backlog, [self.product_backlog, self.random])

        tdd_developer.start()
        self.clock.start()
        tdd_developer.shutdown()

        self.random.seed(1)

        self.assert_operate_trace_length(12, 32)

    def test_tdd_development_team(self):

        self.tdd_development_team = TDDDevelopmentTeam(self.clock, self.centralised_vcs_server)
        self.tdd_development_team.add_developer('alice')
        self.tdd_development_team.add_developer('bob')

        self.clock.start()
        self.tdd_development_team.build_software_system(self.product_backlog, self.random)
        self.clock.shutdown()

if __name__ == '__main__':
    unittest.main()
