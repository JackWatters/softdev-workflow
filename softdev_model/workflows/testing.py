from theatre_ag import default_cost

from change_management import commit_changes


@default_cost(1)
def add_test(self, logical_name, feature):
    feature.add_test(logical_name)


def test_per_chunk_ratio(
        self,
        centralised_vcs_client,
        feature,
        random,
        target_test_coverage_per_feature=1.0,
        target_tests_per_chunk_ratio=1):

    test_count = 0

    while feature.test_coverage < target_test_coverage_per_feature or \
            feature.tests_per_chunk_ratio < target_tests_per_chunk_ratio:

        self.perform_task(add_test, [test_count, feature])
        test_count += 1
        self.perform_task(commit_changes, [centralised_vcs_client, random])


def complete_system_test_suite(
        self,
        centralised_vcs_client,
        random,
        target_test_coverage_per_feature=1.0,
        target_minimum_tests_per_chunk=1):

    for feature in centralised_vcs_client.working_copy.features:
        self.perform_task(test_per_chunk_ratio,
                          [centralised_vcs_client,
                 feature, random,
                 target_test_coverage_per_feature,
                 target_minimum_tests_per_chunk])
