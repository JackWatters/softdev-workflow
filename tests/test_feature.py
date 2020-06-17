"""
@author: twsswt
"""
import unittest

from unittest.mock import Mock

from softdev_model.system import BugEncounteredException, Feature, InoperableFeatureException, SoftwareSystem, \
    SystemRandom


class FeatureTest(unittest.TestCase):

    def setUp(self):

        software_system_mock = Mock(spec=SoftwareSystem)
        self.feature = Feature(software_system_mock, 0, 1)
        software_system_mock.chunks = self.feature.chunks

        software_system_mock.probability_gain_feature_dependency = 0.1
        software_system_mock.probability_gain_system_dependency = 0.05
        software_system_mock.probability_lose_feature_dependency = 0.05
        software_system_mock.probability_lose_system_dependency = 0.05

    def _extend_fixture_feature(self, bug_sequence=[False]):
        random_mock = Mock(spec=SystemRandom)
        random_mock.create_local_content = Mock(side_effect=['content'])
        random_mock.a_bug_should_be_inserted = Mock(side_effect=bug_sequence)
        random_mock.sample_chunks = Mock(side_effect=[set()])

        return self.feature.extend(0, random_mock)

    def test_extend_feature_no_dependencies(self):

        chunk = self._extend_fixture_feature()

        self.assertEquals(0, len(chunk.dependencies))

    def test_operate_implemented_no_bugs(self):
        self._extend_fixture_feature()

        mock_random = Mock(spec=SystemRandom)
        choice_of_chunks = [next(iter(self.feature.chunks))]
        mock_random.sample_chunks = Mock(side_effect=[choice_of_chunks])
        self.feature.operate(mock_random)

    def test_operate_implemented_with_bugs(self):
        self._extend_fixture_feature([True, False])

        mock_random = Mock(spec=SystemRandom)
        mock_random.sample_chunks = Mock(side_effect=[[next(iter(self.feature.chunks))]])
        mock_random.bug_manifests_itself = Mock(return_value=True)

        with self.assertRaises(BugEncounteredException):
            self.feature.operate(mock_random)

    def test_operate_unimplemented(self):
        mock_random = Mock(spec=SystemRandom)

        mock_random.sample = Mock(side_effect=[[]])
        with self.assertRaises(InoperableFeatureException): 
            self.feature.operate(mock_random)

    def test_debug(self):
        chunk = self._extend_fixture_feature([True, False])

        mock_random = Mock(spec=SystemRandom)
        mock_random.unknown_bug_should_be_removed = Mock(spec=[True])
        mock_random.choose_bug = Mock(side_effect=[next(iter(chunk.bugs))])

        self.feature.debug(mock_random)
        self.assertEquals(0, len(chunk.bugs))


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'FeatureTest.test_operate_implemented_with_bugs']
    unittest.main()
