import copy

import unittest

from mock import Mock

from random import Random

from softdev_model.system import Developer, CentralisedVCSServer, SoftwareSystem


class CentralisedVCSTest(unittest.TestCase):

    def setUp(self):
        self.bob = Mock(Developer)
        self.bob.logical_name="bob"

        self.software_system = SoftwareSystem()
        feature = self.software_system.add_feature(0, 2)
        self.chunk = feature.add_chunk(0)

        self.centralised_vcs_server = CentralisedVCSServer(self.software_system)

        self.centralised_vcs_client_alice = self.centralised_vcs_server.checkout()
        self.centralised_vcs_client_bob = self.centralised_vcs_server.checkout()

    def test_checkout(self):
        self.assertEquals([0], self.centralised_vcs_client_alice.working_copy.chunk_names)

    def test_checkout_and_update(self):

        random_mock = Mock(spec=Random)

        self.centralised_vcs_client_alice.update(random_mock)

        self.assertEquals([0], self.centralised_vcs_client_alice.working_copy.chunk_names)

    def _alice_modifies_a_chunk_in_working_copy(self):
        random_mock = Mock(spec=Random)
        random_mock.randint = Mock(side_effect=[456])
        random_mock.random = Mock(side_effect=[1.0])

        self.centralised_vcs_client_alice.working_copy.get_chunk(self.chunk.logical_name).modify("alice", random_mock)

    def _bob_modifies_a_chunk_in_working_copy(self):
        random_mock = Mock(spec=Random)
        random_mock.randint = Mock(side_effect=[789])
        random_mock.random = Mock(side_effect=[1.0])

        self.centralised_vcs_client_bob.working_copy.get_chunk(self.chunk.logical_name).modify("bob", random_mock)

    def _alice_updates_working_copy_and_commits_chunk(self):
        random_mock = Mock(spec=Random)
        random_mock.randint = Mock()
        random_mock.random = Mock()

        self.centralised_vcs_client_alice.update(random_mock)
        self.centralised_vcs_client_alice.commit()
        self.centralised_vcs_client_alice.update(random_mock)

    def _bob_updates_and_conflicts_working_copy(self):
        random_mock = Mock(spec=Random)
        random_mock.random = Mock(side_effect=[1.0])

        self.centralised_vcs_client_bob.update(random_mock)

    def _bob_manually_resolves_conflict(self):
        random_mock = Mock(spec=Random)
        random_mock.randint = Mock(side_effect=[234])
        random_mock.random = Mock(side_effect=[0.1, 1.0])

        self.centralised_vcs_client_bob.resolve(self.centralised_vcs_client_bob.conflicts[0], self.bob, random_mock)

    def _bob_commits_and_updates_working_copy(self):

        self.centralised_vcs_client_bob.commit()

        random_mock = Mock(spec=Random)

        random_mock.random = Mock(side_effect=[])
        self.centralised_vcs_client_bob.update(random_mock)

    def test_checkout_modify_update_and_commit(self):

        self._alice_modifies_a_chunk_in_working_copy()
        self._alice_updates_working_copy_and_commits_chunk()

        self.assertEquals([456], self.centralised_vcs_client_alice.working_copy.chunk_contents)

    def test_concurrent_checkout_modify_and_conflict(self):
        self._alice_modifies_a_chunk_in_working_copy()
        self._bob_modifies_a_chunk_in_working_copy()
        self._alice_updates_working_copy_and_commits_chunk()
        self._bob_updates_and_conflicts_working_copy()

        self.assertEquals(1, len(self.centralised_vcs_client_bob.conflicts))

    def test_that_automatic_merge_is_stateless(self):
        """
        Checks that a subsequent call to update cannot resolve a conflict that was not resolved automatically.
        """

        self._alice_modifies_a_chunk_in_working_copy()
        self._bob_modifies_a_chunk_in_working_copy()
        self._alice_updates_working_copy_and_commits_chunk()
        self._bob_updates_and_conflicts_working_copy()
        self._bob_updates_and_conflicts_working_copy()

        self.assertEquals(1, len(self.centralised_vcs_client_bob.conflicts))

    def test_that_conflicts_can_be_resolved(self):
        """
        Checks that a subsequent call to update cannot resolve a conflict that was not resolved automatically.
        """

        self._alice_modifies_a_chunk_in_working_copy()
        self._bob_modifies_a_chunk_in_working_copy()
        self._alice_updates_working_copy_and_commits_chunk()
        self._bob_updates_and_conflicts_working_copy()
        self._bob_manually_resolves_conflict()
        self._bob_commits_and_updates_working_copy()

        self.assertEquals(0, len(self.centralised_vcs_client_bob.conflicts))


if __name__ == '__main__':
    unittest.main()
