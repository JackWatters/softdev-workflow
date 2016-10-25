from theatre_ag import workflow
from softdev_model.system import CentralisedVCSException


class ChangeManagement(object):

    def __init__(self, centralised_vcs_server):
        self.centralised_vcs_server = centralised_vcs_server
        self.centralised_vcs_client = None

    @workflow(1)
    def resolve(self, conflict, random):
        self.centralised_vcs_client.resolve(conflict, random)

    @workflow(0)
    def commit_changes(self, random):
        while True:
            try:
                self.centralised_vcs_client.commit()
                self.centralised_vcs_client.update(random)
                break
            except CentralisedVCSException:
                self.centralised_vcs_client.update(random)
                for conflict in self.centralised_vcs_client.conflicts:
                    self.resolve(conflict, random)

    @workflow(0)
    def checkout(self):
        self.centralised_vcs_client = self.centralised_vcs_server.checkout()
