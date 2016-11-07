"""
@author: twsswt
"""
import unittest

import sys

from theatre_ag import Actor, SynchronizingClock

from softdev_model.system import BugEncounteredException, CentralisedVCSServer, SoftwareSystem, SystemRandom, \
    UserStory, WaterfallDevelopmentTeam


class WaterfallRegressionTestCase(unittest.TestCase):

    def setUp(self):

        self.is_64bits = sys.maxsize > 2 ** 32

        self.clock = SynchronizingClock(max_ticks=100000)

        self.centralised_vcs_server = CentralisedVCSServer(SoftwareSystem())

        self.specification = list()

        self.specification.append(UserStory(0, 3, 1))
        self.specification.append(UserStory(1, 5, 2))
        self.specification.append(UserStory(2, 7, 3))

        self.random = SystemRandom(1)

        self.development_team = WaterfallDevelopmentTeam(
            self.clock, self.centralised_vcs_server, self.specification, self.random)

        self.development_team.add_member('manager')
        self.development_team.add_member('alice')

    def assert_operate_to_desired_trace_length(self, x64_bit_result=10000, x32_bit_result=10000, limit=10000):

        try:
            self.clock.start()
            self.development_team.perform()
            self.clock.shutdown()

            working_copy = self.centralised_vcs_server.checkout().working_copy

            working_copy.operate(self.random, limit)

        except BugEncounteredException:
            pass

        if self.is_64bits:
            self.assertEquals(x64_bit_result, len(working_copy.last_trace))
        else:
            self.assertEquals(x32_bit_result, len(working_copy.last_trace))

    def test_implement_default_system_and_operate(self):
        self.assert_operate_to_desired_trace_length(12, 151)

    def test_implement_system_with_low_effectiveness_tests_and_operate(self):
        self.centralised_vcs_server.master.test_effectiveness = 0.1
        self.assert_operate_to_desired_trace_length(12, 8)

    def test_implement_system_with_high_effectiveness_tests_and_operate(self):
        self.centralised_vcs_server.master.test_effectiveness = 1.0
        self.assert_operate_to_desired_trace_length()


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
