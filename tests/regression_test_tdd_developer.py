import unittest

from Queue import Queue

from threading import Thread

from theatre_ag import Actor, SynchronizingClock

from softdev_model.system import CentralisedVCSServer, SoftwareSystem, SystemRandom, UserStory
from softdev_model.workflows import TestDrivenDevelopment


class TDDDeveloperRegressionTestCase(unittest.TestCase):

    def setUp(self):
        self.clock = SynchronizingClock(max_ticks=1000)

        self.clock_thread = Thread(target=self.clock.tick_toc)

        self.centralised_vcs_server = CentralisedVCSServer(SoftwareSystem())

        self.tdd_developer_1 = Actor("alice", self.clock)
        self.tdd_developer_2 = Actor("bob", self.clock)

        self.test_driven_development_1 = TestDrivenDevelopment(self.tdd_developer_1, self.centralised_vcs_server)
        self.test_driven_development_2 = TestDrivenDevelopment(self.tdd_developer_2, self.centralised_vcs_server)

        self.product_backlog = Queue()

        self.product_backlog.put(UserStory(0, 3, 1))
        self.product_backlog.put(UserStory(1, 5, 2))
        self.product_backlog.put(UserStory(2, 7, 3))

        self.random = SystemRandom(1)

    def test_tdd_developer(self):
        self.tdd_developer_1.allocate_task(
            self.test_driven_development_1.work_from_backlog, [self.product_backlog, self.random])

        self.tdd_developer_1.start()
        self.tdd_developer_2.start()

        self.clock_thread.start()
        self.tdd_developer_1.shutdown()
        self.tdd_developer_2.shutdown()

    def test_tdd_developers(self):

        self.tdd_developer_1.allocate_task(
            self.test_driven_development_1.work_from_backlog, [self.product_backlog, self.random])

        self.tdd_developer_2.allocate_task(
            self.test_driven_development_2.work_from_backlog, [self.product_backlog, self.random])

        self.tdd_developer_1.start()
        self.tdd_developer_2.start()

        self.clock_thread.start()
        self.tdd_developer_1.shutdown()
        self.tdd_developer_2.shutdown()

'''
class TDDDevelopmentTeamTestCase(unittest.TestCase):

        def setUp(self):
            self.clock = SynchronizingClock(max_ticks=1000)

            self.clock_thread = Thread(target=self.clock.tick_toc)

            self.tdd_development_team = TDDDevelopmentTeam()

            self.product_backlog = Queue()

            self.product_backlog.put(UserStory(0, 3, 1))
            self.product_backlog.put(UserStory(1, 5, 2))
            self.product_backlog.put(UserStory(2, 7, 3))

            self.random = SystemRandom(1)

        def test_tdd_development_team(self):
            self.tdd_development_team.build_system()
'''


if __name__ == '__main__':
    unittest.main()
