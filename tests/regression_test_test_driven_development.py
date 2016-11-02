import sys
import unittest

from Queue import PriorityQueue

from theatre_ag import Actor, SynchronizingClock

from softdev_model.system import BugEncounteredException, CentralisedVCSServer, SoftwareSystem, SystemRandom, UserStory
from softdev_model.workflows import TestDrivenDevelopment


class TestDrivenDevelopmentRegressionTestCase(unittest.TestCase):

    def setUp(self):

        self.is_64bits = sys.maxsize > 2 ** 32

        self.centralised_vcs_server = CentralisedVCSServer(SoftwareSystem())

        self.product_backlog = PriorityQueue()
        self.product_backlog.put(UserStory(0, 3, 1))
        self.product_backlog.put(UserStory(1, 5, 2))
        self.product_backlog.put(UserStory(2, 7, 3))

        self.random = SystemRandom(1)

        self.clock = SynchronizingClock(max_ticks=1000)

        self.actor = Actor("alice", self.clock)

        self.test_driven_development = TestDrivenDevelopment(self.actor, self.centralised_vcs_server)

    def test_work_from_backlog(self):

        self.test_driven_development.work_from_backlog(self.product_backlog, self.random)

        self.random.seed(1)

        working_copy = self.centralised_vcs_server.checkout().working_copy

        with self.assertRaises(BugEncounteredException):
            working_copy.operate(self.random, 10000)

        if self.is_64bits:
            self.assertEquals(12, len(working_copy.last_trace))
        else:
            self.assertEquals(85, len(working_copy.last_trace))


if __name__ == '__main__':
    unittest.main()
