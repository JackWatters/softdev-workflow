from theatre_ag import default_cost, Workflow


class Refactoring(Workflow):

    def __init__(self, actor, change_management, target_dependencies_per_feature=0):
        super(Refactoring, self).__init__(actor)
        self.change_management = change_management
        self.target_dependencies_per_feature = target_dependencies_per_feature

    @default_cost(1)
    def refactoring(self, feature, random):
        feature.refactor(random)

    @default_cost()
    def refactor_feature(self, feature, random):
        while len(feature.dependencies) > self.target_dependencies_per_feature:
            self.refactoring(feature, random)
            self.change_management.commit_changes(random)

    @default_cost()
    def refactor_system(self, random):

        self.change_management.checkout()

        for feature in self.change_management.centralised_vcs_client.working_copy.features:
            self.refactor_feature(feature, random)
