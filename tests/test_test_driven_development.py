import sys
import unittest

from mock import Mock
from random import Random

from theatre_ag import AbstractClock, Actor

from softdev_model.system import BugEncounteredException, CentralisedVCSServer, SoftwareSystem

from softdev_model.workflows import test_driven_development


class TestDrivenDevelopmentTest(unittest.TestCase):

    def setUp(self):

        self.is_64bits = sys.maxsize > 2 ** 32

        clock = Mock(spec=AbstractClock)
        clock.current_tick = -1
        self.developer = Actor("alice", clock)

        self.centralised_vcs_server = CentralisedVCSServer(SoftwareSystem())
        self.schedule = [(0, 3), (1, 5), (2, 7)]
        self.random = Random(1)

    def test_implement_default_system_and_operate_regression(self):

        self.developer.perform_task(test_driven_development, [self.centralised_vcs_server, self.schedule, self.random])

        self.random.seed(1)

        working_copy = self.centralised_vcs_server.checkout().working_copy

        with self.assertRaises(BugEncounteredException):
            working_copy.operate(self.random, 10000)

        if self.is_64bits:
            self.assertEquals(12, len(working_copy.last_trace))
        else:
            self.assertEquals(24, len(working_copy.last_trace))


if __name__ == '__main__':
    unittest.main()
