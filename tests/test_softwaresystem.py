"""
@author: tws
"""
import unittest

from sortedcontainers import SortedSet

from softdev_model.system import BugEncounteredException, SoftwareSystem, SystemRandom

from mock import Mock


class SoftwareSystemTest(unittest.TestCase):

    def setUp(self):
        self.software_system = SoftwareSystem()
        self.chunk_count = 0

    def test_add_feature(self):
        self.software_system.add_feature('a', 1)
        self.software_system.add_feature('b', 1)

        self.assertEquals(['a', 'b'], map(lambda f: f.logical_name, self.software_system.features))

    def test_get_feature(self):
        self.software_system.add_feature('a', 2)
        feature = self.software_system.get_feature('a')

        self.assertEquals('a', feature.logical_name)

    def test_chunks(self):
        feature_a = self.software_system.add_feature('a', 1)
        feature_b = self.software_system.add_feature('b', 1)

        feature_b.add_chunk('2')
        feature_a.add_chunk('1')

        self.assertEquals(['a.1', 'b.2'], self.software_system.chunk_names)

    def test_bugs(self):

        random_mock = Mock(spec=SystemRandom)

        feature_a = self.software_system.add_feature('a', 5)
        random_mock.sample_chunks = Mock(return_value=SortedSet(key=lambda c: c.fully_qualified_name))
        random_mock.create_local_content = Mock(return_value=['123'])
        random_mock.a_bug_should_be_inserted = Mock(side_effect=[True, False])
        chunk_1 = feature_a.extend('1', random_mock)

        random_mock.sample_chunks = \
            Mock(return_value=SortedSet(iterable={chunk_1}, key=lambda c: c.fully_qualified_name))
        random_mock.create_local_content = Mock(return_value=['456'])
        random_mock.dependency_should_be_added = Mock(side_effect=[False, True, True, True])
        random_mock.a_bug_should_be_inserted = Mock(side_effect=[True, False, False])
        chunk_2 = feature_a.extend('2', random_mock)

        random_mock.sample_chunks = \
            Mock(return_value=SortedSet(iterable={chunk_2}, key=lambda c: c.fully_qualified_name))
        random_mock.create_local_content = Mock(return_value=['789'])
        random_mock.dependency_should_be_added = Mock(side_effect=[False, True, True, True])
        random_mock.a_bug_should_be_inserted = Mock(side_effect=[False, True, False])
        feature_a.extend('4', random_mock)

        self.assertEquals(['a.1.0', 'a.1.1', 'a.4.0'], map(lambda b: b.fully_qualified_name, self.software_system.bugs))

    def test_tests(self):

        feature_a = self.software_system.add_feature('a', 3)
        feature_a.add_test(4)
        feature_a.add_test(3)
        self.assertEquals(['a.3', 'a.4'], map(lambda t: t.fully_qualified_name, self.software_system.tests))

    def complete_feature(self, logical_name, size, random):
        feature = self.software_system.add_feature(logical_name, size)
        while not feature.is_implemented:
            feature.extend(self.chunk_count, random)
            self.chunk_count += 1

        for test_logical_name in range(0, 30):
            feature.add_test(test_logical_name)

    def test_operate_test_debug_operate_regression(self):
        """
        Regression tests using a seed random value for repeatability.
        """

        random = SystemRandom()
        random.seed(1)

        for logical_name in range(0, 1):
            self.complete_feature(logical_name, 3, random)

        with self.assertRaises(BugEncounteredException):
            self.software_system.operate(random, 10000)

        self.assertEquals(3, len(self.software_system.last_trace))

        for test in self.software_system.tests:

            while True:
                try:
                    test.exercise()
                    break
                except BugEncounteredException as e:
                    test.feature.debug(random, e.bug)

        self.software_system.operate(random, 10000)
        self.assertEquals(10000, len(self.software_system.last_trace))


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'ChunkTest.testName']
    unittest.main()
