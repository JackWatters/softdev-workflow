import unittest

from mock import Mock

from Queue import Queue

from theatre_ag import SynchronizingClock, Cast

from softdev_model.system import CentralisedVCSServer, SoftwareProject, SystemRandom, SoftwareSystem

from softdev_model.workflows import WaterfallDevelopmentPlan


class SoftwareProjectTestCase(unittest.TestCase):

    def setUp(self):

        self.mock_random = Mock(spec=SystemRandom)

        self.clock = Mock(spec=SynchronizingClock)

        self.mock_development_team = Mock(spec=Cast)

        self.centralised_vcs_server = Mock(spec=CentralisedVCSServer)

        self.mock_plan = Mock(spec=WaterfallDevelopmentPlan)
        self.mock_plan.release = Mock(return_value=Mock(spec=SoftwareSystem))
        self.mock_plan.centralised_vcs_server = self.centralised_vcs_server

        self.software_project = SoftwareProject(
            self.clock, self.mock_development_team, self.mock_plan, self.mock_random)

    def test_that_system_is_built_and_operated(self):

        self.software_project.perform()

        self.software_project.deploy_and_operate(1, 1000)

        self.mock_development_team.start.assert_called_once_with()

        self.software_project.last_deployment.operate.assert_called_with(self.mock_random, 1000)


if __name__ == '__main__':
    unittest.main()
