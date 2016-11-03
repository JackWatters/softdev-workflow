import unittest

from mock import Mock

from Queue import Queue

from softdev_model.system import TDDDevelopmentTeam, SoftwareProject, SystemRandom


class SoftwareProjectTestCase(unittest.TestCase):

    def setUp(self):

        self.mock_random = Mock(spec=SystemRandom)
        self.mock_schedule = Mock(spec=Queue)

        self.mock_development_team = Mock(spec=TDDDevelopmentTeam)

        self.software_project = SoftwareProject(
            self.mock_random,
            self.mock_development_team,
            self.mock_schedule,
            number_of_traces=5,
            max_trace_length=1000
        )

    def test_that_system_is_built_and_operated(self):

        self.software_project.build_and_operate()

        self.mock_development_team.build_software_system.assert_called_once_with(self.mock_schedule, self.mock_random)

        self.mock_development_team.release.operate.assert_called_with(self.mock_random, 1000)


if __name__ == '__main__':
    unittest.main()
