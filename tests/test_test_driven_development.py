import unittest

from mock import Mock, call

from threading import _RLock

from theatre_ag import Actor, SynchronizingClock

from softdev_model.system import Bug, BugEncounteredException, CentralisedVCSClient, CentralisedVCSServer, Chunk, \
    Feature, SoftwareSystem, SystemRandom, Test, UserStory

from softdev_model.workflows import TestDrivenDevelopment


class TestDrivenDevelopmentTestCase(unittest.TestCase):

    def configure_system_development_mocks(self):

        self.mock_centralised_vcs_server = Mock(spec=CentralisedVCSServer)

        self.mock_centralised_vcs_client = Mock(spec=CentralisedVCSClient)
        self.mock_centralised_vcs_client.working_copy = Mock(spec=SoftwareSystem)
        self.mock_centralised_vcs_server.checkout = Mock(return_value=self.mock_centralised_vcs_client)

        self.mock_feature = Mock(spec=Feature)

        self.mock_feature.tests_per_chunk_ratio = 0
        self.mock_feature.test_coverage = 0.0

        self.mock_feature.chunks = []

        # noinspection PyUnusedLocal
        def add_test_side_effect(*args, **kwargs):
            self.mock_feature.tests_per_chunk_ratio = 1
            self.mock_feature.test_coverage = 1.0

        self.mock_feature.add_test = Mock(side_effect=add_test_side_effect)

        self.mock_feature.is_implemented = False

        # noinspection PyUnusedLocal
        def extend_side_effect(*args, **kwargs):
            self.mock_feature.is_implemented = True

        self.mock_feature.extend = Mock(side_effect=extend_side_effect)

        mock_test = Mock(spec=Test)
        self.mock_bug = Mock(spec=Bug)
        mock_bug = self.mock_bug

        class ExerciseTestSideEffect:

            def __init__(self):
                self.raised = False

            # noinspection PyUnusedLocal
            def __call__(self, *args, **kwargs):
                if not self.raised:
                    self.raised = True
                    raise BugEncounteredException(mock_bug)
                else:
                    return

        mock_test.exercise = Mock(side_effect=ExerciseTestSideEffect())
        mock_test.feature = self.mock_feature
        self.mock_feature.tests = {mock_test}

        mock_dependency = Mock(spec=Chunk)
        self.mock_feature.dependencies = {mock_dependency}

        # noinspection PyUnusedLocal
        def mock_refactoring(*args, **kwargs):
            self.mock_feature.dependencies = {}

        self.mock_feature.refactor = Mock(side_effect=mock_refactoring)

        self.mock_centralised_vcs_client.working_copy.get_feature = Mock(return_value=self.mock_feature)
        self.mock_centralised_vcs_client.working_copy.features = {self.mock_feature}

    def setUp(self):

        self.configure_system_development_mocks()

        self.test_driven_development = TestDrivenDevelopment(self.mock_centralised_vcs_server)

        self.user_story = UserStory('mock_story', 1)

    def test_implement_feature_tdd(self):

        mock_random = Mock(spec=SystemRandom)

        self.test_driven_development.implement_feature_tdd(self.user_story, mock_random)

        self.mock_centralised_vcs_client.working_copy.add_feature.assert_called_once_with('mock_story', 1)

        self.mock_feature.extend.assert_has_calls(
            [call(0, mock_random)]
        )

        self.mock_feature.add_test.assert_has_calls(
            [call(0)]
        )

        self.mock_feature.debug.assert_has_calls(
            [call(mock_random, self.mock_bug)]
        )

        self.mock_feature.refactor.assert_has_calls(
            [call(mock_random)]
        )

        self.mock_centralised_vcs_client.commit.assert_has_calls(
            [],
            any_order=False
        )


if __name__ == '__main__':
    unittest.main()
