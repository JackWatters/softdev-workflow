import unittest

from mock import Mock

from theatre_ag import SynchronizingClock

from softdev_model.system import CentralisedVCSServer, TDDDevelopmentTeam


class MyTestCase(unittest.TestCase):

    def setUp(self):

        self.clock = Mock(spec=SynchronizingClock)
        self.centralised_vcs = Mock(spec=CentralisedVCSServer)

        self.tdd_development_team = TDDDevelopmentTeam(self.clock, self.centralised_vcs)

    def test_add_developer(self):
        self.tdd_development_team.add_tdd_developer('alice')

        self.assertEqual(1, len(self.tdd_development_team.developers))


if __name__ == '__main__':
    unittest.main()
