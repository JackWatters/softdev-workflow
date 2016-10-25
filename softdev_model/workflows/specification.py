from theatre_ag import workflow
from .change_management import ChangeManagement


class Specification(ChangeManagement, object):

    def __init__(self, centralised_vcs_server):
        ChangeManagement.__init__(self, centralised_vcs_server)

    @workflow(1)
    def add_feature(self, logical_name, size, random):
        self.checkout()
        self.centralised_vcs_client.working_copy.add_feature(logical_name, size)
        self.commit_changes(random)

    @workflow()
    def complete_specification(self, schedule, random):
        for logical_name, feature_size in schedule:
            self.add_feature(logical_name, feature_size, random)

