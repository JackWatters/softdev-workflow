from theatre_ag import default_cost

from change_management import commit_changes


# noinspection PyUnusedLocal
@default_cost(1)
def refactoring(self, feature, random):
    feature.refactor(random)


def refactor_feature(self, centralised_vcs_client, feature, random, target_dependencies_per_feature=0):
    while len(feature.dependencies) > target_dependencies_per_feature:
        self.perform_task(refactoring, [feature, random])
        self.perform_task(commit_changes, [centralised_vcs_client, random])


def refactor_system(self, centralised_vcs_client, random, target_dependencies_per_feature=0):
    for feature in centralised_vcs_client.working_copy.features:
        self.perform_task(refactor_feature, [centralised_vcs_client, feature, random, target_dependencies_per_feature])
