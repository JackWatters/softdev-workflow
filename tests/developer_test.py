import unittest

from mock import Mock
from random import Random

from softdev_model.system import Developer, Feature, SoftwareSystem


class DeveloperTestCase(unittest.TestCase):

    def setUp(self):
        self.developer = Developer(2)

    def test_idle(self):

        self.developer.idle()
        self.assertEquals(1, self.developer.person_time)

    def test_extend_feature(self):

        random_mock = Mock(spec=Random)
        feature_mock = Mock(spec=Feature)
        feature_mock.chunks = set()
        feature_mock._sample_chunks = Mock(side_effect=[set()])
        feature_mock.software_system = Mock(spec=SoftwareSystem)
        feature_mock.software_system.chunks = set()
        feature_mock.software_system.probability_gain_system_dependency = 0.0
        feature_mock.software_system.probability_gain_feature_dependency = 0.0
        feature_mock.software_system.probability_new_bug = 0.0

        self.developer.extend_feature(random_mock, feature_mock)
        self.assertEquals(1, self.developer.person_time)

if __name__ == '__main__':
    unittest.main()
