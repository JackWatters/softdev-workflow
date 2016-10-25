from theatre_ag import workflow

from .change_management import ChangeManagement


class Implementation(ChangeManagement, object):

    def __init__(self, centralised_vcs_server):
        ChangeManagement.__init__(self, centralised_vcs_server)

    @workflow(1)
    def add_chunk(self, chunk_logical_name, feature, random):
        feature.extend(chunk_logical_name, random)

    @workflow()
    def implement_feature(self, feature, random):
        chunk_count = 0
        while not feature.is_implemented:
            self.add_chunk(chunk_count, feature, random)
            chunk_count += 1
            self.commit_changes(random)

    @workflow()
    def implement_system(self, random):

        self.checkout()

        for feature in self.centralised_vcs_client.working_copy.features:
            self.implement_feature(feature, random)
