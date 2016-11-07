"""
@author: twsswt
"""
import unittest

import sys

from theatre_ag import Actor, SynchronizingClock

from softdev_model.system import BugEncounteredException, CentralisedVCSServer, SoftwareSystem, SystemRandom

from softdev_model.workflows import Waterfall


class WaterfallRegressionTestCase(unittest.TestCase):

    def setUp(self):

        self.is_64bits = sys.maxsize > 2**32

        self.random = SystemRandom(1)
        software_system = SoftwareSystem()
        self.centralised_vcs_server = CentralisedVCSServer(software_system)

        self.clock = SynchronizingClock(max_ticks=1000)
        self.team_manager = Actor('manager', self.clock)

        self.developers = {Actor('alice', self.clock), Actor('bob', self.clock)}

        self.waterfall = Waterfall(self.team_manager, self.developers, self.centralised_vcs_server)

    def test_implement_default_system_and_operate(self):

        self.team_manager.allocate_task(
            self.waterfall, self.waterfall.allocate_tasks, [[(0, 3), (1, 5), (2, 7)], self.random])

        self.team_manager.start()

        for developer in self.developers:
            developer.start()

        self.clock.start()

        self.team_manager.shutdown()
        for developer in self.developers:
            developer.shutdown()

        for developer in self.developers:
            print developer.completed_tasks

        vcs_client = self.centralised_vcs_server.checkout()

        with self.assertRaises(BugEncounteredException):
            self.random.seed(1)
            vcs_client.working_copy.operate(self.random, 10000)

        if self.is_64bits:
            self.assertEquals(88, len(vcs_client.working_copy.last_trace))
        else:
            self.assertEquals(27, len(vcs_client.working_copy.last_trace))

    def test_implement_system_with_low_effectiveness_tests_and_operate(self):

        self.centralised_vcs_server.master.test_effectiveness = 0.1

        self.waterfall.allocate_tasks([(0, 3), (1, 5), (2, 7)], self.random)

        software_system = self.centralised_vcs_server.checkout().working_copy

        with self.assertRaises(BugEncounteredException):
            self.random.seed(1)
            software_system.operate(self.random, 10000)

        if self.is_64bits:
            self.assertEquals(88, len(software_system.last_trace))
        else:
            self.assertEquals(0, len(software_system.last_trace))

    def test_implement_system_with_high_effectiveness_tests_and_operate(self):
        self.centralised_vcs_server.master.test_effectiveness = 1.0

        self.waterfall.allocate_tasks([(0, 3), (1, 5), (2, 7)], self.random)

        self.random.seed(1)

        software_system = self.centralised_vcs_server.checkout().working_copy

        software_system.operate(self.random, 10000)
        self.assertEquals(10000, len(software_system.last_trace))


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
