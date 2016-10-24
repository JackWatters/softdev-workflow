"""
@author: twsswt
"""
import unittest

from mock import Mock

from softdev_model.system import BugEncounteredException, Chunk, Feature, SoftwareSystem, SystemRandom


class ChunkTest(unittest.TestCase):

    def setUp(self):
        """
        Mocks a single feature system and gives it two chunks.
        """

        feature_mock = Mock(spec=Feature)
        
        self.fixture_chunks = []
        
        feature_mock.chunks = set()
        
        feature_mock.software_system = Mock(spec=SoftwareSystem)
        feature_mock.software_system.chunks = feature_mock.chunks

        feature_mock.software_system.probability_gain_feature_dependency = 0.1
        feature_mock.software_system.probability_gain_system_dependency = 0.05
        feature_mock.software_system.probability_lose_feature_dependency = 0.05
        feature_mock.software_system.probability_lose_system_dependency = 0.05

        self.fixture_chunks.append(Chunk(0, feature_mock))
        self.fixture_chunks.append(Chunk(1, feature_mock))
        
        feature_mock.chunks |= set(self.fixture_chunks)

    def tearDown(self):
        pass

    def test_modify_create_bug(self):
        random_mock = Mock(spec=SystemRandom)
        random_mock.a_bug_should_be_inserted = Mock(side_effect=[True, False])

        self.fixture_chunks[0].modify(random_mock)

        self.assertEqual(1, len(self.fixture_chunks[0].bugs), "Unexpected number of bugs")

    def test_modify_create_dependency(self):
        random_mock = Mock(spec=SystemRandom)
        random_mock.a_bug_should_be_inserted = Mock(side_effect=[False])
        random_mock.a_system_dependency_should_be_added = Mock(side_effect=[False])

        self.fixture_chunks[0].modify(random_mock)
        
        self.assertEqual(1, len(self.fixture_chunks[0].dependencies))

    def test_refactor(self):
        random_mock = Mock(spec=SystemRandom)
        random_mock.dependency_should_be_added = Mock(side_effect=[True])
        random_mock.a_bug_should_be_inserted = Mock(side_effect=[False])
        random_mock.dependency_should_be_removed = Mock(side_effect=[True])

        self.fixture_chunks[0].modify(random_mock)
        self.fixture_chunks[0].refactor(random_mock)

        self.assertEqual(0, len(self.fixture_chunks[0].dependencies))

    def test_debug(self):
        random_mock = Mock(spec=SystemRandom)

        random_mock.unknown_bug_should_be_removed = Mock(return_value=True)

        self.fixture_chunks[0].debug(random_mock)

        self.assertEqual(len(self.fixture_chunks[0].bugs), 0)

    def test_operate_bug_not_manifest(self):
        random_mock = Mock(spec=SystemRandom)

        random_mock.dependency_should_be_added = Mock(side_effect=[False])
        random_mock.a_bug_should_be_inserted = Mock(side_effect=[True, False])
        self.fixture_chunks[0].modify(random_mock)
        
        random_mock.bug_manifests_itself = Mock(side_effect=[False])
        self.fixture_chunks[0].operate(random_mock)

    def test_operate_bug_manifest(self):
        random_mock = Mock(spec=SystemRandom)
        random_mock.dependency_should_be_added = Mock(side_effect=[False])
        random_mock.a_bug_should_be_inserted = Mock(side_effect=[True, False])

        self.fixture_chunks[0].modify(random_mock)
        
        random_mock.bug_manifests_itself = Mock(side_effect=[True])
        with self.assertRaises(BugEncounteredException):
            self.fixture_chunks[0].operate(random_mock)


if __name__ == "__main__":
    # import sys;sys.argv = [.., .ChunkTest.testName.]
    unittest.main()
