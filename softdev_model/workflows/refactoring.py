from theatre_ag import default_cost


class Refactoring(object):

    is_workflow = True

    def __init__(self, change_management, target_dependencies_per_feature=0):
        self.change_management = change_management
        self.target_dependencies_per_feature = target_dependencies_per_feature

    @default_cost(1)
    def refactoring(self, feature, random):
        feature.refactor(random)

    @default_cost()
    def refactor_feature(self, logical_name, random):

        self.change_management.checkout()

        feature = self.change_management.centralised_vcs_client.working_copy.get_feature(logical_name)

        while len(feature.dependencies) > self.target_dependencies_per_feature:
            self.refactoring(feature, random)
            self.change_management.commit_changes(random)

    @default_cost()
    def refactor_system(self, random):

        self.change_management.checkout()

        for feature in self.change_management.centralised_vcs_client.working_copy.features:
            self.refactor_feature(feature, random)
