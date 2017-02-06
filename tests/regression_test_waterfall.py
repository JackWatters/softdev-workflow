"""
@author: twsswt
"""
import unittest

import sys

from theatre_ag import SynchronizingClock, Team

from softdev_model.system import BugEncounteredException, CentralisedVCSServer, SoftwareProject, SoftwareSystem, \
    SystemRandom, UserStory, WaterfallDevelopmentPlan


class WaterfallRegressionTestCase(unittest.TestCase):

    def setUp(self):

        self.is_64bits = sys.maxsize > 2 ** 32

        self.clock = SynchronizingClock(max_ticks=100000)

        self.development_team = Team(self.clock)
        self.development_team.add_member('manager')
        self.development_team.add_member('alice')

        self.specification = [UserStory(0, 3, 1), UserStory(1, 5, 2), UserStory(2, 7, 3)]

        self.random = SystemRandom(1)

        self.plan = WaterfallDevelopmentPlan(self.specification, self.random)

        self.centralised_vcs_server = CentralisedVCSServer(SoftwareSystem())

        self.project = SoftwareProject(
            self.clock, self.development_team, self.plan, self.centralised_vcs_server, self.random)

    def assert_operate_to_desired_trace_length(self, x64_bit_result=10000, x32_bit_result=10000, limit=10000):

        try:
            self.project.build()

            working_copy = self.centralised_vcs_server.checkout().working_copy

            working_copy.operate(self.random, limit)

        except BugEncounteredException:
            pass

        if self.is_64bits:
            self.assertEquals(x64_bit_result, len(working_copy.last_trace))
        else:
            self.assertEquals(x32_bit_result, len(working_copy.last_trace))

    def test_implement_default_system_and_operate(self):
        self.assert_operate_to_desired_trace_length(12, 1)

    def test_implement_system_with_low_effectiveness_tests_and_operate(self):
        self.centralised_vcs_server.master.test_effectiveness = 0.1
        self.assert_operate_to_desired_trace_length(12, 0)

    def test_implement_system_with_high_effectiveness_tests_and_operate(self):
        self.centralised_vcs_server.master.test_effectiveness = 1.0
        self.assert_operate_to_desired_trace_length()


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
