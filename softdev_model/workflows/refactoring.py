from theatre_ag import workflow

from change_management import ChangeManagement


class Refactoring(ChangeManagement, object):

    def __init__(self, centralised_vcs_server, target_dependencies_per_feature=0):
        ChangeManagement.__init__(self, centralised_vcs_server)
        self.target_dependencies_per_feature = target_dependencies_per_feature

    @workflow(1)
    def refactoring(self, feature, random):
        feature.refactor(random)

    @workflow()
    def refactor_feature(self, feature, random):
        while len(feature.dependencies) > self.target_dependencies_per_feature:
            self.refactoring(feature, random)
            self.commit_changes(random)

    @workflow()
    def refactor_system(self, random):

        self.checkout()

        for feature in self.centralised_vcs_client.working_copy.features:
            self.refactor_feature(feature, random)
