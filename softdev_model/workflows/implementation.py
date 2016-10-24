from theatre_ag import default_cost

from change_management import commit_changes


# noinspection PyUnusedLocal
@default_cost(1)
def add_chunk(self, chunk_logical_name, feature, random):
    feature.extend(chunk_logical_name, random)


def implement_feature(self, centralised_vcs_client, feature, random):
    chunk_count = 0
    while not feature.is_implemented:
        self.perform_task(add_chunk, [chunk_count, feature, random])
        chunk_count += 1
        self.perform_task(commit_changes, [centralised_vcs_client, random])


def implement_system(self, centralised_vcs_client, random):
    for feature in centralised_vcs_client.working_copy.features:
        self.perform_task(implement_feature, [centralised_vcs_client, feature, random])
