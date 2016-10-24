from theatre_ag import default_cost
from change_management import commit_changes


@default_cost(1)
def add_feature(self, centralised_vcs_client, logical_name, size, random):
    centralised_vcs_client.working_copy.add_feature(logical_name, size)
    self.perform_task(commit_changes, [centralised_vcs_client, random])


def complete_specification(self, schedule, centralised_vcs_client, random):
    for logical_name, feature_size in schedule:
        self.perform_task(add_feature, [centralised_vcs_client, logical_name, feature_size, random])
