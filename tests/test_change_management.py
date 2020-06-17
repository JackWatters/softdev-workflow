import unittest
from unittest.mock import Mock

from threading import _RLock

from theatre_ag import Actor, SynchronizingClock

from softdev_model.system import CentralisedVCSClient, CentralisedVCSServer, Conflict, SystemRandom
from softdev_model.workflows import ChangeManagement


class ChangeManagementTestCase(unittest.TestCase):

    def setUp(self):
        self.centralised_vcs_server = Mock(spec=CentralisedVCSServer)
        self.centralised_vcs_client = Mock(spec=CentralisedVCSClient)
        self.centralised_vcs_server.checkout = Mock(return_value=self.centralised_vcs_client)

        self.actor = Mock(spec=Actor)
        self.actor.busy = Mock(spec=_RLock)
        self.actor.clock = Mock(spec=SynchronizingClock)
        self.actor.completed_tasks = Mock(spec=list)

        self.change_management = ChangeManagement(self.centralised_vcs_server)

    def test_checkout(self):

        self.change_management.checkout()

        self.assertEquals(self.centralised_vcs_client, self.change_management.centralised_vcs_client)

    def test_resolve(self):
        self.change_management.checkout()

        random_mock = Mock(spec=SystemRandom)
        conflict_mock = Mock(spec=Conflict)
        self.change_management.resolve(conflict_mock, random_mock)

        self.centralised_vcs_client.resolve.assert_called_with(conflict_mock, random_mock)

    def test_commit_changes(self):

        self.change_management.checkout()

        random_mock = Mock(spec=SystemRandom)
        self.change_management.commit_changes(random_mock)

        self.centralised_vcs_client.commit.assert_called_with()
