import unittest

from mock import Mock

from theatre_ag import SynchronizingClock

from softdev_model.system import CentralisedVCSServer, TDDDevelopmentTeam


class TDDDevelopmentTeamTestCase(unittest.TestCase):

    def setUp(self):

        self.clock = Mock(spec=SynchronizingClock)
        self.centralised_vcs = Mock(spec=CentralisedVCSServer)

        self.tdd_development_team = TDDDevelopmentTeam(self.clock, self.centralised_vcs, None, None)

    def test_add_developer(self):
        self.tdd_development_team.add_member('alice')

        self.assertEqual(1, len(self.tdd_development_team.team_members))


if __name__ == '__main__':
    unittest.main()
