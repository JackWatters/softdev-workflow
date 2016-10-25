import unittest
from mock import Mock, call

from theatre_ag import AbstractClock

from softdev_model.system import Bug, BugEncounteredException, CentralisedVCSClient, CentralisedVCSServer, Chunk, \
    Feature, SoftwareSystem, SystemRandom, Test

from softdev_model.workflows import TDDDeveloper


class TDDDeveloperTestCase(unittest.TestCase):

    def setUp(self):
        self.clock = Mock(spec=AbstractClock)
        self.clock.current_tick = 0

        self.centralised_vcs_server = Mock(spec=CentralisedVCSServer)

        self.developer = TDDDeveloper("alice", self.clock, self.centralised_vcs_server)

    def test_tdd_developer(self):

        centralised_vcs_client = Mock(spec=CentralisedVCSClient)
        centralised_vcs_client.working_copy = Mock(spec=SoftwareSystem)
        self.centralised_vcs_server.checkout = Mock(return_value=centralised_vcs_client)

        mock_feature = Mock(spec=Feature)

        mock_feature.tests_per_chunk_ratio = 0
        mock_feature.test_coverage = 0.0

        # noinspection PyUnusedLocal
        def add_test_side_effect(*args, **kwargs):
            mock_feature.tests_per_chunk_ratio = 1
            mock_feature.test_coverage = 1.0

        mock_feature.add_test = Mock(side_effect=add_test_side_effect)

        mock_feature.is_implemented = False

        # noinspection PyUnusedLocal
        def extend_side_effect(*args, **kwargs):
            mock_feature.is_implemented = True

        mock_feature.extend = Mock(side_effect=extend_side_effect)

        mock_test = Mock(spec=Test)
        mock_bug = Mock(spec=Bug)

        class ExerciseTestSideEffect:

            def __init__(self): self.raised = False

            # noinspection PyUnusedLocal
            def __call__(self, *args, **kwargs):
                if not self.raised:
                    self.raised = True
                    raise BugEncounteredException(mock_bug)
                else:
                    return

        mock_test.exercise = Mock(side_effect=ExerciseTestSideEffect())
        mock_test.feature = mock_feature
        mock_feature.tests = {mock_test}

        mock_dependency = Mock(spec=Chunk)
        mock_feature.dependencies = {mock_dependency}

        # noinspection PyUnusedLocal
        def mock_refactoring(*args, **kwargs):
            mock_feature.dependencies = {}

        mock_feature.refactor = Mock(side_effect=mock_refactoring)

        centralised_vcs_client.working_copy.get_feature = Mock(return_value=mock_feature)
        centralised_vcs_client.working_copy.features = {mock_feature}

        random = Mock(spec=SystemRandom)

        self.developer.allocate_tasks([(0, 1)], random)

        centralised_vcs_client.working_copy.add_feature.assert_called_once_with(0, 1)

        mock_feature.extend.assert_has_calls(
            [call(0, random)]
        )

        mock_feature.add_test.assert_has_calls(
            [call(0)]
        )

        mock_feature.debug.assert_has_calls(
            [call(random, mock_bug)]
        )

        mock_feature.refactor.assert_has_calls(
            [call(random)]
        )

        centralised_vcs_client.commit.assert_has_calls(
            [],
            any_order=False
        )


if __name__ == '__main__':
    unittest.main()
