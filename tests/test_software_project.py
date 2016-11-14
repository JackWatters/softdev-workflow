import unittest

from mock import Mock

from Queue import Queue

from theatre_ag import SynchronizingClock, Team

from softdev_model.system import DevelopmentPlan, CentralisedVCSServer, SoftwareProject, SystemRandom, SoftwareSystem


class SoftwareProjectTestCase(unittest.TestCase):

    def setUp(self):

        self.mock_random = Mock(spec=SystemRandom)

        self.clock = Mock(spec=SynchronizingClock)

        self.mock_development_team = Mock(spec=Team)

        self.centralised_vcs_server = Mock(spec=CentralisedVCSServer)

        self.mock_plan = Mock(spec=DevelopmentPlan)
        self.mock_plan.release = Mock(return_value=Mock(spec=SoftwareSystem))

        self.software_project = SoftwareProject(self.clock, self.mock_development_team, self.mock_plan,
                                                self.centralised_vcs_server, self.mock_random)

    def test_that_system_is_built_and_operated(self):

        self.software_project.build()

        self.software_project.deploy_and_operate(1, 1000)

        self.mock_development_team.perform.assert_called_once_with()

        self.software_project.last_deployment.operate.assert_called_with(self.mock_random, 1000)


if __name__ == '__main__':
    unittest.main()
