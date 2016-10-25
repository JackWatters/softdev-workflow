from theatre_ag import workflow

from change_management import ChangeManagement


class Testing(ChangeManagement, object):

    def __init__(self, centralised_vcs_server, target_test_coverage_per_feature=1.0, target_tests_per_chunk_ratio=1):
        ChangeManagement.__init__(self, centralised_vcs_server)
        self.target_test_coverage_per_feature = target_test_coverage_per_feature
        self.target_tests_per_chunk_ratio = target_tests_per_chunk_ratio

    @workflow(1)
    def add_test(self, logical_name, feature):
        feature.add_test(logical_name)

    @workflow()
    def test_per_chunk_ratio(self, feature, random):

        test_count = 0

        while feature.test_coverage < self.target_test_coverage_per_feature or \
                feature.tests_per_chunk_ratio < self.target_tests_per_chunk_ratio:

            self.add_test(test_count, feature)
            test_count += 1
            self.commit_changes(random)

    @workflow()
    def complete_system_test_suite(self, random):

        self.checkout()

        for feature in self.centralised_vcs_client.working_copy.features:
            self.test_per_chunk_ratio(feature, random)
