"""
@author: twsswt
"""
import unittest

from mock import Mock

from softdev_model.system import BugEncounteredException, Feature, InoperableFeatureException, SoftwareSystem

from random import Random


class FeatureTest(unittest.TestCase):

    def setUp(self):
        software_system_mock = Mock(spec=SoftwareSystem)
        self.feature = Feature(software_system_mock, 1)
        software_system_mock.chunks = self.feature.chunks
        
        software_system_mock.probability_gain_feature_dependency = 0.1
        software_system_mock.probability_gain_system_dependency = 0.05
        software_system_mock.probability_lose_feature_dependency = 0.05
        software_system_mock.probability_lose_system_dependency = 0.05
        software_system_mock.probability_new_bug = 0.5
        software_system_mock.probability_debug_known = 0.9
        software_system_mock.probability_debug_unknown = 0.01
        software_system_mock.probability_detection = 0.5
        software_system_mock.probability_failure_on_demand = 0.01

    def _extend_feature_with_bug_and_feature_spec(self, random_float_sequence):
        random_mock = Mock(spec=Random)
        
        random_mock.sample = Mock(side_effect=[[]])
        random_mock.randint = Mock(side_effect=[1])
        random_mock.random = Mock(side_effect=random_float_sequence)
        chunk = self.feature.extend(random_mock)
        
        return chunk

    def _extend_fixture_feature_with_no_bugs(self):
        return self._extend_feature_with_bug_and_feature_spec([1.0])

    def _extend_fixture_feature_with_bug(self):
        return self._extend_feature_with_bug_and_feature_spec([.45, 0.55, 0.001])

    def test_extend_feature_no_dependencies(self):
        chunk = self._extend_fixture_feature_with_no_bugs()
        self.assertEquals(0, len(chunk.dependencies))

    def test_operate_implemented_no_bugs(self):
        self._extend_fixture_feature_with_no_bugs()

        mock_random = Mock(spec=Random)
        choice_of_chunks = [next(iter(self.feature.chunks))]
        mock_random.sample = Mock(side_effect=[choice_of_chunks])
        self.feature.operate(mock_random)

    def test_operate_implemented_with_bugs(self):
        self._extend_fixture_feature_with_bug()

        mock_random = Mock(spec=Random)

        choice_of_chunks = [next(iter(self.feature.chunks))]
        mock_random.sample = Mock(side_effect=[choice_of_chunks])
        mock_random.random = Mock(side_effect=[0.001])

        with self.assertRaises(BugEncounteredException):
            self.feature.operate(mock_random)

    def test_operate_unimplemented(self):
        mock_random = Mock(spec=Random)

        mock_random.sample = Mock(side_effect=[[]])
        with self.assertRaises(InoperableFeatureException): 
            self.feature.operate(mock_random)

    def test_debug(self):
        chunk = self._extend_fixture_feature_with_bug()

        mock_random = Mock(spec=Random)
        mock_random.choice = Mock(side_effect=[next(iter(chunk.bugs))])
        mock_random.random = Mock(side_effect=[0.001])

        self.feature.debug(mock_random)
        self.assertEquals(0, len(chunk.bugs))


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'FeatureTest.test_operate_implemented_with_bugs']
    unittest.main()
