import unittest

from mock import Mock
from random import Random

from softdev_model.system import Bug, Developer, Feature, SoftwareSystem, CentralisedVCSClient


class DeveloperTestCase(unittest.TestCase):

    def setUp(self):

        self.developer = Developer("alice", person_time=2)

        self.feature_mock = Mock(spec=Feature)
        self.bug_mock = Mock(spec=Bug)
        self.software_system_mock = Mock(spec=SoftwareSystem)
        self.centralised_vcs_client_mock = Mock(spec=CentralisedVCSClient)
        self.random_mock = Mock(spec=Random)

    def test_idle(self):

        self.developer.idle()
        self.assertEquals(1, self.developer.person_time)

    def test_extend_feature(self):

        self.developer.extend_feature(random=self.random_mock, logical_name=0, feature=self.feature_mock)

        self.assertEquals(1, self.developer.person_time)

    def test_add_test(self):

        self.developer.add_test(self.software_system_mock, 0, self.feature_mock)

        self.assertEquals(1, self.developer.person_time)

    def test_debug(self):

        self.developer.debug(self.feature_mock, self.bug_mock, self.random_mock)

        self.assertEquals(1, self.developer.person_time)

    def test_refactor(self):

        self.developer.refactor(self.feature_mock, self.random_mock)

        self.assertEquals(1, self.developer.person_time)

    def test_update(self):

        self.centralised_vcs_client_mock.conflicts = {}

        self.developer.update_working_copy(self.centralised_vcs_client_mock, self.random_mock)

        self.assertEquals(2, self.developer.person_time)

    def test_commit(self):

        self.centralised_vcs_client_mock.conflicts = {}

        self.developer.commit_changes(self.centralised_vcs_client_mock)

        self.assertEquals(2, self.developer.person_time)


if __name__ == '__main__':
    unittest.main()
