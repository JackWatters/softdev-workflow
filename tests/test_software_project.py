import unittest

from mock import Mock

from Queue import Queue

from theatre_ag import Team

from softdev_model.system import DevelopmentPlan, SoftwareProject, SystemRandom, SoftwareSystem


class SoftwareProjectTestCase(unittest.TestCase):

    def setUp(self):

        self.mock_random = Mock(spec=SystemRandom)
        self.mock_plan = Mock(spec=DevelopmentPlan)
        self.mock_plan.release = Mock(return_value=Mock(spec=SoftwareSystem))

        self.mock_development_team = Mock(spec=Team)

        self.software_project = SoftwareProject(
            self.mock_random,
            self.mock_development_team,
            self.mock_plan,
            number_of_traces=5,
            max_trace_length=1000
        )

    def test_that_system_is_built_and_operated(self):

        self.software_project.build_and_operate()

        self.mock_development_team.perform.assert_called_once_with()

        self.mock_plan.release.operate.assert_called_with(self.mock_random, 1000)


if __name__ == '__main__':
    unittest.main()
